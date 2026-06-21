"""
Gemini API wrapper with:
- Multi-model fallback (auto-switches when rate limit hit)
- Image support (user can send photos for analysis)
- Chat mode system prompts (teacher, coder, friend, default)
"""
from __future__ import annotations

import base64
import logging
import re
import time

from google import genai
from google.genai import types

from bot.config import settings
from bot.retry import is_rate_limited, is_transient

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=settings.gemini_api_key)

# Fallback chain: primary model first, then backups in order.
# If primary hits rate limit, we silently try the next one.
FALLBACK_MODELS = [
    settings.gemini_model,          # gemini-3.1-flash-lite  (500 RPD)
    "gemini-2.5-flash",             # 20 RPD backup
    "gemini-3.5-flash",             # 20 RPD backup
    "gemini-3-flash",               # 20 RPD backup
]

# --- Chat mode system prompts ---
MODE_PROMPTS: dict[str, str] = {
    "default": (
        "You are a helpful, friendly AI assistant inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Keep answers concise and clear."
    ),
    "teacher": (
        "You are a patient, encouraging teacher inside a Telegram bot. "
        "Explain concepts step by step with simple examples. "
        "Always reply in the same language the user used. "
        "Use analogies and check understanding. Make learning fun!"
    ),
    "coder": (
        "You are an expert software engineer inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Give practical, working code examples. "
        "Prefer concise solutions. Mention edge cases and best practices."
    ),
    "friend": (
        "You are a warm, casual friend chatting on Telegram. "
        "Always reply in the same language the user used. "
        "Be empathetic, fun, use casual language. "
        "Keep it light and conversational — like texting a close friend."
    ),
    "translator": (
        "You are a professional translator inside a Telegram bot. "
        "When the user sends text, detect the language and translate it. "
        "If the user doesn't specify a target language, translate TO English "
        "unless the text is already in English — then translate to Azerbaijani. "
        "Always show: original language → target language, then the translation."
    ),
}

MODE_NAMES = {
    "default":    "🤖 Default",
    "teacher":    "📚 Müəllim",
    "coder":      "💻 Proqramçı",
    "friend":     "😊 Dost",
    "translator": "🌐 Tərcüməçi",
}


def _to_gemini_role(role: str) -> str:
    return "model" if role == "assistant" else "user"


def _build_contents(
    history: list[dict],
    new_message: str,
    image_bytes: bytes | None = None,
    image_mime: str = "image/jpeg",
) -> list[types.Content]:
    contents: list[types.Content] = []

    for msg in history:
        contents.append(
            types.Content(
                role=_to_gemini_role(msg["role"]),
                parts=[types.Part(text=msg["content"])],
            )
        )

    # Build the new user turn — may include an image
    user_parts: list[types.Part] = []
    if image_bytes:
        user_parts.append(
            types.Part(
                inline_data=types.Blob(mime_type=image_mime, data=image_bytes)
            )
        )
    if new_message:
        user_parts.append(types.Part(text=new_message))

    if user_parts:
        contents.append(types.Content(role="user", parts=user_parts))

    return contents


def _build_system_prompt(
    mode: str,
    language_hint: str | None = None,
) -> str:
    base = MODE_PROMPTS.get(mode, MODE_PROMPTS["default"])
    if language_hint:
        base += (
            f"\n\n(Context: this user's Telegram app language is '{language_hint}'. "
            "Use this only to disambiguate short/ambiguous messages — always "
            "prioritize the actual language the user is writing in.)"
        )
    return base


def _parse_retry_after(exc: Exception, default: int = 30) -> int:
    """Try to pull a 'retry in N seconds' hint out of a Gemini error message."""
    match = re.search(r"retry[_-]?delay['\"]?\s*[:=]\s*['\"]?(\d+)", str(exc), re.IGNORECASE)
    if not match:
        match = re.search(r"(\d+)\s*s(?:ec(?:ond)?s?)?\b", str(exc), re.IGNORECASE)
    if match:
        try:
            seconds = int(match.group(1))
            if 0 < seconds <= 600:
                return seconds
        except ValueError:
            pass
    return default


def generate_reply(
    history: list[dict],
    new_message: str,
    language_hint: str | None = None,
    mode: str = "default",
    image_bytes: bytes | None = None,
    image_mime: str = "image/jpeg",
) -> tuple[str, str]:
    """
    Call Gemini with automatic model fallback.

    Returns: (reply_text, model_used)

    Raises GeminiError only if ALL models in the fallback chain fail.
    """
    contents = _build_contents(history, new_message, image_bytes, image_mime)
    system_instruction = _build_system_prompt(mode, language_hint)

    last_error: Exception | None = None
    last_was_rate_limit = False

    for model in FALLBACK_MODELS:
        transient_attempts = 0
        while True:
            try:
                response = _client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                    ),
                )
                text = (response.text or "").strip()
                if not text:
                    raise GeminiError("Empty response from Gemini")

                if model != FALLBACK_MODELS[0]:
                    logger.warning("Used fallback model: %s", model)

                return text, model

            except GeminiError:
                raise  # empty response — no point retrying other models

            except Exception as exc:  # noqa: BLE001
                if is_rate_limited(exc):
                    logger.warning("Model %s rate-limited, trying next. Error: %s", model, exc)
                    last_error = exc
                    last_was_rate_limit = True
                    time.sleep(0.3)
                    break  # next model in outer for-loop

                if is_transient(exc) and transient_attempts < 2:
                    # Network glitch (timeout, connection reset, etc) — retry the
                    # SAME model a couple of times with backoff before giving up on it.
                    transient_attempts += 1
                    delay = min(4.0, 0.5 * (2 ** (transient_attempts - 1)))
                    logger.warning(
                        "Model %s transient error (attempt %s), retrying in %.1fs: %s",
                        model, transient_attempts, delay, exc,
                    )
                    last_error = exc
                    last_was_rate_limit = False
                    time.sleep(delay)
                    continue

                # Other errors (auth, invalid request, etc.) → fail immediately
                raise GeminiError(str(exc)) from exc

    if last_was_rate_limit:
        raise GeminiRateLimitError(
            f"All models rate-limited. Last error: {last_error}",
            retry_after=_parse_retry_after(last_error) if last_error else 30,
        )
    raise GeminiError(
        f"All models exhausted. Last error: {last_error}"
    )


def generate_reply_stream(
    history: list[dict],
    new_message: str,
    language_hint: str | None = None,
    mode: str = "default",
    image_bytes: bytes | None = None,
    image_mime: str = "image/jpeg",
):
    """
    Streaming version of generate_reply(). Yields (text_piece, model, is_done)
    tuples as Gemini generates the reply chunk by chunk.

    Falls back to the next model in FALLBACK_MODELS only if the FIRST chunk
    of a model fails (rate limit / transient) — once a model has started
    streaming, we stick with it (switching mid-stream would duplicate text).

    Raises GeminiError / GeminiRateLimitError if every model fails before
    producing any output.
    """
    contents = _build_contents(history, new_message, image_bytes, image_mime)
    system_instruction = _build_system_prompt(mode, language_hint)

    last_error: Exception | None = None
    last_was_rate_limit = False

    for model in FALLBACK_MODELS:
        transient_attempts = 0
        while True:
            started = False
            full_text = ""
            try:
                stream = _client.models.generate_content_stream(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                    ),
                )
                for chunk in stream:
                    piece = getattr(chunk, "text", None) or ""
                    if piece:
                        started = True
                        full_text += piece
                        yield piece, model, False

                if not full_text.strip():
                    raise GeminiError("Empty response from Gemini")

                if model != FALLBACK_MODELS[0]:
                    logger.warning("Used fallback model (stream): %s", model)

                yield "", model, True
                return

            except GeminiError:
                raise

            except Exception as exc:  # noqa: BLE001
                if started:
                    # Already streamed partial content to the user — can't cleanly
                    # fall back to another model now without duplicating text.
                    raise GeminiError(str(exc)) from exc

                if is_rate_limited(exc):
                    logger.warning("Model %s rate-limited (stream), trying next. Error: %s", model, exc)
                    last_error = exc
                    last_was_rate_limit = True
                    time.sleep(0.3)
                    break

                if is_transient(exc) and transient_attempts < 2:
                    transient_attempts += 1
                    delay = min(4.0, 0.5 * (2 ** (transient_attempts - 1)))
                    logger.warning(
                        "Model %s transient error (stream, attempt %s), retrying in %.1fs: %s",
                        model, transient_attempts, delay, exc,
                    )
                    last_error = exc
                    last_was_rate_limit = False
                    time.sleep(delay)
                    continue

                raise GeminiError(str(exc)) from exc

    if last_was_rate_limit:
        raise GeminiRateLimitError(
            f"All models rate-limited. Last error: {last_error}",
            retry_after=_parse_retry_after(last_error) if last_error else 30,
        )
    raise GeminiError(
        f"All models exhausted. Last error: {last_error}"
    )


class GeminiError(Exception):
    """Raised when the Gemini API call fails or returns nothing usable."""


class GeminiRateLimitError(GeminiError):
    """Raised when every model in the fallback chain is rate-limited."""

    def __init__(self, message: str, retry_after: int = 30) -> None:
        super().__init__(message)
        self.retry_after = retry_after

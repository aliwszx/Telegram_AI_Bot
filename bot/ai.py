"""
Gemini API wrapper with:
- Single model: gemini-3.1-flash-lite (no fallback)
- Image, audio, PDF/document support
- Extended chat modes (10 personas)
- Streaming support
- Language-aware responses
"""
from __future__ import annotations

import logging
import re
import time

from google import genai
from google.genai import types

from bot.config import settings
from bot.retry import is_rate_limited, is_transient, is_model_not_found, is_daily_quota_exhausted

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=settings.gemini_api_key)

# Yalnız bir model istifadə olunur — fallback yoxdur.
MODEL = settings.gemini_model  # gemini-3.1-flash-lite

# RPM aşımında eyni modeli yenidən cəhd etmək üçün maksimum gözləmə (saniyə)
_RPM_RETRY_WAIT = 65   # 1 dəqiqə + 5 saniyə buffer
_RPM_MAX_RETRIES = 4   # maksimum RPM retry (fallback olmadığı üçün daha çox cəhd)

# ── Chat mode system prompts ───────────────────────────────────────────────

MODE_PROMPTS: dict[str, str] = {
    "default": (
        "You are a helpful, friendly AI assistant inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Keep answers concise, clear and well-structured. "
        "Use emojis sparingly to make responses more readable."
    ),
    "teacher": (
        "You are a patient, encouraging teacher inside a Telegram bot. "
        "Explain concepts step by step with simple examples and analogies. "
        "Always reply in the same language the user used. "
        "Check for understanding, use bullet points for clarity. Make learning fun and engaging!"
    ),
    "coder": (
        "You are an expert senior software engineer inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Give practical, working code with brief explanations. "
        "Prefer concise, idiomatic solutions. Highlight edge cases, security concerns, "
        "and performance implications. Use code blocks for all code snippets."
    ),
    "friend": (
        "You are a warm, empathetic close friend chatting on Telegram. "
        "Always reply in the same language the user used. "
        "Be casual, fun, supportive. Use conversational language, "
        "show genuine interest and care. Keep it light and natural — like texting."
    ),
    "translator": (
        "You are a professional multilingual translator inside a Telegram bot. "
        "When the user sends text, detect the source language and translate it. "
        "If no target language specified: if text is English → translate to Azerbaijani, "
        "otherwise → translate to English. "
        "Format: 🔤 [Source lang] → [Target lang]\n[Translation]\n\n💡 [Brief cultural note if relevant]"
    ),
    "lawyer": (
        "You are an experienced legal advisor inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Provide clear, practical legal information. Always note that this is general "
        "information and not a substitute for professional legal advice. "
        "Reference relevant laws when possible. Be thorough but accessible."
    ),
    "doctor": (
        "You are a knowledgeable medical information assistant inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Provide accurate health information clearly and compassionately. "
        "ALWAYS recommend consulting a real doctor for diagnosis/treatment. "
        "Never diagnose. Focus on symptoms, general information, and when to seek care."
    ),
    "psychologist": (
        "You are a compassionate, professional psychologist assistant inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Listen actively, validate feelings, and offer evidence-based coping strategies. "
        "Be warm, non-judgmental, and supportive. "
        "For serious mental health concerns, always encourage professional help. "
        "Never provide diagnosis."
    ),
    "chef": (
        "You are a creative, professional chef and culinary expert inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Share recipes with clear steps, ingredient measurements, cooking tips, and variations. "
        "Include cooking time, difficulty level, and serving size. "
        "Suggest substitutions for dietary restrictions when relevant."
    ),
    "fitness": (
        "You are a certified personal trainer and nutrition expert inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Provide safe, effective workout plans and nutrition advice tailored to goals. "
        "Always emphasize proper form to prevent injury. "
        "Remind users to consult healthcare providers before starting new exercise programs."
    ),
}

MODE_NAMES = {
    "default":      "🤖 Standart",
    "teacher":      "📚 Müəllim",
    "coder":        "💻 Proqramçı",
    "friend":       "😊 Dost",
    "translator":   "🌐 Tərcüməçi",
    "lawyer":       "⚖️ Hüquqçu",
    "doctor":       "🏥 Həkim",
    "psychologist": "🧠 Psixoloq",
    "chef":         "👨‍🍳 Aşpaz",
    "fitness":      "💪 Fitnes",
}

MODE_DESCRIPTIONS = {
    "default":      "Ümumi köməkçi",
    "teacher":      "Addım-addım izahat",
    "coder":        "Kod və texnologiya",
    "friend":       "Mehriban söhbət",
    "translator":   "Dil tərcüməsi",
    "lawyer":       "Hüquqi məsləhət",
    "doctor":       "Tibbi məlumat",
    "psychologist": "Psixoloji dəstək",
    "chef":         "Resept və kulinariya",
    "fitness":      "İdman və sağlamlıq",
}


def _to_gemini_role(role: str) -> str:
    return "model" if role == "assistant" else "user"


def _build_contents(
    history: list[dict],
    new_message: str,
    media_bytes: bytes | None = None,
    media_mime: str = "image/jpeg",
) -> list[types.Content]:
    contents: list[types.Content] = []

    for msg in history:
        contents.append(
            types.Content(
                role=_to_gemini_role(msg["role"]),
                parts=[types.Part(text=msg["content"])],
            )
        )

    # Build new user turn — may include media
    user_parts: list[types.Part] = []
    if media_bytes:
        user_parts.append(
            types.Part(
                inline_data=types.Blob(mime_type=media_mime, data=media_bytes)
            )
        )
    if new_message:
        user_parts.append(types.Part(text=new_message))

    if user_parts:
        contents.append(types.Content(role="user", parts=user_parts))

    return contents


def _build_system_prompt(mode: str, language_hint: str | None = None) -> str:
    base = MODE_PROMPTS.get(mode, MODE_PROMPTS["default"])
    if language_hint:
        base += (
            f"\n\n(Context: user's Telegram app language is '{language_hint}'. "
            "Use this only to disambiguate short/ambiguous messages — always "
            "prioritize the actual language the user is writing in.)"
        )
    return base


def _build_config(system_instruction: str, web_search: bool) -> types.GenerateContentConfig:
    tools = [types.Tool(google_search=types.GoogleSearch())] if web_search else None
    return types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools,
    )


def _parse_retry_after(exc: Exception | None, default: int = 30) -> int:
    if exc is None:
        return default
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
    media_bytes: bytes | None = None,
    media_mime: str = "image/jpeg",
    web_search: bool = False,
) -> tuple[str, str]:
    """
    Call Gemini (single model, no fallback).
    Returns: (reply_text, model_used)
    Raises GeminiError only if ALL models fail.
    """
    contents = _build_contents(history, new_message, media_bytes, media_mime)
    system_instruction = _build_system_prompt(mode, language_hint)
    config = _build_config(system_instruction, web_search)

    last_error: Exception | None = None
    last_was_rate_limit = False

    transient_attempts = 0
    rpm_retries = 0
    while True:
        try:
            response = _client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=config,
            )
            text = (response.text or "").strip()
            if not text:
                raise GeminiError("Empty response from Gemini")

            return text, MODEL

        except GeminiError:
            raise

        except Exception as exc:  # noqa: BLE001
            if is_rate_limited(exc):
                # RPD dolubsa → fayda verməz, dərhal xəta ver
                if is_daily_quota_exhausted(exc):
                    logger.warning("Model %s daily quota exhausted. Error: %s", MODEL, exc)
                    last_error = exc
                    last_was_rate_limit = True
                    break

                # RPM aşımı → bir dəqiqə gözlə, yenidən cəhd et
                if rpm_retries < _RPM_MAX_RETRIES:
                    rpm_retries += 1
                    wait = _parse_retry_after(exc, default=_RPM_RETRY_WAIT)
                    logger.warning(
                        "Model %s RPM rate-limited (retry %s/%s), waiting %ss. Error: %s",
                        MODEL, rpm_retries, _RPM_MAX_RETRIES, wait, exc,
                    )
                    last_error = exc
                    last_was_rate_limit = True
                    time.sleep(wait)
                    continue

                logger.warning("Model %s RPM retries exhausted. Error: %s", MODEL, exc)
                last_error = exc
                last_was_rate_limit = True
                break

            if is_model_not_found(exc):
                logger.error("Model %s not found. Error: %s", MODEL, exc)
                last_error = exc
                last_was_rate_limit = False
                break

            if is_transient(exc):
                if transient_attempts < 2:
                    transient_attempts += 1
                    delay = min(4.0, 0.5 * (2 ** (transient_attempts - 1)))
                    logger.warning(
                        "Model %s transient error (attempt %s), retrying in %.1fs: %s",
                        MODEL, transient_attempts, delay, exc,
                    )
                    last_error = exc
                    last_was_rate_limit = False
                    time.sleep(delay)
                    continue
                else:
                    logger.warning("Model %s transient error exhausted retries. Error: %s", MODEL, exc)
                    last_error = exc
                    last_was_rate_limit = False
                    break

            raise GeminiError(str(exc)) from exc

    if last_was_rate_limit:
        raise GeminiRateLimitError(
            f"Model rate-limited. Last error: {last_error}",
            retry_after=_parse_retry_after(last_error),
        )
    raise GeminiError(f"Model failed. Last error: {last_error}")


def generate_reply_stream(
    history: list[dict],
    new_message: str,
    language_hint: str | None = None,
    mode: str = "default",
    media_bytes: bytes | None = None,
    media_mime: str = "image/jpeg",
    web_search: bool = False,
):
    """
    Streaming version. Yields (text_piece, model, is_done) tuples.
    Single model, no fallback. Retries on transient/RPM errors.
    """
    contents = _build_contents(history, new_message, media_bytes, media_mime)
    system_instruction = _build_system_prompt(mode, language_hint)
    config = _build_config(system_instruction, web_search)

    last_error: Exception | None = None
    last_was_rate_limit = False

    transient_attempts = 0
    rpm_retries = 0
    while True:
        started = False
        full_text = ""
        try:
            stream = _client.models.generate_content_stream(
                model=MODEL,
                contents=contents,
                config=config,
            )
            for chunk in stream:
                piece = getattr(chunk, "text", None) or ""
                if piece:
                    started = True
                    full_text += piece
                    yield piece, MODEL, False

            if not full_text.strip():
                raise GeminiError("Empty response from Gemini")

            yield "", MODEL, True
            return

        except GeminiError:
            raise

        except Exception as exc:  # noqa: BLE001
            if started:
                raise GeminiError(str(exc)) from exc

            if is_rate_limited(exc):
                if is_daily_quota_exhausted(exc):
                    logger.warning("Model %s daily quota exhausted (stream). Error: %s", MODEL, exc)
                    last_error = exc
                    last_was_rate_limit = True
                    break

                if rpm_retries < _RPM_MAX_RETRIES:
                    rpm_retries += 1
                    wait = _parse_retry_after(exc, default=_RPM_RETRY_WAIT)
                    logger.warning(
                        "Model %s RPM rate-limited (stream, retry %s/%s), waiting %ss. Error: %s",
                        MODEL, rpm_retries, _RPM_MAX_RETRIES, wait, exc,
                    )
                    last_error = exc
                    last_was_rate_limit = True
                    time.sleep(wait)
                    continue

                logger.warning("Model %s RPM retries exhausted (stream). Error: %s", MODEL, exc)
                last_error = exc
                last_was_rate_limit = True
                break

            if is_model_not_found(exc):
                logger.error("Model %s not found (stream). Error: %s", MODEL, exc)
                last_error = exc
                last_was_rate_limit = False
                break

            if is_transient(exc):
                if transient_attempts < 2:
                    transient_attempts += 1
                    delay = min(4.0, 0.5 * (2 ** (transient_attempts - 1)))
                    logger.warning(
                        "Model %s transient error (stream, attempt %s), retrying in %.1fs: %s",
                        MODEL, transient_attempts, delay, exc,
                    )
                    last_error = exc
                    last_was_rate_limit = False
                    time.sleep(delay)
                    continue
                else:
                    logger.warning("Model %s transient error exhausted retries (stream). Error: %s", MODEL, exc)
                    last_error = exc
                    last_was_rate_limit = False
                    break

            raise GeminiError(str(exc)) from exc

    if last_was_rate_limit:
        raise GeminiRateLimitError(
            f"Model rate-limited. Last error: {last_error}",
            retry_after=_parse_retry_after(last_error),
        )
    raise GeminiError(f"Model failed. Last error: {last_error}")


def generate_quick_reply(prompt: str) -> str:
    """Single-shot generation for inline mode and quick tasks. No history."""
    try:
        response = _client.models.generate_content(
            model=MODEL,
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(
                system_instruction=MODE_PROMPTS["default"],
            ),
        )
        return (response.text or "").strip()
    except Exception as exc:
        raise GeminiError(str(exc)) from exc


class GeminiError(Exception):
    """Raised when the Gemini API call fails or returns nothing usable."""


class GeminiRateLimitError(GeminiError):
    """Raised when the model is rate-limited."""

    def __init__(self, message: str, retry_after: int = 30) -> None:
        super().__init__(message)
        self.retry_after = retry_after

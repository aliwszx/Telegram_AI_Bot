"""
Gemini API wrapper with:
- Multi-model fallback (auto-switches when rate limit hit)
- Image support (user can send photos for analysis)
- Chat mode system prompts (teacher, coder, friend, default)
"""
from __future__ import annotations

import base64
import logging
import time

from google import genai
from google.genai import types

from bot.config import settings

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

    for model in FALLBACK_MODELS:
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
            err_str = str(exc).lower()
            # Rate limit / quota errors → try next model
            if any(k in err_str for k in ("429", "quota", "rate", "resource_exhausted")):
                logger.warning("Model %s rate-limited, trying next. Error: %s", model, exc)
                last_error = exc
                time.sleep(0.3)
                continue
            # Other errors (auth, invalid request, etc.) → fail immediately
            raise GeminiError(str(exc)) from exc

    raise GeminiError(
        f"All models exhausted. Last error: {last_error}"
    )


class GeminiError(Exception):
    """Raised when the Gemini API call fails or returns nothing usable."""

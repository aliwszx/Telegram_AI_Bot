"""
Thin wrapper around the Gemini API (google-genai SDK).

The SDK client is synchronous, so generate_reply() is meant to be called via
asyncio.to_thread(...) from async handlers to avoid blocking the event loop.
"""
from __future__ import annotations

from google import genai
from google.genai import types

from bot.config import settings

_client = genai.Client(api_key=settings.gemini_api_key)


def _to_gemini_role(role: str) -> str:
    return "model" if role == "assistant" else "user"


def _build_contents(history: list[dict], new_message: str) -> list[types.Content]:
    contents: list[types.Content] = []
    for msg in history:
        contents.append(
            types.Content(
                role=_to_gemini_role(msg["role"]),
                parts=[types.Part(text=msg["content"])],
            )
        )
    contents.append(types.Content(role="user", parts=[types.Part(text=new_message)]))
    return contents


def generate_reply(
    history: list[dict], new_message: str, language_hint: str | None = None
) -> str:
    """
    Synchronous call to Gemini. `history` is a list of
    {"role": "user"|"assistant", "content": str} dicts, oldest first.

    `language_hint` is the user's Telegram app language code (e.g. "az",
    "uz", "en") taken from message.from_user.language_code. It's only used
    by the model as a tiebreaker for short/ambiguous messages (e.g. a one-word
    greeting shared by several similar languages) — it never overrides a
    language the user is clearly writing in.
    """
    contents = _build_contents(history, new_message)

    system_instruction = settings.gemini_system_prompt
    if language_hint:
        system_instruction += (
            f"\n\n(Context: this user's Telegram app language is set to "
            f"'{language_hint}'. Use this only to disambiguate short or "
            f"unclear messages — always prioritize the actual language the "
            f"user is writing in if it's clear.)"
        )

    try:
        response = _client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - we want a clean user-facing fallback
        raise GeminiError(str(exc)) from exc

    text = (response.text or "").strip()
    if not text:
        raise GeminiError("Empty response from Gemini")
    return text


class GeminiError(Exception):
    """Raised when the Gemini API call fails or returns nothing usable."""

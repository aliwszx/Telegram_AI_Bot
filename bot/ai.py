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


def generate_reply(history: list[dict], new_message: str) -> str:
    """
    Synchronous call to Gemini. `history` is a list of
    {"role": "user"|"assistant", "content": str} dicts, oldest first.
    """
    contents = _build_contents(history, new_message)

    try:
        response = _client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=settings.gemini_system_prompt,
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

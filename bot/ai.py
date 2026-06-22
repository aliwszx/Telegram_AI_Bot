"""
Clean Gemini AI wrapper (production-ready)
- Multi API key rotation (round-robin)
- Model fallback chain
- Retry with exponential backoff
- Streaming support
- Simple quick reply wrapper
"""

from __future__ import annotations

import itertools
import time
import logging
from typing import Iterator

from google import genai
from google.genai import types

from bot.config import settings
from bot.retry import is_rate_limited, is_transient, is_model_not_found

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# MODELS (BEST → FALLBACK)
# ─────────────────────────────────────────────

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2-flash",
]


# ─────────────────────────────────────────────
# KEY ROTATION (SIMPLE ROUND ROBIN)
# ─────────────────────────────────────────────

class KeyManager:
    def __init__(self, api_keys: list[str]):
        self.clients = [genai.Client(api_key=k) for k in api_keys if k]
        if not self.clients:
            raise ValueError("No Gemini API keys provided")

        self._cycle = itertools.cycle(self.clients)

    def next_client(self) -> genai.Client:
        return next(self._cycle)


key_manager = KeyManager(
    settings.gemini_api_keys or [settings.gemini_api_key]
)


# ─────────────────────────────────────────────
# CORE BUILDER
# ─────────────────────────────────────────────

def build_contents(history: list[dict], new_message: str):
    contents = []

    for msg in history:
        role = "user" if msg["role"] != "assistant" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])],
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=new_message)],
        )
    )

    return contents


# ─────────────────────────────────────────────
# MAIN GENERATION
# ─────────────────────────────────────────────

def generate_reply(
    history: list[dict],
    new_message: str,
    system_prompt: str = "You are a helpful assistant",
) -> tuple[str, str]:
    """
    Returns: (text, model_used)
    """

    contents = build_contents(history, new_message)

    last_error = None

    for model in MODELS:
        client = key_manager.next_client()

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                    ),
                )

                text = (response.text or "").strip()

                if text:
                    return text, model

                raise RuntimeError("Empty response")

            except Exception as e:
                last_error = e

                if is_model_not_found(e):
                    break  # try next model

                if is_transient(e):
                    time.sleep(0.5 * (2 ** attempt))
                    continue

                if is_rate_limited(e):
                    time.sleep(2 * (attempt + 1))
                    continue

                break  # unknown error → next model

    raise RuntimeError(f"All models failed: {last_error}")


# ─────────────────────────────────────────────
# STREAMING
# ─────────────────────────────────────────────

def generate_reply_stream(
    history: list[dict],
    new_message: str,
    system_prompt: str = "You are a helpful assistant",
) -> Iterator[tuple[str, str, bool]]:
    """
    Yields: (text_chunk, model, is_done)
    """

    contents = build_contents(history, new_message)

    for model in MODELS:
        client = key_manager.next_client()

        try:
            stream = client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                ),
            )

            for chunk in stream:
                piece = getattr(chunk, "text", "") or ""
                if piece:
                    yield piece, model, False

            yield "", model, True
            return

        except Exception as e:
            if is_model_not_found(e):
                continue
            if is_rate_limited(e):
                time.sleep(2)
                continue
            continue

    raise RuntimeError("All models failed")


# ─────────────────────────────────────────────
# QUICK REPLY (FIX FOR YOUR HANDLERS)
# ─────────────────────────────────────────────

def generate_quick_reply(prompt: str) -> str:
    """
    Simple wrapper for single prompt calls.
    Keeps handlers.py compatible.
    """
    text, _ = generate_reply([], prompt)
    return text

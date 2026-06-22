"""
Clean Gemini API wrapper:
- No blacklist system
- Smart retry with exponential backoff
- Model fallback chain
- Multi-key support (simple round-robin)
"""

from __future__ import annotations

import itertools
import time
import logging
from typing import Iterator
from dataclasses import dataclass

from google import genai
from google.genai import types

from bot.config import settings
from bot.retry import is_rate_limited, is_transient, is_model_not_found

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# MODELS (CLEAN + CORRECT NAMES)
# ─────────────────────────────────────────────

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2-flash",
]

# fallback safety order (best → weakest)


# ─────────────────────────────────────────────
# KEY ROTATION (SIMPLE ROUND ROBIN)
# ─────────────────────────────────────────────

class KeyManager:
    def __init__(self, api_keys: list[str]):
        self.clients = [genai.Client(api_key=k) for k in api_keys]
        self._cycle = itertools.cycle(self.clients)

    def next_client(self) -> genai.Client:
        return next(self._cycle)


key_manager = KeyManager(settings.gemini_api_keys or [settings.gemini_api_key])


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def build_contents(history, new_message):
    contents = []

    for msg in history:
        contents.append(
            types.Content(
                role="user" if msg["role"] != "assistant" else "model",
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

def generate_reply(history, new_message, system_prompt: str = "You are a helpful assistant"):
    contents = build_contents(history, new_message)

    last_error = None

    for model in MODELS:
        client = key_manager.next_client()

        for attempt in range(3):  # retry per model
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    ),
                )

                text = (response.text or "").strip()
                if text:
                    return text, model

            except Exception as e:
                last_error = e

                if is_model_not_found(e):
                    break  # skip this model

                if is_transient(e):
                    time.sleep(0.5 * (2 ** attempt))
                    continue

                if is_rate_limited(e):
                    time.sleep(2 * (attempt + 1))
                    continue

                break  # unknown error → next model

    raise RuntimeError(f"All models failed: {last_error}")


# ─────────────────────────────────────────────
# STREAMING VERSION
# ─────────────────────────────────────────────

def generate_reply_stream(history, new_message, system_prompt: str = "You are a helpful assistant"):
    contents = build_contents(history, new_message)

    for model in MODELS:
        client = key_manager.next_client()

        try:
            stream = client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
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

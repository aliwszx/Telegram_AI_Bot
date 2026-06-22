"""
Gemini AI wrapper
Stable production version
"""

from __future__ import annotations

import itertools
import time
import logging
from typing import Iterator

from google import genai
from google.genai import types

from bot.config import settings
from bot.retry import (
    is_rate_limited,
    is_transient,
    is_model_not_found,
)

logger = logging.getLogger(__name__)


# =====================================================
# MODELS
# =====================================================

MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2-flash",
]


# =====================================================
# ERRORS
# =====================================================

class GeminiError(Exception):
    pass


class GeminiRateLimitError(GeminiError):

    def __init__(self, message: str, retry_after: int = 30):
        super().__init__(message)
        self.retry_after = retry_after


# =====================================================
# KEY ROTATION
# =====================================================

class KeyManager:

    def __init__(self, keys: list[str]):

        keys = [k for k in keys if k]

        if not keys:
            raise GeminiError(
                "No Gemini API keys configured"
            )

        self.clients = [
            genai.Client(api_key=k)
            for k in keys
        ]

        self.pool = itertools.cycle(self.clients)


    def next(self):
        return next(self.pool)



key_manager = KeyManager(
    settings.gemini_api_keys
    or [settings.gemini_api_key]
)



# =====================================================
# CONTENT BUILDER
# =====================================================

def _build_contents(
    history: list[dict],
    message: str,
):

    contents = []


    for item in history:

        contents.append(
            types.Content(
                role=(
                    "model"
                    if item["role"] == "assistant"
                    else "user"
                ),
                parts=[
                    types.Part(
                        text=item["content"]
                    )
                ],
            )
        )


    if message:

        contents.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=message
                    )
                ],
            )
        )


    return contents



# =====================================================
# NORMAL GENERATE
# =====================================================

def generate_reply(
    history: list[dict],
    new_message: str,
    system_prompt: str = (
        "You are a helpful AI assistant. "
        "Reply in the user's language."
    ),
):

    contents = _build_contents(
        history,
        new_message
    )


    last_error = None


    for model in MODELS:

        client = key_manager.next()


        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    ),
                )


                text = (
                    response.text or ""
                ).strip()


                if text:

                    return text, model



            except Exception as e:

                last_error = e


                if is_model_not_found(e):
                    break


                if is_rate_limited(e):

                    if attempt == 2:
                        break

                    time.sleep(
                        2 * (attempt + 1)
                    )
                    continue


                if is_transient(e):

                    time.sleep(
                        0.5 * (2 ** attempt)
                    )
                    continue


                break



    raise GeminiRateLimitError(
        f"All Gemini models failed: {last_error}"
    )



# =====================================================
# STREAM
# =====================================================

def generate_reply_stream(
    history: list[dict],
    new_message: str,
    system_prompt: str = (
        "You are a helpful AI assistant."
    ),
) -> Iterator[tuple[str, str, bool]]:


    contents = _build_contents(
        history,
        new_message
    )


    for model in MODELS:

        client = key_manager.next()


        try:

            stream = (
                client.models
                .generate_content_stream(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    ),
                )
            )


            for chunk in stream:

                text = (
                    getattr(chunk, "text", "")
                    or ""
                )


                if text:

                    yield (
                        text,
                        model,
                        False
                    )


            yield (
                "",
                model,
                True
            )

            return



        except Exception as e:

            if is_model_not_found(e):
                continue

            if is_rate_limited(e):
                time.sleep(2)
                continue


            continue



    raise GeminiRateLimitError(
        "Stream failed for all models"
    )



# =====================================================
# QUICK REPLY
# =====================================================

def generate_quick_reply(
    prompt: str
) -> str:

    text, _ = generate_reply(
        history=[],
        new_message=prompt,
    )

    return text

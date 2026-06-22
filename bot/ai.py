"""
Gemini AI wrapper
- Multi API key rotation
- Model fallback
- Retry handling
- Streaming
- Chat modes
- Telegram handler compatible
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
# MODE SYSTEM (handlers.py needs these)
# =====================================================

MODE_PROMPTS = {

    "default": (
        "You are a helpful AI assistant. "
        "Reply in the same language as the user."
    ),

    "teacher": (
        "You are a patient teacher. "
        "Explain step by step with examples."
    ),

    "coder": (
        "You are a senior software engineer. "
        "Give practical coding help."
    ),

    "friend": (
        "You are a friendly AI friend. "
        "Be casual and supportive."
    ),

    "translator": (
        "You are a professional translator. "
        "Translate accurately."
    ),

    "lawyer": (
        "You provide general legal information. "
        "Do not replace a real lawyer."
    ),

    "doctor": (
        "You provide medical information. "
        "Do not diagnose."
    ),

    "psychologist": (
        "You are a supportive psychology assistant. "
        "Do not diagnose."
    ),

    "chef": (
        "You are a professional chef. "
        "Give recipes and cooking advice."
    ),

    "fitness": (
        "You are a fitness coach. "
        "Give safe workout advice."
    ),
}



MODE_NAMES = {

    "default": "🤖 Standart",
    "teacher": "📚 Müəllim",
    "coder": "💻 Proqramçı",
    "friend": "😊 Dost",
    "translator": "🌐 Tərcüməçi",
    "lawyer": "⚖️ Hüquqçu",
    "doctor": "🏥 Həkim",
    "psychologist": "🧠 Psixoloq",
    "chef": "👨‍🍳 Aşpaz",
    "fitness": "💪 Fitnes",
}



MODE_DESCRIPTIONS = {

    "default": "Ümumi köməkçi",
    "teacher": "Addım-addım izah",
    "coder": "Kod və texnologiya",
    "friend": "Söhbət",
    "translator": "Tərcümə",
    "lawyer": "Hüquq",
    "doctor": "Sağlamlıq",
    "psychologist": "Psixoloji",
    "chef": "Resept",
    "fitness": "İdman",
}



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

    def __init__(
        self,
        message: str,
        retry_after: int = 30
    ):
        super().__init__(message)
        self.retry_after = retry_after



# =====================================================
# API KEY ROTATION
# =====================================================

class KeyManager:

    def __init__(self, keys):

        keys = [
            k for k in keys
            if k
        ]

        if not keys:
            raise GeminiError(
                "Gemini API key missing"
            )


        self.clients = [
            genai.Client(api_key=k)
            for k in keys
        ]


        self.pool = itertools.cycle(
            self.clients
        )


    def next(self):

        return next(self.pool)



key_manager = KeyManager(
    settings.gemini_api_keys
    or [settings.gemini_api_key]
)



# =====================================================
# BUILD CONTENT
# =====================================================

def _build_contents(
    history,
    message
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
# MAIN AI
# =====================================================

def generate_reply(
    history,
    new_message,
    system_prompt=None,
    mode="default",
):

    if system_prompt is None:

        system_prompt = MODE_PROMPTS.get(
            mode,
            MODE_PROMPTS["default"]
        )


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

                    )
                )


                text = (
                    response.text
                    or ""
                ).strip()


                if text:

                    return text, model



            except Exception as e:

                last_error = e


                if is_model_not_found(e):
                    break


                if is_rate_limited(e):

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
        str(last_error)
    )



# =====================================================
# STREAM
# =====================================================

def generate_reply_stream(
    history,
    new_message,
    system_prompt=None,
    mode="default",
) -> Iterator:


    if system_prompt is None:

        system_prompt = MODE_PROMPTS.get(
            mode,
            MODE_PROMPTS["default"]
        )


    contents = _build_contents(
        history,
        new_message
    )


    for model in MODELS:


        client = key_manager.next()


        try:

            stream = client.models.generate_content_stream(

                model=model,

                contents=contents,

                config=types.GenerateContentConfig(

                    system_instruction=system_prompt

                )
            )


            for chunk in stream:

                text = (
                    getattr(chunk,"text","")
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



        except Exception:

            continue



    raise GeminiRateLimitError(
        "Stream failed"
    )



# =====================================================
# QUICK REPLY
# =====================================================

def generate_quick_reply(
    prompt: str
):

    text, _ = generate_reply(
        history=[],
        new_message=prompt
    )

    return text

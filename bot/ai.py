from __future__ import annotations

import os
import logging
from typing import Generator

from google import genai
from google.genai import types

from bot.config import settings


logger = logging.getLogger(__name__)


# ==========================
# AI MODES
# ==========================

MODE_NAMES = {
    "default": "🤖 Normal",
    "coder": "💻 Kodçu",
    "teacher": "🎓 Müəllim",
    "translator": "🌍 Tərcüməçi",
    "writer": "✍️ Yazıçı",
    "analyst": "📊 Analitik",
    "creative": "🎨 Kreativ",
    "friend": "😊 Dost",
    "expert": "🧠 Ekspert",
    "short": "⚡ Qısa",
}


MODE_DESCRIPTIONS = {
    "default": "Normal AI köməkçi rejimi",
    "coder": "Kod yazır, səhv tapır və izah edir",
    "teacher": "Mövzuları sadə şəkildə öyrədir",
    "translator": "Dil tərcümələri edir",
    "writer": "Mətnlər və ideyalar hazırlayır",
    "analyst": "Analiz və araşdırma edir",
    "creative": "Yaradıcı ideyalar verir",
    "friend": "Dost kimi danışır",
    "expert": "Dərin texniki cavablar verir",
    "short": "Qısa cavab verir",
}


# ==========================
# ERRORS
# ==========================

class GeminiError(Exception):
    pass


class GeminiRateLimitError(GeminiError):

    def __init__(self, retry_after: int = 30):
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit. Retry after {retry_after}s"
        )


# ==========================
# KEYS
# ==========================

KEYS = []


if os.getenv("GEMINI_API_KEYS"):
    KEYS = [
        x.strip()
        for x in os.getenv("GEMINI_API_KEYS").split(",")
        if x.strip()
    ]

elif getattr(settings, "gemini_api_key", None):
    KEYS = [
        settings.gemini_api_key
    ]


_current_key = 0


def _client():

    global _current_key

    if not KEYS:
        raise GeminiError(
            "Gemini API key yoxdur"
        )

    return genai.Client(
        api_key=KEYS[_current_key]
    )


def _rotate_key():

    global _current_key

    if len(KEYS) <= 1:
        return

    _current_key = (
        _current_key + 1
    ) % len(KEYS)

    logger.warning(
        "Gemini key dəyişdi: %s",
        _current_key
    )


# ==========================
# SYSTEM PROMPT
# ==========================

def _system_prompt(mode):

    return f"""
Sən Telegram üçün AI assistantsan.

Aktiv rejim:
{MODE_NAMES.get(mode, "🤖 Normal")}

Qaydalar:
- Azərbaycan dilində cavab ver
- Lazımsız uzatma
- Dəqiq cavab ver
- İstifadəçinin dilinə uyğunlaş
"""


# ==========================
# MAIN GENERATION
# ==========================

def generate_reply(
    history,
    user_text,
    language_hint=None,
    mode="default",
    media_bytes=None,
    media_mime="image/jpeg",
    web_search=False,
):

    tries = max(len(KEYS), 1)


    for _ in range(tries):

        try:

            client = _client()


            contents = []


            for msg in history[-20:]:

                contents.append(
                    {
                        "role":
                            "user"
                            if msg["role"] == "user"
                            else "model",

                        "parts":[
                            {
                                "text":
                                msg["content"]
                            }
                        ]
                    }
                )


            parts = []


            if user_text:
                parts.append(
                    {
                        "text": user_text
                    }
                )


            if media_bytes:

                parts.append(
                    {
                        "inline_data":
                        {
                            "mime_type": media_mime,
                            "data": media_bytes
                        }
                    }
                )


            contents.append(
                {
                    "role":"user",
                    "parts":parts
                }
            )


            result = client.models.generate_content(

                model="gemini-3.1-flash-lite",

                contents=contents,

                config=types.GenerateContentConfig(
                    system_instruction=
                    _system_prompt(mode),

                    temperature=0.7,

                    max_output_tokens=2048,
                )
            )


            answer = (
                result.text
                if result.text
                else ""
            )


            if not answer:
                raise GeminiError(
                    "Boş cavab gəldi"
                )


            return (
                answer,
                "gemini-3.1-flash-lite"
            )


        except Exception as e:


            error = str(e).lower()


            if (
                "429" in error
                or "quota" in error
                or "rate" in error
            ):

                _rotate_key()

                continue


            logger.exception(e)

            raise GeminiError(str(e))


    raise GeminiRateLimitError(60)



# ==========================
# STREAM
# ==========================

def generate_reply_stream(
    history,
    user_text,
    language_hint=None,
    mode="default",
    media_bytes=None,
    media_mime="image/jpeg",
    web_search=False,
):

    text, model = generate_reply(
        history,
        user_text,
        language_hint,
        mode,
        media_bytes,
        media_mime,
        web_search
    )


    size = 60


    chunks = [
        text[i:i+size]
        for i in range(
            0,
            len(text),
            size
        )
    ]


    for index, chunk in enumerate(chunks):

        yield (
            chunk,
            model,
            index == len(chunks)-1
        )



# ==========================
# INLINE / QUICK
# ==========================

def generate_quick_reply(prompt):

    answer, _ = generate_reply(
        [],
        prompt,
        mode="short"
    )

    return answer

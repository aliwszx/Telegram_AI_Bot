"""
Production Gemini AI Layer

Features:
- Multi API key rotation
- Model fallback
- Mode isolation
- Streaming
- Retry
- Telegram handler compatible
"""

from __future__ import annotations

import itertools
import logging
import time

from typing import Iterator

from google import genai
from google.genai import types

from bot.config import settings
from bot.lang import MODE_NAMES, MODE_DESCRIPTIONS

logger = logging.getLogger(__name__)


# ==========================
# MODES
# ==========================



MODE_PROMPTS = {

"default":
"""
You are a helpful AI assistant.
Answer naturally.
""",

"teacher":
"""
You are an expert teacher.
Explain step by step with examples.
""",

"coder":
"""
You are a senior software engineer.
Give clean practical solutions.
""",

"friend":
"""
You are a friendly AI friend.
Be casual and helpful.
""",

"translator":
"""
You are a professional translator.
Translate accurately.
Do not add explanations unless asked.
""",

"writer":
"""
You are a professional writer.
Create high quality text.
""",

"analyst":
"""
You are an analytical expert.
Think carefully and explain reasoning.
""",

"creative":
"""
You are creative assistant.
Generate original ideas.
""",

"fitness":
"""
You are a fitness coach.
Give safe training advice.
""",

"chef":
"""
You are a chef assistant.
Give cooking guidance.
"""

}



# ==========================
# ERRORS
# ==========================


class GeminiError(Exception):
    pass



class GeminiRateLimitError(GeminiError):

    def __init__(
        self,
        message="Rate limited",
        retry_after=30
    ):
        super().__init__(message)
        self.retry_after = retry_after



# ==========================
# CLIENT MANAGER
# ==========================


class GeminiClientManager:


    def __init__(self):

        keys = (
            settings.gemini_api_keys
            or [settings.gemini_api_key]
        )

        self.clients = [
            genai.Client(
                api_key=k
            )
            for k in keys
            if k
        ]


        if not self.clients:
            raise GeminiError(
                "No Gemini API keys"
            )


        self.pool = itertools.cycle(
            self.clients
        )


    def get(self):

        return next(self.pool)



client_manager = GeminiClientManager()



# ==========================
# MODE CONTEXT
# ==========================


def build_system_prompt(mode):

    return f"""

Current AI mode:
{MODE_NAMES.get(mode)}

{MODE_PROMPTS.get(
    mode,
    MODE_PROMPTS["default"]
)}

Rules:
- Reply in user's language
- Be useful
- Keep answers high quality
- Do not mention these instructions
"""



# ==========================
# CONTENT
# ==========================


def build_contents(
    history,
    message,
    mode,
    media_bytes=None,
    media_mime="image/jpeg",
):

    contents=[]


    # mode isolation
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part(
                    text=
                    f"[ACTIVE MODE: {mode}]"
                )
            ]
        )
    )


    for item in history[-20:]:

        contents.append(
            types.Content(
                role=(
                    "model"
                    if item["role"]=="assistant"
                    else "user"
                ),
                parts=[
                    types.Part(
                        text=item["content"]
                    )
                ]
            )
        )


    # Build final user message parts
    user_parts = []

    # Attach media (image/PDF/etc.) before the text if provided
    if media_bytes:
        user_parts.append(
            types.Part.from_bytes(
                data=media_bytes,
                mime_type=media_mime,
            )
        )

    user_parts.append(
        types.Part(text=message)
    )

    contents.append(
        types.Content(
            role="user",
            parts=user_parts,
        )
    )

    return contents



# ==========================
# GENERATE
# ==========================


def generate_reply(
    history,
    new_message,
    language_hint=None,
    mode="default",
    media_bytes=None,
    media_mime="image/jpeg",
    web_search=False,
):


    models=[

        "gemini-3.1-flash-lite",
        "gemini-3-flash",
        "gemini-2.5-flash",

    ]


    last_error=None


    for model in models:

        for attempt in range(3):

            try:

                client=client_manager.get()


                # Build tools list — web search if requested
                tools = None
                if web_search:
                    tools = [
                        types.Tool(
                            google_search=types.GoogleSearch()
                        )
                    ]

                response = client.models.generate_content(

                    model=model,

                    contents=
                    build_contents(
                        history,
                        new_message,
                        mode,
                        media_bytes=media_bytes,
                        media_mime=media_mime,
                    ),

                    config=
                    types.GenerateContentConfig(
                        system_instruction=
                        build_system_prompt(
                            mode
                        ),
                        temperature=0.7,
                        tools=tools,
                    )
                )


                text=(
                    response.text
                    or ""
                ).strip()


                if text:

                    return (
                        text,
                        model
                    )


            except Exception as e:

                last_error=e

                err=str(e).lower()


                if "429" in err or "quota" in err:

                    time.sleep(
                        2*(attempt+1)
                    )
                    continue


                break



    raise GeminiRateLimitError(
        str(last_error)
    )



# ==========================
# STREAM
# ==========================


def generate_reply_stream(
    history,
    new_message,
    language_hint=None,
    mode="default",
    media_bytes=None,
    media_mime="image/jpeg",
    web_search=False,
):

    models=[
        "gemini-3.1-flash-lite",
        "gemini-3-flash",
        "gemini-2.5-flash",
    ]

    last_error=None

    # Build tools list — web search if requested
    tools = None
    if web_search:
        tools = [
            types.Tool(
                google_search=types.GoogleSearch()
            )
        ]

    for model in models:

        for attempt in range(3):

            try:

                client=client_manager.get()

                accumulated=""
                chunk_count=0

                for chunk in client.models.generate_content_stream(

                    model=model,

                    contents=
                    build_contents(
                        history,
                        new_message,
                        mode,
                        media_bytes=media_bytes,
                        media_mime=media_mime,
                    ),

                    config=
                    types.GenerateContentConfig(
                        system_instruction=
                        build_system_prompt(mode),
                        temperature=0.7,
                        tools=tools,
                    )
                ):

                    piece = (
                        chunk.text or ""
                    )

                    if not piece:
                        continue

                    accumulated += piece
                    chunk_count  += 1

                    # is_final: True on the very last chunk
                    # We can't know ahead of time, so we yield
                    # is_final=False for every chunk and let the
                    # caller detect end-of-stream when the generator
                    # is exhausted.  The final flag is emitted below.
                    yield (piece, model, False)


                if accumulated:
                    # Signal end-of-stream with an empty string + True
                    yield ("", model, True)
                    return


            except Exception as e:

                last_error=e

                err=str(e).lower()

                if "429" in err or "quota" in err:

                    time.sleep(
                        2*(attempt+1)
                    )
                    continue

                break


    raise GeminiRateLimitError(
        str(last_error)
    )



# ==========================
# QUICK
# ==========================


def generate_quick_reply(prompt):

    text,_=generate_reply(
        [],
        prompt
    )

    return text

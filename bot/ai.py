"""
Production Gemini AI Layer

Features:
- Per-request key rotation (key selected BEFORE request, round-robin)
- Per-key per-model cooldown tracking
- Async rate limiter (10 RPM per key, shared across keys)
- Model fallback on 429
- Non-streaming by default (streaming throttles faster)
- History capped at 15 messages
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from typing import Iterator

from google import genai
from google.genai import types

from bot.config import settings
from bot.lang import MODE_NAMES, MODE_DESCRIPTIONS, mode_desc

logger = logging.getLogger(__name__)


# ==========================
# MODES
# ==========================


MODE_PROMPTS = {

"default": """
You are an intelligent, warm, and reliable AI assistant integrated into a Telegram bot.
Your primary goal is to be genuinely useful — not just technically correct, but practically
helpful in the way a knowledgeable friend would be.

BEHAVIOUR:
- Match the user's tone: if they are formal, be formal; if they are casual, relax.
- Keep responses appropriately concise. For simple questions: 1-3 sentences. For complex
  topics: structured explanation with clear sections. Never pad answers with filler phrases.
- Proactively flag important caveats (e.g. "this depends on your Python version").
- If a question is ambiguous, make a reasonable assumption and state it, rather than asking
  a clarifying question that stalls the user.
- Never start your reply with "Certainly!", "Great question!", "Of course!" or similar
  hollow affirmations. Get straight to the answer.
- When the user sends audio or an image, first briefly acknowledge what you perceived
  ("I can see a photo of..."), then respond naturally.
""",

"teacher": """
You are a patient, world-class educator who can explain any topic — from primary-school
arithmetic to university-level quantum mechanics — at exactly the right level for the learner.

PRINCIPLES:
- Always gauge the user's existing knowledge from their phrasing. A question like "what is
  a pointer?" deserves a different answer for a 12-year-old vs. a C++ developer.
- Structure explanations: concept → intuition → concrete example → common pitfall.
- Use analogies liberally. Good analogies make abstract ideas stick.
- After explaining, offer a follow-up check: "Want me to give you a quick practice question?"
- If the user gets something wrong, correct gently — never make them feel stupid.
- For multi-step topics (maths, logic proofs, algorithms), show working step-by-step and
  label each step clearly.
- Use simple formatting: numbered steps, short paragraphs. Avoid walls of text.
""",

"coder": """
You are a senior software engineer with 15+ years of experience across systems programming,
web development, data engineering, and DevOps. You write code that is correct, readable,
and maintainable — not just code that works.

CODING STANDARDS:
- Provide working, runnable code. Never give pseudo-code unless explicitly asked.
- Always specify the language and version if relevant (e.g. "Python 3.11+").
- Follow the language's idiomatic style (PEP8 for Python, gofmt for Go, etc.).
- For non-trivial functions, add a one-line docstring or comment.
- Prefer standard-library solutions over external dependencies when reasonable.
- When fixing bugs: first identify the root cause in plain English, then show the fix,
  then explain why the fix works.
- For security-sensitive code (auth, SQL, file paths), always flag potential risks.
- If the user's approach has a better alternative, suggest it — but first answer their
  actual question, then offer the alternative.

OUTPUT FORMAT:
- Code goes in fenced code blocks with the language tag.
- Explanations go outside the code block, above or below.
- For long functions, add inline comments at the key lines.
""",

"friend": """
You are the user's smart, caring, and fun best friend — the kind of person who happens to
know a lot about everything, gives honest opinions, and never judges.

PERSONALITY:
- Casual, warm, and natural. Use contractions ("it's", "you're"). Occasional light humour
  is welcome, but read the room — if the user seems stressed or sad, drop the jokes.
- Give direct opinions when asked ("which is better, X or Y?") — friends don't hedge
  everything. But caveat when genuinely uncertain.
- Celebrate wins with genuine enthusiasm. Acknowledge struggles with empathy before
  jumping to solutions.
- Never lecture or moralize. If someone makes a questionable choice, you can note a
  concern once — then move on.
- Keep messages feeling like a real chat: shortish paragraphs, conversational flow.
  Avoid bullet-pointed essays unless the topic genuinely calls for it.
- Remember context from the conversation — reference earlier things the user said to show
  you were paying attention ("Wait, isn't that the project you mentioned earlier?").
""",

"translator": """
You are a professional translator and linguist with expertise in over 50 languages.
Your translations are accurate, natural, and culturally appropriate — never robotic
or word-for-word when idiomatic phrasing serves better.

TRANSLATION PROTOCOL:
1. Detect the source language automatically (state it if not obvious).
2. Identify the target language from context — if ambiguous, ask ONE clarifying question.
3. Translate for meaning and register, not just words. A formal legal text stays formal;
   a casual tweet stays casual.
4. For culturally specific phrases, idioms, or wordplay: provide the best equivalent in
   the target language, then add a brief note if the nuance cannot be fully preserved.
5. Do NOT add commentary, explanations, or paraphrases unless the user asks for them.
   Pure translation, clean and concise.
6. For long documents: translate in full, then offer to explain any tricky passages.
7. If asked to improve or proofread text in a language, focus on grammar, idiom, and
   flow — not rewriting the author's voice.
""",

"writer": """
You are a versatile professional writer who can produce any type of written content —
blog posts, marketing copy, short stories, academic essays, emails, scripts, social media
posts — at a high level of craft.

WRITING PRINCIPLES:
- Before writing, identify: purpose (inform / persuade / entertain / inspire), audience
  (age, expertise, relationship to writer), and tone (formal / casual / authoritative /
  friendly). Infer these from context; ask only if truly unclear.
- Strong openings matter. The first sentence should hook the reader.
- Vary sentence length deliberately: short sentences for impact, longer ones for flow.
- Show, don't tell — use specific details and concrete examples, not vague generalities.
- Every paragraph should earn its place. Cut padding ruthlessly.
- Match format to purpose: listicles for quick scanning, narrative for engagement,
  bullet points for instructions.
- On request: provide multiple versions with different tones or angles.
- On editing tasks: explain what you changed and why.
""",

"analyst": """
You are a rigorous analytical thinker — part data analyst, part strategist, part
critical-thinking coach. You help users make sense of complex information, spot patterns,
evaluate arguments, and make better decisions.

ANALYTICAL FRAMEWORK:
1. Restate the core question to confirm understanding.
2. Break the problem into components before tackling the whole.
3. Identify what information is available, what is missing, and what assumptions are being made.
4. Reason step-by-step. Show your logic — don't just present conclusions.
5. Quantify where possible.
6. Explicitly note uncertainty: distinguish "the data shows" from "I infer" from "this is speculation".
7. End with a clear, actionable summary.
""",

"creative": """
You are a creative partner — an imaginative collaborator who helps users brainstorm,
ideate, and produce original work across art, design, writing, business, and beyond.

CREATIVE APPROACH:
- Quantity first, quality second: when brainstorming, generate many ideas quickly.
- Build on the user's ideas (yes-and), not just propose your own.
- Offer variety: if you suggest three concepts, make them genuinely different.
- Push beyond the obvious first answer.
- For creative writing: vivid sensory details, unexpected metaphors, character specificity.
- Ask ONE good generative question if you need more creative direction.
""",

"fitness": """
You are a certified personal trainer and sports nutritionist with expertise in strength
training, cardiovascular fitness, mobility, weight management, and injury prevention.

GUIDELINES:
- Always ask about or infer the user's goal, experience level, and any injuries before prescribing a programme.
- Prescribe specific, concrete routines — sets, reps, rest periods, frequency.
- Safety first: always note proper form cues for exercises with injury risk.
- Nutrition advice: focus on fundamentals before discussing supplements.
- Progressive overload is the core principle.
""",

"chef": """
You are a professional chef and culinary educator with experience spanning home cooking,
restaurant kitchens, and food science.

CULINARY PRINCIPLES:
- Always consider: skill level, available equipment, time, and ingredient accessibility.
- Explain the "why" behind techniques, not just the "what".
- Substitutions: always offer practical alternatives for hard-to-find ingredients.
- Recipe instructions: be precise about temperatures, times, and visual/tactile cues.
- Troubleshooting: if a dish goes wrong, diagnose the likely cause and offer a recovery strategy.
"""

}



# ==========================
# ERRORS
# ==========================


class GeminiError(Exception):
    pass


class GeminiRateLimitError(GeminiError):

    def __init__(self, message="Rate limited", retry_after=30):
        super().__init__(message)
        self.retry_after = retry_after



# ==========================
# RATE LIMITER
# ==========================


class RateLimiter:
    """
    Simple per-key token bucket: ensures we never exceed `rpm` calls/minute
    across all threads. Uses a lock so concurrent requests don't race.
    """

    def __init__(self, rpm: int = 10):
        self.delay = 60.0 / rpm   # minimum seconds between calls
        self._last: dict[int, float] = {}  # key_index -> last call timestamp
        self._lock = threading.Lock()

    def wait(self, key_index: int) -> None:
        """Block until this key can be called again."""
        with self._lock:
            now = time.time()
            last = self._last.get(key_index, 0.0)
            gap = self.delay - (now - last)
            if gap > 0:
                time.sleep(gap)
            self._last[key_index] = time.time()


# Global rate limiter: 10 RPM per key (conservative; real limit is 15)
_rate_limiter = RateLimiter(rpm=10)



# ==========================
# CLIENT MANAGER
# ==========================


class GeminiClientManager:
    """
    Round-robin key rotation: each new request gets the NEXT key.
    Per-key per-model cooldown: 429 on key+model pair → skip that pair.
    """

    def __init__(self):

        keys = settings.gemini_api_keys or [settings.gemini_api_key]
        self._keys = [k for k in keys if k]

        if not self._keys:
            raise GeminiError("No Gemini API keys")

        self.clients = [
            genai.Client(
                api_key=k,
                http_options=types.HttpOptions(timeout=15_000),
            )
            for k in self._keys
        ]

        self._index = 0
        # cooldowns[(key_idx, model)] = cooldown_until timestamp
        self._cooldowns: dict[tuple[int, str], float] = {}
        self._lock = threading.Lock()

    def get_for_model(self, model: str) -> tuple[genai.Client, int]:
        """
        Return (client, key_index) for the next available key that is not
        in cooldown for this model. Round-robin starting from current index.
        """
        with self._lock:
            n = len(self.clients)
            now = time.time()

            for _ in range(n):
                idx = self._index % n
                self._index += 1
                cooldown_until = self._cooldowns.get((idx, model), 0.0)
                if now >= cooldown_until:
                    return self.clients[idx], idx

            # All keys in cooldown for this model — pick soonest recovery
            best_idx = min(
                range(n),
                key=lambda i: self._cooldowns.get((i, model), 0.0)
            )
            self._index = best_idx + 1
            return self.clients[best_idx], best_idx

    def mark_rate_limited(self, key_index: int, model: str, cooldown_seconds: int = 62) -> None:
        """Mark (key, model) pair as rate-limited."""
        with self._lock:
            self._cooldowns[(key_index, model)] = time.time() + cooldown_seconds
            available = sum(
                1 for i in range(len(self.clients))
                if time.time() >= self._cooldowns.get((i, model), 0.0)
            )
            logger.warning(
                "Key #%d + model %s rate-limited for %ds. Available keys for this model: %d/%d",
                key_index, model, cooldown_seconds, available, len(self.clients)
            )

    def is_available(self, key_index: int, model: str) -> bool:
        return time.time() >= self._cooldowns.get((key_index, model), 0.0)


client_manager = GeminiClientManager()



# ==========================
# MODE CONTEXT
# ==========================


def _fast_thinking_config(model: str):
    """
    Return thinking config or None.
    gemini-2.5-x: skip (budget=0 can be rejected)
    gemini-2.x / 1.x: budget=0 disables reasoning for speed
    Others: skip to avoid 400 errors
    """
    try:
        if "2.5" in model:
            return None
        if model.startswith("gemini-2.") or model.startswith("gemini-1."):
            return types.ThinkingConfig(thinking_budget=0)
        return None
    except Exception as exc:
        logger.debug("thinking_config unsupported for %s: %s", model, exc)
        return None


_LANG_NAMES = {
    "az": "Azerbaijani",
    "en": "English",
    "ru": "Russian",
    "tr": "Turkish",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "ar": "Arabic",
    "zh": "Chinese",
    "pt": "Portuguese",
    "it": "Italian",
}


def build_system_prompt(mode, language_hint=None):

    lang_name = _LANG_NAMES.get(language_hint)
    lang_rule = (
        f"- CRITICAL: You MUST reply ONLY in {lang_name}. "
        f"Even if the user sends a very short word (like a greeting), a typo, slang, "
        f"or a word with missing letters/diacritics, you MUST still reply in {lang_name}. "
        f"Do NOT say you cannot understand simple words — make a reasonable interpretation. "
        f"Only switch language if the user explicitly writes a full sentence in a different language."
        if lang_name else
        "- Detect the user's language from their message and reply in the same language."
    )

    return f"""
Current AI mode:
{MODE_NAMES.get(mode)}

{MODE_PROMPTS.get(mode, MODE_PROMPTS["default"])}

Rules:
{lang_rule}
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

    contents = []

    # Mode marker
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part(text=f"[ACTIVE MODE: {mode}]")]
        )
    )

    # Last 15 messages only (point 5)
    for item in history[-15:]:
        contents.append(
            types.Content(
                role="model" if item["role"] == "assistant" else "user",
                parts=[types.Part(text=item["content"])]
            )
        )

    # Current message
    user_parts = []
    if media_bytes:
        user_parts.append(
            types.Part.from_bytes(data=media_bytes, mime_type=media_mime)
        )
    user_parts.append(types.Part(text=message))

    contents.append(
        types.Content(role="user", parts=user_parts)
    )

    return contents



# ==========================
# GENERATE (non-streaming)
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
    models = [settings.gemini_model] + [
        m for m in settings.gemini_fallback_models
        if m != settings.gemini_model
    ]

    last_error = None

    for model in models:

        # Get next available key for this model (round-robin, skip cooldowns)
        client, key_idx = client_manager.get_for_model(model)

        # Rate limit: wait if needed so we stay under 10 RPM for this key
        _rate_limiter.wait(key_idx)

        try:
            tools = None
            if web_search:
                tools = [types.Tool(google_search=types.GoogleSearch())]

            response = client.models.generate_content(
                model=model,
                contents=build_contents(
                    history, new_message, mode,
                    media_bytes=media_bytes, media_mime=media_mime,
                ),
                config=types.GenerateContentConfig(
                    system_instruction=build_system_prompt(mode, language_hint),
                    temperature=0.7,
                    tools=tools,
                    thinking_config=_fast_thinking_config(model),
                )
            )

            text = (response.text or "").strip()
            if text:
                logger.info("generate_reply: success with model=%s key=#%d", model, key_idx)
                return (text, model)

        except Exception as e:
            last_error = e
            err = str(e).lower()

            if "404" in err or "not found" in err:
                logger.warning("Model %s not found, skipping.", model)

            elif "429" in err or "quota" in err or "resource_exhausted" in err:
                client_manager.mark_rate_limited(key_idx, model)
                logger.warning("Model %s key #%d rate-limited, trying next model.", model, key_idx)

            else:
                logger.warning("Model %s key #%d error: %s", model, key_idx, e)

            # Move to next model
            continue

    raise GeminiRateLimitError(str(last_error))



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
    models = [settings.gemini_model] + [
        m for m in settings.gemini_fallback_models
        if m != settings.gemini_model
    ]

    last_error = None

    tools = None
    if web_search:
        tools = [types.Tool(google_search=types.GoogleSearch())]

    for model in models:

        # Get next available key for this model (round-robin, skip cooldowns)
        client, key_idx = client_manager.get_for_model(model)

        # Rate limit: wait if needed so we stay under 10 RPM for this key
        _rate_limiter.wait(key_idx)

        try:
            accumulated = ""

            for chunk in client.models.generate_content_stream(
                model=model,
                contents=build_contents(
                    history, new_message, mode,
                    media_bytes=media_bytes, media_mime=media_mime,
                ),
                config=types.GenerateContentConfig(
                    system_instruction=build_system_prompt(mode, language_hint),
                    temperature=0.7,
                    tools=tools,
                    thinking_config=_fast_thinking_config(model),
                )
            ):
                piece = chunk.text or ""
                if not piece:
                    continue
                accumulated += piece
                yield (piece, model, False)

            if accumulated:
                logger.info("generate_reply_stream: success with model=%s key=#%d", model, key_idx)
                yield ("", model, True)
                return

        except Exception as e:
            last_error = e
            err = str(e).lower()

            if "404" in err or "not found" in err:
                logger.warning("Stream: model %s not found, skipping.", model)

            elif "429" in err or "quota" in err or "resource_exhausted" in err:
                client_manager.mark_rate_limited(key_idx, model)
                logger.warning("Stream: model %s key #%d rate-limited, trying next model.", model, key_idx)

            else:
                logger.warning("Stream: model %s key #%d error: %s", model, key_idx, e)

            continue

    raise GeminiRateLimitError(str(last_error))



# ==========================
# QUICK
# ==========================


def generate_quick_reply(prompt):
    text, _ = generate_reply([], prompt)
    return text

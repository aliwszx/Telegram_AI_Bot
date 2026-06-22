"""
Gemini API wrapper with:
- Multi-key rotation + model fallback chain (quota exhausted → next key/model)
- Image, audio, PDF/document support
- Extended chat modes (10 personas)
- Streaming support
- Language-aware responses
"""
from __future__ import annotations

import logging
import re
import time
import threading
from dataclasses import dataclass, field
from typing import Iterator

from google import genai
from google.genai import types

from bot.config import settings
from bot.retry import is_rate_limited, is_transient, is_model_not_found, is_daily_quota_exhausted

logger = logging.getLogger(__name__)

# ── Key/Model rotation state ───────────────────────────────────────────────

@dataclass
class _KeyState:
    api_key: str
    exhausted_models: set[str] = field(default_factory=set)
    exhausted_until: float = 0.0   # RPM gözləmə zamanı

    def is_exhausted(self, model: str) -> bool:
        return model in self.exhausted_models

    def mark_daily_exhausted(self, model: str) -> None:
        self.exhausted_models.add(model)
        logger.warning("Key ...%s: model %s daily quota exhausted — blacklisted for today.", self.api_key[-6:], model)

    def mark_rpm_limited(self, wait_seconds: int) -> None:
        self.exhausted_until = time.monotonic() + wait_seconds

    def is_rpm_cooling(self) -> bool:
        return time.monotonic() < self.exhausted_until


class _RotationManager:
    """
    Thread-safe key/model rotation.
    Strategy:
      1. Try primary model (GEMINI_MODEL) with each key in order.
      2. If all keys exhausted for primary model, move to next fallback model.
      3. Continue through all models × all keys.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._primary_model = settings.gemini_model
        self._fallback_models: list[str] = settings.gemini_fallback_models
        raw_keys = settings.gemini_api_keys or [settings.gemini_api_key]
        self._keys: list[_KeyState] = [_KeyState(api_key=k) for k in raw_keys if k]
        self._clients: dict[str, genai.Client] = {
            k.api_key: genai.Client(api_key=k.api_key) for k in self._keys
        }
        logger.info(
            "RotationManager initialized: %d API key(s), primary model=%s, fallbacks=%s",
            len(self._keys), self._primary_model, self._fallback_models,
        )

    @property
    def _all_models(self) -> list[str]:
        models = [self._primary_model]
        for m in self._fallback_models:
            if m not in models:
                models.append(m)
        return models

    def get_client_and_model(self) -> tuple[genai.Client, str]:
        """Return (client, model) for the first non-exhausted combination."""
        with self._lock:
            for model in self._all_models:
                for key_state in self._keys:
                    if key_state.is_exhausted(model):
                        continue
                    if key_state.is_rpm_cooling():
                        continue
                    client = self._clients[key_state.api_key]
                    logger.debug("Using key ...%s with model %s", key_state.api_key[-6:], model)
                    return client, model

            # Bütün kombinasiyalar RPM-cooling-dədirsə, ən tez qurtaranı seç
            best: tuple[float, genai.Client, str] | None = None
            for model in self._all_models:
                for key_state in self._keys:
                    if key_state.is_exhausted(model):
                        continue
                    wait_until = key_state.exhausted_until
                    if best is None or wait_until < best[0]:
                        best = (wait_until, self._clients[key_state.api_key], model)

            if best:
                wait_time = max(0.0, best[0] - time.monotonic())
                if wait_time > 0:
                    logger.warning("All keys RPM-cooling. Sleeping %.1fs for best available.", wait_time)
                    time.sleep(wait_time)
                return best[1], best[2]

            raise GeminiRateLimitError("All API keys and models are daily-quota exhausted.")

    def mark_daily_exhausted(self, client: genai.Client, model: str) -> None:
        with self._lock:
            for key_state in self._keys:
                if self._clients[key_state.api_key] is client:
                    key_state.mark_daily_exhausted(model)
                    return

    def mark_rpm_limited(self, client: genai.Client, wait_seconds: int) -> None:
        with self._lock:
            for key_state in self._keys:
                if self._clients[key_state.api_key] is client:
                    key_state.mark_rpm_limited(wait_seconds)
                    return


_rotation = _RotationManager()

# ── RPM retry config ────────────────────────────────────────────────────────
_RPM_RETRY_WAIT = 65
_RPM_MAX_RETRIES = 3

# ── Chat mode system prompts ───────────────────────────────────────────────

MODE_PROMPTS: dict[str, str] = {
    "default": (
        "You are a helpful, friendly AI assistant inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Keep answers concise, clear and well-structured. "
        "Use emojis sparingly to make responses more readable."
    ),
    "teacher": (
        "You are a patient, encouraging teacher inside a Telegram bot. "
        "Explain concepts step by step with simple examples and analogies. "
        "Always reply in the same language the user used. "
        "Check for understanding, use bullet points for clarity. Make learning fun and engaging!"
    ),
    "coder": (
        "You are an expert senior software engineer inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Give practical, working code with brief explanations. "
        "Prefer concise, idiomatic solutions. Highlight edge cases, security concerns, "
        "and performance implications. Use code blocks for all code snippets."
    ),
    "friend": (
        "You are a warm, empathetic close friend chatting on Telegram. "
        "Always reply in the same language the user used. "
        "Be casual, fun, supportive. Use conversational language, "
        "show genuine interest and care. Keep it light and natural — like texting."
    ),
    "translator": (
        "You are a professional multilingual translator inside a Telegram bot. "
        "When the user sends text, detect the source language and translate it. "
        "If no target language specified: if text is English → translate to Azerbaijani, "
        "otherwise → translate to English. "
        "Format: 🔤 [Source lang] → [Target lang]\n[Translation]\n\n💡 [Brief cultural note if relevant]"
    ),
    "lawyer": (
        "You are an experienced legal advisor inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Provide clear, practical legal information. Always note that this is general "
        "information and not a substitute for professional legal advice. "
        "Reference relevant laws when possible. Be thorough but accessible."
    ),
    "doctor": (
        "You are a knowledgeable medical information assistant inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Provide accurate health information clearly and compassionately. "
        "ALWAYS recommend consulting a real doctor for diagnosis/treatment. "
        "Never diagnose. Focus on symptoms, general information, and when to seek care."
    ),
    "psychologist": (
        "You are a compassionate, professional psychologist assistant inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Listen actively, validate feelings, and offer evidence-based coping strategies. "
        "Be warm, non-judgmental, and supportive. "
        "For serious mental health concerns, always encourage professional help. "
        "Never provide diagnosis."
    ),
    "chef": (
        "You are a creative, professional chef and culinary expert inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Share recipes with clear steps, ingredient measurements, cooking tips, and variations. "
        "Include cooking time, difficulty level, and serving size. "
        "Suggest substitutions for dietary restrictions when relevant."
    ),
    "fitness": (
        "You are a certified personal trainer and nutrition expert inside a Telegram bot. "
        "Always reply in the same language the user used. "
        "Provide safe, effective workout plans and nutrition advice tailored to goals. "
        "Always emphasize proper form to prevent injury. "
        "Remind users to consult healthcare providers before starting new exercise programs."
    ),
}

MODE_NAMES = {
    "default":      "🤖 Standart",
    "teacher":      "📚 Müəllim",
    "coder":        "💻 Proqramçı",
    "friend":       "😊 Dost",
    "translator":   "🌐 Tərcüməçi",
    "lawyer":       "⚖️ Hüquqçu",
    "doctor":       "🏥 Həkim",
    "psychologist": "🧠 Psixoloq",
    "chef":         "👨‍🍳 Aşpaz",
    "fitness":      "💪 Fitnes",
}

MODE_DESCRIPTIONS = {
    "default":      "Ümumi köməkçi",
    "teacher":      "Addım-addım izahat",
    "coder":        "Kod və texnologiya",
    "friend":       "Mehriban söhbət",
    "translator":   "Dil tərcüməsi",
    "lawyer":       "Hüquqi məsləhət",
    "doctor":       "Tibbi məlumat",
    "psychologist": "Psixoloji dəstək",
    "chef":         "Resept və kulinariya",
    "fitness":      "İdman və sağlamlıq",
}


# ── Helpers ────────────────────────────────────────────────────────────────

def _to_gemini_role(role: str) -> str:
    return "model" if role == "assistant" else "user"


def _build_contents(
    history: list[dict],
    new_message: str,
    media_bytes: bytes | None = None,
    media_mime: str = "image/jpeg",
) -> list[types.Content]:
    contents: list[types.Content] = []

    for msg in history:
        contents.append(
            types.Content(
                role=_to_gemini_role(msg["role"]),
                parts=[types.Part(text=msg["content"])],
            )
        )

    user_parts: list[types.Part] = []
    if media_bytes:
        user_parts.append(
            types.Part(inline_data=types.Blob(mime_type=media_mime, data=media_bytes))
        )
    if new_message:
        user_parts.append(types.Part(text=new_message))

    if user_parts:
        contents.append(types.Content(role="user", parts=user_parts))

    return contents


def _build_system_prompt(mode: str, language_hint: str | None = None) -> str:
    base = MODE_PROMPTS.get(mode, MODE_PROMPTS["default"])
    if language_hint:
        base += (
            f"\n\n(Context: user's Telegram app language is '{language_hint}'. "
            "Use this only to disambiguate short/ambiguous messages — always "
            "prioritize the actual language the user is writing in.)"
        )
    return base


def _build_config(system_instruction: str, web_search: bool) -> types.GenerateContentConfig:
    tools = [types.Tool(google_search=types.GoogleSearch())] if web_search else None
    return types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=tools,
    )


def _parse_retry_after(exc: Exception | None, default: int = 30) -> int:
    if exc is None:
        return default
    match = re.search(r"retry[_-]?delay['\"]?\s*[:=]\s*['\"]?(\d+)", str(exc), re.IGNORECASE)
    if not match:
        match = re.search(r"(\d+)\s*s(?:ec(?:ond)?s?)?\b", str(exc), re.IGNORECASE)
    if match:
        try:
            seconds = int(match.group(1))
            if 0 < seconds <= 600:
                return seconds
        except ValueError:
            pass
    return default


# ── Main generation functions ──────────────────────────────────────────────

def generate_reply(
    history: list[dict],
    new_message: str,
    language_hint: str | None = None,
    mode: str = "default",
    media_bytes: bytes | None = None,
    media_mime: str = "image/jpeg",
    web_search: bool = False,
) -> tuple[str, str]:
    """
    Call Gemini with automatic key rotation and model fallback.
    Returns: (reply_text, model_used)
    """
    contents = _build_contents(history, new_message, media_bytes, media_mime)
    system_instruction = _build_system_prompt(mode, language_hint)
    config = _build_config(system_instruction, web_search)

    rpm_retries = 0
    transient_attempts = 0
    attempted: set[tuple[str, str]] = set()  # (key_suffix, model) cütlükləri

    while True:
        client, model = _rotation.get_client_and_model()
        key_id = id(client)

        # Eyni kombinasiyanı iki dəfə cəhd etmə (sonsuz döngüdən qorun)
        combo = (str(key_id), model)
        if combo in attempted:
            raise GeminiRateLimitError("All API key / model combinations exhausted.")
        attempted.add(combo)

        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
            text = (response.text or "").strip()
            if not text:
                raise GeminiError("Empty response from Gemini")
            if model != settings.gemini_model:
                logger.info("Fallback model used: %s", model)
            return text, model

        except GeminiError:
            raise

        except Exception as exc:  # noqa: BLE001
            if is_rate_limited(exc):
                if is_daily_quota_exhausted(exc):
                    _rotation.mark_daily_exhausted(client, model)
                    # Fərqli key/model kombinasiyasını cəhd et
                    continue

                # RPM — qısa müddət gözlə, eyni key ilə yenidən cəhd et
                if rpm_retries < _RPM_MAX_RETRIES:
                    rpm_retries += 1
                    wait = _parse_retry_after(exc, default=_RPM_RETRY_WAIT)
                    logger.warning("RPM rate-limit (retry %s/%s), waiting %ss: %s", rpm_retries, _RPM_MAX_RETRIES, wait, exc)
                    _rotation.mark_rpm_limited(client, wait)
                    attempted.discard(combo)  # bu kombinasiyanı yenidən cəhd etməyə icazə ver
                    continue

                # RPM retryları bitdi — bu keyə daily-exhausted kimi bax
                _rotation.mark_daily_exhausted(client, model)
                continue

            if is_model_not_found(exc):
                logger.error("Model %s not found, skipping: %s", model, exc)
                _rotation.mark_daily_exhausted(client, model)
                continue

            if is_transient(exc):
                if transient_attempts < 2:
                    transient_attempts += 1
                    delay = min(4.0, 0.5 * (2 ** (transient_attempts - 1)))
                    logger.warning("Transient error (attempt %s), retrying in %.1fs: %s", transient_attempts, delay, exc)
                    time.sleep(delay)
                    attempted.discard(combo)
                    continue

            raise GeminiError(str(exc)) from exc


def generate_reply_stream(
    history: list[dict],
    new_message: str,
    language_hint: str | None = None,
    mode: str = "default",
    media_bytes: bytes | None = None,
    media_mime: str = "image/jpeg",
    web_search: bool = False,
) -> Iterator[tuple[str, str, bool]]:
    """
    Streaming version. Yields (text_piece, model, is_done) tuples.
    Key rotation + model fallback on daily quota exhaustion.
    """
    contents = _build_contents(history, new_message, media_bytes, media_mime)
    system_instruction = _build_system_prompt(mode, language_hint)
    config = _build_config(system_instruction, web_search)

    rpm_retries = 0
    transient_attempts = 0
    attempted: set[tuple[str, str]] = set()

    while True:
        client, model = _rotation.get_client_and_model()
        key_id = id(client)

        combo = (str(key_id), model)
        if combo in attempted:
            raise GeminiRateLimitError("All API key / model combinations exhausted.")
        attempted.add(combo)

        started = False
        full_text = ""
        try:
            stream = client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=config,
            )
            for chunk in stream:
                piece = getattr(chunk, "text", None) or ""
                if piece:
                    started = True
                    full_text += piece
                    yield piece, model, False

            if not full_text.strip():
                raise GeminiError("Empty response from Gemini")

            if model != settings.gemini_model:
                logger.info("Fallback model used (stream): %s", model)
            yield "", model, True
            return

        except GeminiError:
            raise

        except Exception as exc:  # noqa: BLE001
            if started:
                # Artıq cavab göndərməyə başlamışıq — indi dəyişmək olmaz
                raise GeminiError(str(exc)) from exc

            if is_rate_limited(exc):
                if is_daily_quota_exhausted(exc):
                    _rotation.mark_daily_exhausted(client, model)
                    continue

                if rpm_retries < _RPM_MAX_RETRIES:
                    rpm_retries += 1
                    wait = _parse_retry_after(exc, default=_RPM_RETRY_WAIT)
                    logger.warning("RPM rate-limit stream (retry %s/%s), waiting %ss: %s", rpm_retries, _RPM_MAX_RETRIES, wait, exc)
                    _rotation.mark_rpm_limited(client, wait)
                    attempted.discard(combo)
                    continue

                _rotation.mark_daily_exhausted(client, model)
                continue

            if is_model_not_found(exc):
                logger.error("Model %s not found (stream), skipping: %s", model, exc)
                _rotation.mark_daily_exhausted(client, model)
                continue

            if is_transient(exc):
                if transient_attempts < 2:
                    transient_attempts += 1
                    delay = min(4.0, 0.5 * (2 ** (transient_attempts - 1)))
                    logger.warning("Transient stream error (attempt %s), retrying in %.1fs: %s", transient_attempts, delay, exc)
                    time.sleep(delay)
                    attempted.discard(combo)
                    continue

            raise GeminiError(str(exc)) from exc


def generate_quick_reply(prompt: str) -> str:
    """Single-shot generation for inline mode and quick tasks. No history."""
    client, model = _rotation.get_client_and_model()
    try:
        response = client.models.generate_content(
            model=model,
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(
                system_instruction=MODE_PROMPTS["default"],
            ),
        )
        return (response.text or "").strip()
    except Exception as exc:
        raise GeminiError(str(exc)) from exc


# ── Exceptions ─────────────────────────────────────────────────────────────

class GeminiError(Exception):
    """Raised when the Gemini API call fails or returns nothing usable."""


class GeminiRateLimitError(GeminiError):
    """Raised when all keys/models are rate-limited or quota exhausted."""

    def __init__(self, message: str, retry_after: int = 30) -> None:
        super().__init__(message)
        self.retry_after = retry_after

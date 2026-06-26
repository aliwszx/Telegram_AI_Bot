"""
Central configuration — environment variables (.env locally, real env on Render).
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def _get_bool(name: str, default: bool = True) -> bool:
    val = os.getenv(name, "").lower()
    if val in ("false", "0", "no"):
        return False
    if val in ("true", "1", "yes"):
        return True
    return default


def _get_list(name: str) -> list[int]:
    raw = os.getenv(name, "")
    result: list[int] = []
    for x in raw.split(","):
        x = x.strip()
        if not x:
            continue
        if not x.lstrip("-").isdigit():
            print(f"[config] WARNING: ignoring invalid {name} entry '{x}'")
            continue
        result.append(int(x))
    return result


def _get_api_keys() -> list[str]:
    """
    Çoxlu Gemini API key dəstəyi.
    GEMINI_API_KEY_1, GEMINI_API_KEY_2, ... və ya vergüllə ayrılmış GEMINI_API_KEYS.
    Əgər heç biri yoxdursa, köhnə GEMINI_API_KEY istifadə olunur.
    """
    # Vergüllə ayrılmış format: GEMINI_API_KEYS=key1,key2,key3
    multi = os.getenv("GEMINI_API_KEYS", "")
    if multi:
        keys = [k.strip() for k in multi.split(",") if k.strip()]
        if keys:
            return keys

    # Nömrəli format: GEMINI_API_KEY_1, GEMINI_API_KEY_2, ...
    numbered: list[str] = []
    for i in range(1, 20):
        k = os.getenv(f"GEMINI_API_KEY_{i}", "")
        if k:
            numbered.append(k)
    if numbered:
        return numbered

    # Köhnə tək key formatı
    single = os.getenv("GEMINI_API_KEY", "")
    return [single] if single else []


def _get_fallback_models() -> list[str]:
    """
    Fallback model zənciri.
    GEMINI_FALLBACK_MODELS=gemini-2.0-flash-lite,gemini-1.5-flash-8b,gemini-1.5-flash
    Əgər yoxdursa, default zəncir istifadə olunur.
    """
    raw = os.getenv("GEMINI_FALLBACK_MODELS", "")
    if raw:
        models = [m.strip() for m in raw.split(",") if m.strip()]
        if models:
            return models
    # Default fallback zənciri (free tier-də mövcud modellər, 2026)
    return [
        "gemini-3.5-flash",
        "gemini-3-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
    ]


@dataclass(frozen=True)
class Settings:
    # ── Telegram ───────────────────────────────────────────────────────────
    bot_token: str = os.getenv("BOT_TOKEN", "")

    # ── Gemini ─────────────────────────────────────────────────────────────
    # Köhnə tək key (geriyə uyğunluq üçün)
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

    # Çoxlu key və fallback model dəstəyi
    gemini_api_keys: list[str] = field(default_factory=_get_api_keys)
    gemini_fallback_models: list[str] = field(default_factory=_get_fallback_models)

    # ── Supabase ───────────────────────────────────────────────────────────
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    # ── Limits ─────────────────────────────────────────────────────────────
    history_limit: int = field(default_factory=lambda: _get_int("HISTORY_LIMIT", 15))
    free_daily_limit: int = field(default_factory=lambda: _get_int("FREE_DAILY_LIMIT", 20))
    premium_daily_limit: int = field(default_factory=lambda: _get_int("PREMIUM_DAILY_LIMIT", 500))

    # ── Payment ────────────────────────────────────────────────────────────
    stars_price: int = field(default_factory=lambda: _get_int("STARS_PRICE", 100))
    premium_duration_days: int = field(default_factory=lambda: _get_int("PREMIUM_DURATION_DAYS", 30))

    # ── Admins ─────────────────────────────────────────────────────────────
    admin_ids: list[int] = field(default_factory=lambda: _get_list("ADMIN_IDS"))

    # ── Webhook ────────────────────────────────────────────────────────────
    webhook_base_url: str = os.getenv("WEBHOOK_BASE_URL", "")
    webhook_path: str = os.getenv("WEBHOOK_PATH", "/webhook")
    port: int = field(default_factory=lambda: _get_int("PORT", 10000))

    # ── Sentry ─────────────────────────────────────────────────────────────
    sentry_dsn: str = os.getenv("SENTRY_DSN", "")
    sentry_environment: str = os.getenv("SENTRY_ENVIRONMENT", "production")

    # ── Feature flags ──────────────────────────────────────────────────────
    streaming_enabled: bool = field(default_factory=lambda: _get_bool("STREAMING_ENABLED", True))
    inline_mode_enabled: bool = field(default_factory=lambda: _get_bool("INLINE_MODE_ENABLED", True))
    premium_expiry_warning_days: int = field(default_factory=lambda: _get_int("PREMIUM_EXPIRY_WARNING_DAYS", 3))

    def validate(self, webhook_mode: bool = False) -> None:
        # Ən az bir API key olmalıdır
        if not self.gemini_api_keys and not self.gemini_api_key:
            raise RuntimeError(
                "Heç bir Gemini API key tapılmadı. "
                "GEMINI_API_KEY, GEMINI_API_KEYS, və ya GEMINI_API_KEY_1 mühit dəyişənini təyin edin."
            )

        missing = [
            name
            for name, value in [
                ("BOT_TOKEN", self.bot_token),
                ("SUPABASE_URL", self.supabase_url),
                ("SUPABASE_KEY", self.supabase_key),
            ]
            if not value
        ]
        if webhook_mode and not self.webhook_base_url:
            missing.append("WEBHOOK_BASE_URL")

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Check your .env file or Render environment settings."
            )


settings = Settings()

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


@dataclass(frozen=True)
class Settings:
    # ── Telegram ───────────────────────────────────────────────────────────
    bot_token: str = os.getenv("BOT_TOKEN", "")

    # ── Gemini ─────────────────────────────────────────────────────────────
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

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

    def validate(self) -> None:
        missing = [
            name
            for name, value in [
                ("BOT_TOKEN", self.bot_token),
                ("GEMINI_API_KEY", self.gemini_api_key),
                ("SUPABASE_URL", self.supabase_url),
                ("SUPABASE_KEY", self.supabase_key),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Check your .env file or Render environment settings."
            )


settings = Settings()

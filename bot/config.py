"""
Central configuration loaded from environment variables (.env in local dev,
real environment variables on Render).
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def _get_list(name: str) -> list[int]:
    raw = os.getenv(name, "")
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


@dataclass(frozen=True)
class Settings:
    # Telegram
    bot_token: str = os.getenv("BOT_TOKEN", "")

    # Gemini
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
    gemini_system_prompt: str = os.getenv(
        "GEMINI_SYSTEM_PROMPT",
        "You are a helpful, friendly AI assistant inside a Telegram bot. "
        "Always reply in the same language the user used in their message. "
        "If a message is too short or ambiguous to confidently detect the "
        "language on its own (e.g. a one-word greeting that looks similar "
        "across several Turkic languages like Azerbaijani, Uzbek, Turkish), "
        "use the user's Telegram app language hint, if provided, to decide. "
        "Keep answers concise and clear.",
    )

    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    # Limits
    history_limit: int = field(default_factory=lambda: _get_int("HISTORY_LIMIT", 10))
    free_daily_limit: int = field(default_factory=lambda: _get_int("FREE_DAILY_LIMIT", 20))
    premium_daily_limit: int = field(default_factory=lambda: _get_int("PREMIUM_DAILY_LIMIT", 300))

    # Telegram Stars payment (currency code "XTR", no provider token needed)
    stars_price: int = field(default_factory=lambda: _get_int("STARS_PRICE", 100))
    premium_duration_days: int = field(default_factory=lambda: _get_int("PREMIUM_DURATION_DAYS", 30))

    # Admins
    admin_ids: list[int] = field(default_factory=lambda: _get_list("ADMIN_IDS"))

    # Webhook (optional deployment mode)
    webhook_base_url: str = os.getenv("WEBHOOK_BASE_URL", "")
    webhook_path: str = os.getenv("WEBHOOK_PATH", "/webhook")
    port: int = field(default_factory=lambda: _get_int("PORT", 10000))

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

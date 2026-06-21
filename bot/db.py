"""
Database access layer.

All Supabase calls are synchronous (supabase-py v2 uses httpx under the hood
but exposes a blocking API), so every function here is wrapped with
asyncio.to_thread when called from async handlers. Keep that wrapping in
handlers.py / call sites, not here, so this module stays simple and testable.
"""
from __future__ import annotations

import datetime as dt
from typing import Literal

from supabase import create_client, Client

from bot.config import settings

Plan = Literal["free", "premium"]

_client: Client = create_client(settings.supabase_url, settings.supabase_key)


def _today() -> str:
    return dt.date.today().isoformat()


def today() -> str:
    """Public helper, e.g. for comparing last_usage_date in handlers."""
    return _today()


def get_or_create_user(user_id: int, username: str | None, first_name: str | None) -> dict:
    """Return the user row, creating it with default 'free' plan if missing."""
    existing = _client.table("users").select("*").eq("id", user_id).execute()
    if existing.data:
        # Keep username/first_name fresh in case they changed
        _client.table("users").update(
            {"username": username, "first_name": first_name}
        ).eq("id", user_id).execute()
        return existing.data[0]

    new_row = {
        "id": user_id,
        "username": username,
        "first_name": first_name,
        "plan": "free",
        "daily_usage": 0,
        "last_usage_date": _today(),
    }
    result = _client.table("users").insert(new_row).execute()
    return result.data[0]


def get_user(user_id: int) -> dict | None:
    result = _client.table("users").select("*").eq("id", user_id).execute()
    return result.data[0] if result.data else None


def get_daily_limit(plan: Plan) -> int:
    return settings.premium_daily_limit if plan == "premium" else settings.free_daily_limit


def check_and_increment_usage(user_id: int) -> tuple[bool, int, int]:
    """
    Atomically (best-effort) checks the user's daily usage against their plan
    limit, resetting the counter if the day has rolled over, and increments
    usage if allowed.

    Returns: (allowed, remaining_after_this_message, limit)
    """
    user = get_user(user_id)
    if user is None:
        # Should not happen if get_or_create_user was called first, but be safe.
        user = get_or_create_user(user_id, None, None)

    plan: Plan = user.get("plan", "free")
    limit = get_daily_limit(plan)

    today = _today()
    usage = user.get("daily_usage", 0)
    if user.get("last_usage_date") != today:
        usage = 0  # new day, reset

    if usage >= limit:
        # Persist the reset even if we deny, so the date stays current
        _client.table("users").update(
            {"daily_usage": usage, "last_usage_date": today}
        ).eq("id", user_id).execute()
        return False, 0, limit

    usage += 1
    _client.table("users").update(
        {"daily_usage": usage, "last_usage_date": today}
    ).eq("id", user_id).execute()

    return True, max(limit - usage, 0), limit


def set_plan(user_id: int, plan: Plan) -> None:
    _client.table("users").update({"plan": plan}).eq("id", user_id).execute()


def save_message(user_id: int, role: Literal["user", "assistant"], content: str) -> None:
    _client.table("messages").insert(
        {"user_id": user_id, "role": role, "content": content}
    ).execute()


def get_recent_messages(user_id: int, limit: int | None = None) -> list[dict]:
    """Return the last N messages for a user in chronological (oldest-first) order."""
    limit = limit or settings.history_limit
    result = (
        _client.table("messages")
        .select("role, content, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return list(reversed(result.data))

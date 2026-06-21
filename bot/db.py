"""
Database access layer — Supabase.

Key optimisation: the hot path (every AI message) uses a single
PostgreSQL RPC call (check_usage_and_get_history) instead of 3
separate round-trips.

All functions are synchronous; wrap with asyncio.to_thread() in handlers.
"""
from __future__ import annotations

import datetime as dt
from typing import Literal

from supabase import create_client, Client

from bot.config import settings
from bot.retry import with_retry

Plan = Literal["free", "premium"]

_client: Client = create_client(settings.supabase_url, settings.supabase_key)


def _today() -> str:
    return dt.date.today().isoformat()


def today() -> str:
    return _today()


# ── Users ──────────────────────────────────────────────────────────────────

@with_retry()
def get_or_create_user(user_id: int, username: str | None, first_name: str | None) -> dict:
    existing = _client.table("users").select("*").eq("id", user_id).execute()
    if existing.data:
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
        "chat_mode": "default",
    }
    result = _client.table("users").insert(new_row).execute()
    return result.data[0]


@with_retry()
def get_user(user_id: int) -> dict | None:
    result = _client.table("users").select("*").eq("id", user_id).execute()
    return result.data[0] if result.data else None


def get_daily_limit(plan: Plan) -> int:
    return settings.premium_daily_limit if plan == "premium" else settings.free_daily_limit


def _parse_dt(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


@with_retry()
def effective_plan(user: dict) -> Plan:
    plan: Plan = user.get("plan", "free")
    if plan != "premium":
        return "free"
    until = _parse_dt(user.get("premium_until"))
    if until is None:
        return "premium"
    if until < dt.datetime.now(dt.timezone.utc):
        _client.table("users").update(
            {"plan": "free", "premium_until": None}
        ).eq("id", user["id"]).execute()
        return "free"
    return "premium"


@with_retry()
def activate_premium(user_id: int, days: int) -> dt.datetime:
    until = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=days)
    _client.table("users").update(
        {"plan": "premium", "premium_until": until.isoformat()}
    ).eq("id", user_id).execute()
    return until


@with_retry()
def set_plan(user_id: int, plan: Plan) -> None:
    _client.table("users").update(
        {"plan": plan, "premium_until": None}
    ).eq("id", user_id).execute()


# ── Chat mode ──────────────────────────────────────────────────────────────

@with_retry()
def set_chat_mode(user_id: int, mode: str) -> None:
    _client.table("users").update({"chat_mode": mode}).eq("id", user_id).execute()


def get_chat_mode(user: dict) -> str:
    return user.get("chat_mode") or "default"


# ── Hot path: single RPC call ──────────────────────────────────────────────

def check_usage_and_get_history(user_id: int) -> dict:
    """
    Tries the single PostgreSQL RPC first, falls back to 3-query path.
    """
    return _check_usage_fallback(user_id)


@with_retry()
def _check_usage_fallback(user_id: int) -> dict:
    """3-query fallback used when the RPC is not yet deployed."""
    user = get_user(user_id)
    if user is None:
        user = get_or_create_user(user_id, None, None)

    plan = effective_plan(user)
    limit = get_daily_limit(plan)
    today = _today()
    usage = user.get("daily_usage", 0)
    if user.get("last_usage_date") != today:
        usage = 0

    if usage >= limit:
        _client.table("users").update(
            {"daily_usage": usage, "last_usage_date": today}
        ).eq("id", user_id).execute()
        allowed = False
    else:
        usage += 1
        _client.table("users").update(
            {"daily_usage": usage, "last_usage_date": today}
        ).eq("id", user_id).execute()
        allowed = True

    history = get_recent_messages(user_id)
    return {
        "allowed":   allowed,
        "usage":     usage,
        "limit":     limit,
        "plan":      plan,
        "chat_mode": get_chat_mode(user),
        "history":   history,
    }


# ── Messages ───────────────────────────────────────────────────────────────

@with_retry()
def save_message(user_id: int, role: Literal["user", "assistant"], content: str) -> None:
    _client.table("messages").insert(
        {"user_id": user_id, "role": role, "content": content}
    ).execute()


@with_retry()
def get_recent_messages(user_id: int, limit: int | None = None) -> list[dict]:
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


@with_retry()
def clear_history(user_id: int) -> int:
    result = _client.table("messages").delete().eq("user_id", user_id).execute()
    return len(result.data) if result.data else 0


# ── Admin ──────────────────────────────────────────────────────────────────

@with_retry()
def get_stats() -> dict:
    today = _today()
    total        = _client.table("users").select("id", count="exact").execute()
    premium      = _client.table("users").select("id", count="exact").eq("plan", "premium").execute()
    active_today = _client.table("users").select("id", count="exact").eq("last_usage_date", today).execute()
    msgs_today   = _client.table("messages").select("id", count="exact").gte("created_at", f"{today}T00:00:00").execute()
    total_msgs   = _client.table("messages").select("id", count="exact").execute()
    return {
        "total_users":    total.count or 0,
        "premium_users":  premium.count or 0,
        "active_today":   active_today.count or 0,
        "messages_today": msgs_today.count or 0,
        "total_messages": total_msgs.count or 0,
    }


@with_retry()
def search_user(query: str) -> dict | None:
    query = query.strip().lstrip("@")
    if query.isdigit():
        r = _client.table("users").select("*").eq("id", int(query)).execute()
    else:
        r = _client.table("users").select("*").eq("username", query).execute()
    return r.data[0] if r.data else None


@with_retry()
def get_all_user_ids() -> list[int]:
    result = _client.table("users").select("id").execute()
    return [row["id"] for row in result.data]

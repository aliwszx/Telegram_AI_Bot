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

Plan = Literal["free", "premium"]

_client: Client = create_client(settings.supabase_url, settings.supabase_key)


def _today() -> str:
    return dt.date.today().isoformat()


def today() -> str:
    return _today()


# ── Users ──────────────────────────────────────────────────────────────────

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


def activate_premium(user_id: int, days: int) -> dt.datetime:
    until = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=days)
    _client.table("users").update(
        {"plan": "premium", "premium_until": until.isoformat()}
    ).eq("id", user_id).execute()
    return until


def set_plan(user_id: int, plan: Plan) -> None:
    _client.table("users").update(
        {"plan": plan, "premium_until": None}
    ).eq("id", user_id).execute()


# ── Chat mode ──────────────────────────────────────────────────────────────

def set_chat_mode(user_id: int, mode: str) -> None:
    _client.table("users").update({"chat_mode": mode}).eq("id", user_id).execute()


def get_chat_mode(user: dict) -> str:
    return user.get("chat_mode") or "default"


# ── Hot path: single RPC call ──────────────────────────────────────────────

def check_usage_and_get_history(user_id: int) -> dict:
    """
    Single PostgreSQL RPC replaces 3 separate queries:
      1. get_user (to check plan & usage)
      2. increment daily_usage
      3. get_recent_messages

    Returns dict with keys:
      allowed   bool
      usage     int
      limit     int
      plan      str
      chat_mode str
      history   list[dict]  — [{role, content, created_at}, ...]
    """
    try:
        result = _client.rpc(
            "check_usage_and_get_history",
            {
                "p_user_id":    user_id,
                "p_free_limit": settings.free_daily_limit,
                "p_prem_limit": settings.premium_daily_limit,
                "p_hist_limit": settings.history_limit,
            },
        ).execute()
        data = result.data
        if isinstance(data, list):
            data = data[0]
        history = data.get("history") or []
        if isinstance(history, str):
            import json
            history = json.loads(history)
        data["history"] = list(reversed(history)) if history else []
        return data
    except Exception as exc:
        # RPC not yet deployed → fallback to 3-query path
        import logging
        logging.getLogger(__name__).warning(
            "RPC check_usage_and_get_history failed (%s), using fallback", exc
        )
        return _check_usage_fallback(user_id)


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

def save_message(user_id: int, role: Literal["user", "assistant"], content: str) -> None:
    _client.table("messages").insert(
        {"user_id": user_id, "role": role, "content": content}
    ).execute()


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


def clear_history(user_id: int) -> int:
    result = _client.table("messages").delete().eq("user_id", user_id).execute()
    return len(result.data) if result.data else 0


# ── Admin ──────────────────────────────────────────────────────────────────

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


def search_user(query: str) -> dict | None:
    query = query.strip().lstrip("@")
    if query.isdigit():
        r = _client.table("users").select("*").eq("id", int(query)).execute()
    else:
        r = _client.table("users").select("*").eq("username", query).execute()
    return r.data[0] if r.data else None


def get_all_user_ids() -> list[int]:
    result = _client.table("users").select("id").execute()
    return [row["id"] for row in result.data]

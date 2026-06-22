"""
Database access layer — Supabase.

Optimised hot path: single PostgreSQL RPC call per AI message.
New features: conversation topics, revenue tracking, premium expiry warnings.
"""
from __future__ import annotations

import datetime as dt
import logging
from typing import Literal

logger = logging.getLogger(__name__)

from supabase import create_client, Client

from bot.config import settings
from bot.retry import with_retry

Plan = Literal["free", "premium"]

_client: Client = create_client(settings.supabase_url, settings.supabase_key)


def today() -> str:
    return dt.date.today().isoformat()


# Internal alias used within this module
_today = today


# ── Users ──────────────────────────────────────────────────────────────────

@with_retry()
def get_or_create_user(
    user_id: int,
    username: str | None,
    first_name: str | None,
    referred_by: int | None = None,
) -> dict:
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
        "language_code": None,
    }
    if referred_by and referred_by != user_id:
        ref_row = get_user(referred_by)
        if ref_row is not None:
            new_row["referred_by"] = referred_by

    result = _client.table("users").insert(new_row).execute()
    created = result.data[0]

    if new_row.get("referred_by"):
        try:
            add_bonus_messages(referred_by, 5)
            add_bonus_messages(user_id, 5)
            _client.table("users").update(
                {"referral_count": (ref_row.get("referral_count", 0) or 0) + 1}
            ).eq("id", referred_by).execute()
        except Exception:  # noqa: BLE001
            pass

    return created


@with_retry()
def get_user(user_id: int) -> dict | None:
    result = _client.table("users").select("*").eq("id", user_id).execute()
    return result.data[0] if result.data else None


@with_retry()
def update_user_language(user_id: int, language_code: str | None) -> None:
    if language_code:
        _client.table("users").update(
            {"language_code": language_code}
        ).eq("id", user_id).execute()


@with_retry()
def add_bonus_messages(user_id: int, amount: int) -> None:
    user = get_user(user_id)
    if user is None:
        return
    current = user.get("bonus_messages", 0) or 0
    _client.table("users").update(
        {"bonus_messages": current + amount}
    ).eq("id", user_id).execute()


def get_daily_limit(plan: Plan, bonus: int = 0) -> int:
    base = settings.premium_daily_limit if plan == "premium" else settings.free_daily_limit
    return base + max(bonus, 0)


def get_web_search_enabled(user: dict) -> bool:
    return user.get("web_search", False)


@with_retry()
def set_web_search(user_id: int, enabled: bool) -> None:
    _client.table("users").update({"web_search": enabled}).eq("id", user_id).execute()


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


def days_until_premium_expires(user: dict) -> int | None:
    """Returns number of days until premium expires, or None if not premium / no expiry."""
    if user.get("plan") != "premium":
        return None
    until = _parse_dt(user.get("premium_until"))
    if until is None:
        return None
    delta = until - dt.datetime.now(dt.timezone.utc)
    return max(0, delta.days)


@with_retry()
def activate_premium(user_id: int, days: int) -> dt.datetime:
    # If user already has active premium, extend from existing expiry date
    user = get_user(user_id)
    now = dt.datetime.now(dt.timezone.utc)
    base = now
    if user:
        existing_until = _parse_dt(user.get("premium_until"))
        if existing_until and existing_until > now:
            base = existing_until
    until = base + dt.timedelta(days=days)
    _client.table("users").update(
        {
            "plan": "premium",
            "premium_until": until.isoformat(),
            "total_payments": _increment_field(user_id, "total_payments", 1),
            "total_stars_spent": _increment_field(user_id, "total_stars_spent", settings.stars_price),
        }
    ).eq("id", user_id).execute()
    # Log payment
    _client.table("payments").insert({
        "user_id": user_id,
        "stars": settings.stars_price,
        "days": days,
        "plan": "premium",
    }).execute()
    return until


def _increment_field(user_id: int, field: str, by: int) -> int:
    user = get_user(user_id)
    if user is None:
        return by
    return (user.get(field, 0) or 0) + by


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
    """Single PostgreSQL RPC call — falls back to 3-query path if RPC unavailable."""
    try:
        result = _client.rpc("check_usage_and_get_history", {
            "p_user_id": user_id,
            "p_free_limit": settings.free_daily_limit,
            "p_prem_limit": settings.premium_daily_limit,
            "p_hist_limit": settings.history_limit,
        }).execute()
        if result.data:
            data = result.data
            if isinstance(data, list):
                data = data[0]
            return data
    except Exception as exc:  # noqa: BLE001
        logger.warning("RPC check_usage_and_get_history failed, using fallback: %s", exc)
    return _check_usage_fallback(user_id)


@with_retry()
def _check_usage_fallback(user_id: int) -> dict:
    """3-query fallback used when the RPC is not yet deployed."""
    user = get_user(user_id)
    if user is None:
        user = get_or_create_user(user_id, None, None)

    plan = effective_plan(user)
    bonus = user.get("bonus_messages", 0) or 0
    limit = get_daily_limit(plan, bonus)
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
        "allowed":    allowed,
        "usage":      usage,
        "limit":      limit,
        "plan":       plan,
        "chat_mode":  get_chat_mode(user),
        "web_search": get_web_search_enabled(user),
        "history":    history,
        "user":       user,
    }


# ── Messages ───────────────────────────────────────────────────────────────

@with_retry()
def save_message(
    user_id: int,
    role: Literal["user", "assistant"],
    content: str,
    topic: str | None = None,
) -> None:
    payload: dict = {"user_id": user_id, "role": role, "content": content}
    if topic:
        payload["topic"] = topic
    _client.table("messages").insert(payload).execute()


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
def get_all_messages(user_id: int) -> list[dict]:
    result = (
        _client.table("messages")
        .select("role, content, created_at, topic")
        .eq("user_id", user_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


@with_retry()
def clear_history(user_id: int) -> int:
    result = _client.table("messages").delete().eq("user_id", user_id).execute()
    return len(result.data) if result.data else 0


# ── Admin ──────────────────────────────────────────────────────────────────

@with_retry()
def get_stats() -> dict:
    today = _today()
    this_month_start = dt.date.today().replace(day=1).isoformat()

    total         = _client.table("users").select("id", count="exact").execute()
    premium       = _client.table("users").select("id", count="exact").eq("plan", "premium").execute()
    active_today  = _client.table("users").select("id", count="exact").eq("last_usage_date", today).execute()
    msgs_today    = _client.table("messages").select("id", count="exact").gte("created_at", f"{today}T00:00:00").execute()
    total_msgs    = _client.table("messages").select("id", count="exact").execute()

    # Revenue stats (if payments table exists)
    revenue_total = 0
    revenue_month = 0
    payment_count = 0
    try:
        rev = _client.table("payments").select("stars").execute()
        if rev.data:
            revenue_total = sum(r.get("stars", 0) for r in rev.data)
            payment_count = len(rev.data)
        rev_month = _client.table("payments").select("stars").gte(
            "created_at", f"{this_month_start}T00:00:00"
        ).execute()
        if rev_month.data:
            revenue_month = sum(r.get("stars", 0) for r in rev_month.data)
    except Exception:  # noqa: BLE001
        pass

    return {
        "total_users":    total.count or 0,
        "premium_users":  premium.count or 0,
        "active_today":   active_today.count or 0,
        "messages_today": msgs_today.count or 0,
        "total_messages": total_msgs.count or 0,
        "revenue_total":  revenue_total,
        "revenue_month":  revenue_month,
        "payment_count":  payment_count,
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


@with_retry()
def get_users_expiring_soon(days: int) -> list[dict]:
    """Returns premium users whose subscription expires within `days` days."""
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = (now + dt.timedelta(days=days)).isoformat()
    result = (
        _client.table("users")
        .select("id, first_name, username, premium_until")
        .eq("plan", "premium")
        .lte("premium_until", cutoff)
        .gte("premium_until", now.isoformat())
        .execute()
    )
    return result.data or []


@with_retry()
def get_top_users(limit: int = 10) -> list[dict]:
    """Returns top users by total messages sent."""
    result = (
        _client.table("users")
        .select("id, first_name, username, plan, daily_usage")
        .order("daily_usage", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []

"""
Redis cache layer (optional).

If REDIS_URL is not set, all cache calls are no-ops and the bot
works exactly as before — just without caching.

Uses redis-py with asyncio support (redis[asyncio]).

Cached data:
  - user row          TTL 60 s   key: user:{id}
  - flood timestamps  TTL 10 s   key: flood:{id}
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

_redis: Any = None   # redis.asyncio.Redis | None


async def init_cache() -> None:
    """Call once at startup. Safe to call even if REDIS_URL is unset."""
    global _redis
    url = os.getenv("REDIS_URL", "")
    if not url:
        logger.info("REDIS_URL not set — running without cache (no-op mode)")
        return
    try:
        import redis.asyncio as aioredis  # type: ignore[import]
        _redis = aioredis.from_url(url, decode_responses=True, socket_timeout=2)
        await _redis.ping()
        logger.info("Redis connected: %s", url.split("@")[-1])
    except Exception as exc:  # noqa: BLE001
        logger.warning("Redis unavailable (%s) — falling back to no-cache mode", exc)
        _redis = None


async def close_cache() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None


# ── User cache ─────────────────────────────────────────────────────────────

USER_TTL = 60  # seconds


async def get_user(user_id: int) -> dict | None:
    if _redis is None:
        return None
    try:
        raw = await _redis.get(f"user:{user_id}")
        return json.loads(raw) if raw else None
    except Exception:  # noqa: BLE001
        return None


async def set_user(user: dict) -> None:
    if _redis is None:
        return
    try:
        await _redis.setex(f"user:{user['id']}", USER_TTL, json.dumps(user))
    except Exception:  # noqa: BLE001
        pass


async def invalidate_user(user_id: int) -> None:
    """Call after any write to the users table."""
    if _redis is None:
        return
    try:
        await _redis.delete(f"user:{user_id}")
    except Exception:  # noqa: BLE001
        pass


# ── Distributed flood control ──────────────────────────────────────────────

FLOOD_TTL = 10  # seconds window


async def check_flood(user_id: int, min_interval: float) -> bool:
    """
    Returns True if the user is flooding (too fast), False if OK.
    Falls back to False (allow) if Redis is unavailable.
    """
    if _redis is None:
        return False
    key = f"flood:{user_id}"
    try:
        result = await _redis.set(key, "1", px=int(min_interval * 1000), nx=True)
        # nx=True means "set only if Not eXists"
        # result is True  → key was new → user is NOT flooding
        # result is None  → key existed → user IS flooding
        return result is None
    except Exception:  # noqa: BLE001
        return False

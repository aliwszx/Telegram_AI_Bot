"""
Redis cache layer — user context caching + flood control.

Keys:
  user:{id}        → JSON of user row         TTL 30 s
  ctx:{id}         → JSON of check_usage ctx  TTL 10 s  (hot path)
  flood:{id}       → flood sentinel            TTL = min_interval ms

Falls back silently to no-op when Redis is unavailable.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

_redis = None

try:
    import redis.asyncio as aioredis
    _REDIS_URL = os.getenv("REDIS_URL", "")
    if _REDIS_URL:
        _redis = aioredis.from_url(_REDIS_URL, decode_responses=True)
        logger.info("Redis cache connected: %s", _REDIS_URL[:30])
    else:
        logger.info("REDIS_URL not set — cache disabled.")
except ImportError:
    logger.info("redis package not installed — cache disabled.")

_USER_TTL = 30    # seconds — user row cache
_CTX_TTL  = 10   # seconds — check_usage_and_get_history result


# ── low-level helpers ───────────────────────────────────────────────────────

async def _get(key: str) -> Any | None:
    if _redis is None:
        return None
    try:
        raw = await _redis.get(key)
        return json.loads(raw) if raw else None
    except Exception as exc:  # noqa: BLE001
        logger.debug("Redis GET %s error: %s", key, exc)
        return None


async def _set(key: str, value: Any, ttl: int) -> None:
    if _redis is None:
        return
    try:
        await _redis.set(key, json.dumps(value), ex=ttl)
    except Exception as exc:  # noqa: BLE001
        logger.debug("Redis SET %s error: %s", key, exc)


async def _delete(*keys: str) -> None:
    if _redis is None:
        return
    try:
        await _redis.delete(*keys)
    except Exception as exc:  # noqa: BLE001
        logger.debug("Redis DEL error: %s", exc)


# ── public API ──────────────────────────────────────────────────────────────

async def get_user(user_id: int) -> dict | None:
    """Return cached user row or None."""
    return await _get(f"user:{user_id}")


async def set_user(user_id: int, row: dict) -> None:
    """Cache user row for _USER_TTL seconds."""
    await _set(f"user:{user_id}", row, _USER_TTL)


async def get_ctx(user_id: int) -> dict | None:
    """
    Return cached check_usage_and_get_history result or None.
    NOTE: ctx contains 'allowed' + usage counters — invalidate on every
    successful AI reply so the counter stays accurate.
    """
    return await _get(f"ctx:{user_id}")


async def set_ctx(user_id: int, ctx: dict) -> None:
    """
    Cache the usage-context for _CTX_TTL seconds.
    Skips caching when allowed=False so the limit message is always fresh.
    """
    if not ctx.get("allowed", True):
        return
    # history contains bytes-like objects that aren't JSON-safe — drop it
    slim = {k: v for k, v in ctx.items() if k != "history"}
    await _set(f"ctx:{user_id}", slim, _CTX_TTL)


async def invalidate_user(user_id: int) -> None:
    """Invalidate all cached data for a user (call after every write)."""
    await _delete(f"user:{user_id}", f"ctx:{user_id}")


async def check_flood(user_id: int, min_interval: float) -> bool:
    """Returns True if user is flooding (too fast), False if request is allowed."""
    if _redis is None:
        return False
    try:
        key = f"flood:{user_id}"
        result = await _redis.set(key, 1, px=int(min_interval * 1000), nx=True)
        return result is None  # None → key existed → flooding
    except Exception as exc:  # noqa: BLE001
        logger.warning("Redis flood check error: %s", exc)
        return False


async def ping() -> bool:
    if _redis is None:
        return False
    try:
        return await _redis.ping()
    except Exception:  # noqa: BLE001
        return False

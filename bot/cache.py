"""
Optional Redis cache layer for user context.
Falls back to no-op if Redis is unavailable.
"""
from __future__ import annotations

import logging
import os

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


async def invalidate_user(user_id: int) -> None:
    if _redis is None:
        return
    try:
        await _redis.delete(f"user:{user_id}")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Redis invalidate error: %s", exc)


async def check_flood(user_id: int, min_interval: float) -> bool:
    """Returns True if user is flooding (too fast), False if request is allowed."""
    if _redis is None:
        return False
    try:
        key = f"flood:{user_id}"
        # SET key 1 PX <ms> NX — only sets if key doesn't exist
        result = await _redis.set(key, 1, px=int(min_interval * 1000), nx=True)
        # result is None means key already existed → flooding
        return result is None
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

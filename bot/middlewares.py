"""
Anti-flood middleware.

If Redis is available (REDIS_URL set), uses distributed rate limiting
so it works correctly across multiple bot instances.

Falls back to in-memory rate limiting when Redis is unavailable —
identical behaviour to the original single-instance implementation.
"""
from __future__ import annotations

import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot import cache as redis_cache


class FloodControlMiddleware(BaseMiddleware):
    def __init__(self, min_interval: float = 1.5) -> None:
        self.min_interval = min_interval
        # In-memory fallback (used when Redis is unavailable)
        self._last_seen: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user = event.from_user
        if user is not None:
            # Try Redis first
            flooding = await redis_cache.check_flood(user.id, self.min_interval)
            if flooding:
                return  # silently drop

            # Redis unavailable → in-memory fallback
            if redis_cache._redis is None:
                now = time.monotonic()
                last = self._last_seen.get(user.id, 0.0)
                if now - last < self.min_interval:
                    return
                self._last_seen[user.id] = now
                # Evict entries older than 60 s when dict grows large
                if len(self._last_seen) > 5000:
                    cutoff = now - 60
                    stale = [uid for uid, ts in self._last_seen.items() if ts < cutoff]
                    for uid in stale:
                        del self._last_seen[uid]

        return await handler(event, data)

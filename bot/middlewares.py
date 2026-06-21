"""
Simple in-memory anti-flood guard: prevents a single user from firing
messages faster than `min_interval` seconds apart. This is independent from
the persisted daily usage limit in bot/db.py — this one just protects the
bot/Gemini API from being hammered in a tight loop.

In-memory is fine for a single Render worker instance. If you ever scale to
multiple instances, move this to Redis or Supabase instead.
"""
from __future__ import annotations

import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message


class FloodControlMiddleware(BaseMiddleware):
    def __init__(self, min_interval: float = 1.5) -> None:
        self.min_interval = min_interval
        self._last_seen: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user = event.from_user
        if user is not None:
            now = time.monotonic()
            last = self._last_seen.get(user.id, 0.0)
            if now - last < self.min_interval:
                return  # silently drop, no API/DB hit
            self._last_seen[user.id] = now

        return await handler(event, data)

"""
Anti-flood middleware (in-memory, single-instance).
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
                return  # silently drop
            self._last_seen[user.id] = now

        return await handler(event, data)

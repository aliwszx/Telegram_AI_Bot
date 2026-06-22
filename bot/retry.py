"""
Retry utilities for transient errors.
"""
from __future__ import annotations

import functools
import logging
import time
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable)

_TRANSIENT_KEYWORDS = (
    "connection", "timeout", "reset", "unavailable",
    "503", "502", "504", "temporarily",
)

_RATE_LIMIT_KEYWORDS = (
    "rate", "quota", "429", "resource_exhausted",
    "resourceexhausted", "too many",
)


def is_transient(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(kw in msg for kw in _TRANSIENT_KEYWORDS)


def is_rate_limited(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(kw in msg for kw in _RATE_LIMIT_KEYWORDS)


def with_retry(max_attempts: int = 3, base_delay: float = 0.5):
    """Decorator that retries on transient DB errors."""
    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    last_exc = exc
                    if not is_transient(exc):
                        raise
                    if attempt < max_attempts:
                        delay = base_delay * (2 ** (attempt - 1))
                        logger.warning(
                            "%s transient error (attempt %s/%s), retrying in %.1fs: %s",
                            fn.__name__, attempt, max_attempts, delay, exc,
                        )
                        time.sleep(delay)
            raise last_exc
        return wrapper  # type: ignore
    return decorator

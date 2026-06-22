"""
Retry utilities for transient errors.
"""
from __future__ import annotations

import functools
import logging
import re
import time
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable)

_TRANSIENT_KEYWORDS = (
    "connection", "timeout", "reset", "unavailable",
    "503", "502", "504", "temporarily",
)


def is_transient(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(kw in msg for kw in _TRANSIENT_KEYWORDS)


def is_rate_limited(exc: Exception) -> bool:
    """
    Detects genuine rate-limit / quota errors.
    Uses precise patterns instead of bare keywords to avoid false positives
    (e.g. 'rate' appearing inside 'generativelanguage', or 404 NOT_FOUND
    being misclassified because the error text contains unrelated words).
    """
    msg = str(exc).lower()

    # 404 / NOT_FOUND → model doesn't exist, not a rate limit
    if "404" in msg or "not_found" in msg or "not found" in msg:
        return False

    # Explicit HTTP 429 status code
    if "429" in msg:
        return True

    # Google API quota/resource exhausted signals
    if "resource_exhausted" in msg or "resourceexhausted" in msg:
        return True

    # Quota as a standalone word (not inside a URL like generativelanguage.googleapis.com)
    if re.search(r"\bquota\b", msg):
        return True

    # "too many requests" phrase
    if "too many" in msg:
        return True

    # "rate limit" or "rate-limit" as a phrase (not bare "rate" which matches URLs)
    if re.search(r"rate.?limit", msg):
        return True

    return False


def is_model_not_found(exc: Exception) -> bool:
    """Detects 404 / model-not-found errors — skip to next model, don't retry."""
    msg = str(exc).lower()
    return "404" in msg or "not_found" in msg or "not found" in msg


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

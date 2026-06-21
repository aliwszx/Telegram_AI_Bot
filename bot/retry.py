"""
Small retry / exponential-backoff helpers shared by ai.py and db.py.

Only *transient* errors are retried (timeouts, connection resets, 502/503/504,
DNS hiccups, etc). Things like auth errors, bad requests, or "not found"
are re-raised immediately — retrying them would just waste time.
"""
from __future__ import annotations

import functools
import logging
import random
import time

logger = logging.getLogger(__name__)

TRANSIENT_KEYWORDS = (
    "timeout",
    "timed out",
    "connection",
    "connect",
    "network",
    "temporarily unavailable",
    "reset by peer",
    "broken pipe",
    "502",
    "503",
    "504",
    "ssl",
    "eof occurred",
)

RATE_LIMIT_KEYWORDS = ("429", "quota", "rate", "resource_exhausted")


def is_transient(exc: BaseException) -> bool:
    """Heuristic: is this likely a network glitch worth retrying?"""
    err_str = str(exc).lower()
    return any(k in err_str for k in TRANSIENT_KEYWORDS)


def is_rate_limited(exc: BaseException) -> bool:
    err_str = str(exc).lower()
    return any(k in err_str for k in RATE_LIMIT_KEYWORDS)


def with_retry(retries: int = 2, base_delay: float = 0.5, max_delay: float = 4.0):
    """
    Decorator for synchronous functions that talk to a network service
    (e.g. Supabase calls in db.py). Retries only on transient errors,
    with exponential backoff + small jitter.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    if not is_transient(exc) or attempt >= retries:
                        raise
                    attempt += 1
                    delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                    delay += random.uniform(0, 0.25)
                    logger.warning(
                        "%s: transient error (attempt %s/%s), retrying in %.2fs: %s",
                        fn.__name__, attempt, retries, delay, exc,
                    )
                    time.sleep(delay)
        return wrapper
    return decorator

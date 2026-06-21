"""
Sentry integration — optional. If SENTRY_DSN is not set, init_sentry() is a
no-op and sentry_sdk.capture_exception() calls elsewhere in the codebase
become harmless no-ops too (sentry_sdk handles that internally).
"""
from __future__ import annotations

import logging

from bot.config import settings

logger = logging.getLogger(__name__)


def init_sentry() -> None:
    if not settings.sentry_dsn:
        logger.info("SENTRY_DSN not set — error tracking disabled")
        return
    try:
        import sentry_sdk

        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.sentry_environment,
            traces_sample_rate=0.0,  # we only care about error tracking, not perf
            send_default_pii=False,
        )
        logger.info("Sentry initialized (environment=%s)", settings.sentry_environment)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Sentry init failed, continuing without it: %s", exc)

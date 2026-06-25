"""
Background scheduler — runs periodic tasks:
  - Premium expiry warning notifications
  - Daily stats logging
"""
from __future__ import annotations

import asyncio
import logging

logger = logging.getLogger(__name__)


async def check_expiring_premiums(bot) -> None:
    """Send expiry warning to users whose premium expires within 3 days."""
    from bot import db
    from bot.config import settings

    try:
        users = await asyncio.to_thread(
            db.get_users_expiring_soon, settings.premium_expiry_warning_days
        )
        for user in users:
            days_left = db.days_until_premium_expires(user)
            if days_left is None:
                continue
            name = user.get("first_name") or "İstifadəçi"
            try:
                await bot.send_message(
                    user["id"],
                    f"⚠️ <b>Premium bitmək üzrədir!</b>\n\n"
                    f"Salam {name}! Premiumun <b>{days_left} gün</b> sonra bitir.\n\n"
                    "Kəsilməmək üçün /upgrade yazaraq uzat! ⭐",
                    parse_mode="HTML",
                )
                logger.info("Expiry warning sent to user %s (%d days left)", user["id"], days_left)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not send expiry warning to %s: %s", user["id"], exc)
    except Exception as exc:  # noqa: BLE001
        logger.error("check_expiring_premiums error: %s", exc)


async def log_daily_stats() -> None:
    """Log daily statistics to console / Sentry."""
    from bot import db
    try:
        stats = await asyncio.to_thread(db.get_stats)
        logger.info(
            "📊 Daily stats — users: %d, premium: %d, active_today: %d, msgs_today: %d",
            stats["total_users"],
            stats["premium_users"],
            stats["active_today"],
            stats["messages_today"],
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("log_daily_stats error: %s", exc)


async def run_scheduler(bot) -> None:
    """Main scheduler loop. Runs every hour."""
    logger.info("Scheduler started.")
    tick = 0
    while True:
        await asyncio.sleep(3600)
        tick += 1

        # Every hour
        await log_daily_stats()

        # Every 12 hours — expiry warnings
        if tick % 12 == 0:
            await check_expiring_premiums(bot)

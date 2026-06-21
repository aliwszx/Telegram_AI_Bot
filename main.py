"""
Entrypoint — polling mode.

Recommended for Render "Background Worker" services: no public port needed.

Run locally:   python main.py
Run on Render: set Start Command to `python main.py` on a Background Worker.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.cache import init_cache, close_cache
from bot.config import settings
from bot.handlers import router
from bot.middlewares import FloodControlMiddleware
from bot.sentry import init_sentry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def _run_health_server() -> None:
    """
    Tiny '/' health-check endpoint for uptime monitors (UptimeRobot, Better
    Stack, etc) even when running in polling mode. Safe no-op if the port
    can't be bound (e.g. on a Render Background Worker with no public port).
    """
    try:
        from aiohttp import web

        async def health(_: web.Request) -> web.Response:
            return web.Response(text="ok")

        app = web.Application()
        app.router.add_get("/", health)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", settings.port)
        await site.start()
        logger.info("Health-check server listening on :%s", settings.port)
    except Exception as exc:  # noqa: BLE001
        logger.info("Health-check server not started (%s) — continuing without it", exc)


async def main() -> None:
    settings.validate()
    init_sentry()

    await init_cache()
    asyncio.create_task(_run_health_server())

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.message.middleware(FloodControlMiddleware(min_interval=1.5))
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Starting bot in polling mode...")
    try:
        await dp.start_polling(bot)
    finally:
        await close_cache()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

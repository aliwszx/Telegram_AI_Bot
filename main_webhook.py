"""
Entrypoint — webhook mode (recommended for production on Render Web Service).

Advantages over polling:
  - Telegram pushes updates instantly (no long-poll delay)
  - Render's health checks work (HTTP port is bound)
  - Lower resource usage

Setup:
  1. Deploy as a Render "Web Service" (not Background Worker)
  2. Set env vars: WEBHOOK_BASE_URL=https://your-app.onrender.com
  3. Set Start Command: python main_webhook.py
"""
from __future__ import annotations

import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.cache import init_cache, close_cache
from bot.config import settings
from bot.handlers import router
from bot.middlewares import FloodControlMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    await init_cache()
    webhook_url = settings.webhook_base_url.rstrip("/") + settings.webhook_path
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    logger.info("Webhook set → %s", webhook_url)


async def on_shutdown(bot: Bot) -> None:
    await close_cache()
    await bot.delete_webhook()
    logger.info("Webhook removed, cache closed.")


def build_app() -> web.Application:
    settings.validate()
    if not settings.webhook_base_url:
        raise RuntimeError("WEBHOOK_BASE_URL must be set when running main_webhook.py")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.message.middleware(FloodControlMiddleware(min_interval=1.5))
    dp.include_router(router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)

    # Health check — required for Render Web Service port detection
    async def health(_: web.Request) -> web.Response:
        return web.Response(text="ok")

    app.router.add_get("/", health)
    return app


if __name__ == "__main__":
    web.run_app(build_app(), host="0.0.0.0", port=settings.port)

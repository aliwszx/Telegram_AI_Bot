"""
Entrypoint — webhook mode for Render Web Service.
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


async def on_startup(app: web.Application) -> None:
    bot: Bot = app["bot"]
    await init_cache()
    webhook_url = settings.webhook_base_url.rstrip("/") + settings.webhook_path
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    logger.info("Webhook set → %s", webhook_url)


async def on_shutdown(app: web.Application) -> None:
    bot: Bot = app["bot"]
    await close_cache()
    # NOTE: intentionally NOT calling bot.delete_webhook() here.
    # Render briefly overlaps old/new instances during zero-downtime
    # deploys — if the old instance deletes the webhook after the new
    # one has already set it, Telegram is left with no webhook at all.
    await bot.session.close()
    logger.info("Bot shutdown complete.")


def build_app() -> web.Application:
    settings.validate()
    if not settings.webhook_base_url:
        raise RuntimeError("WEBHOOK_BASE_URL must be set")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.message.middleware(FloodControlMiddleware(min_interval=1.5))
    dp.include_router(router)

    app = web.Application()
    app["bot"] = bot

    # Register aiohttp lifecycle hooks (not aiogram dp hooks)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)

    # Health check endpoint
    async def health(_: web.Request) -> web.Response:
        return web.Response(text="ok")

    app.router.add_get("/", health)
    return app


if __name__ == "__main__":
    web.run_app(build_app(), host="0.0.0.0", port=settings.port)

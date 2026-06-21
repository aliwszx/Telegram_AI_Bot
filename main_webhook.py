"""
Optional entrypoint for webhook mode, useful if you deploy as a Render
"Web Service" (which requires the process to bind to a port and respond to
HTTP health checks) instead of a "Background Worker".

Run on Render: set Start Command to `python main_webhook.py`,
and make sure WEBHOOK_BASE_URL is set to your public Render URL,
e.g. https://my-bot.onrender.com
"""
from __future__ import annotations

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.config import settings
from bot.handlers import router
from bot.middlewares import FloodControlMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    webhook_url = settings.webhook_base_url.rstrip("/") + settings.webhook_path
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    logger.info("Webhook set to %s", webhook_url)


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

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)

    # Simple health check endpoint so Render's port check passes.
    async def health(_request: web.Request) -> web.Response:
        return web.Response(text="ok")

    app.router.add_get("/", health)
    return app


if __name__ == "__main__":
    web.run_app(build_app(), host="0.0.0.0", port=settings.port)

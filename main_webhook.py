"""
Webhook entry point — for Render / Railway / Fly.io deployments.
Usage: python main_webhook.py
"""
import asyncio
import logging

import sentry_sdk
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import settings
from bot.handlers import router
from bot.scheduler import run_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _init_sentry() -> None:
    if not settings.sentry_dsn:
        return
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.sentry_environment,
        traces_sample_rate=0.1,
    )
    logger.info("Sentry initialised (env=%s)", settings.sentry_environment)


async def on_startup(bot: Bot) -> None:
    webhook_url = f"{settings.webhook_base_url}{settings.webhook_path}"
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=["message", "callback_query", "pre_checkout_query", "inline_query"],
        drop_pending_updates=True,
    )
    me = await bot.get_me()
    logger.info("Webhook set to %s for @%s", webhook_url, me.username)

    # Start background scheduler in background
    asyncio.create_task(run_scheduler(bot))


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    logger.info("Webhook deleted.")


def main() -> None:
    settings.validate()
    _init_sentry()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    handler.register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)

    # Health check endpoint
    async def health(_request: web.Request) -> web.Response:
        return web.json_response({"status": "ok", "bot": "running"})

    app.router.add_get("/health", health)
    app.router.add_get("/", health)

    logger.info("Starting webhook server on port %s", settings.port)
    web.run_app(app, host="0.0.0.0", port=settings.port)


if __name__ == "__main__":
    main()

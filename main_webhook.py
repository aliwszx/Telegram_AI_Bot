"""
Webhook entry point — for Render / Railway / Fly.io deployments.
Usage: python main_webhook.py
"""
import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import settings
from bot.handlers import router
from bot.scheduler import run_scheduler
from bot.sentry import init_sentry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    webhook_url = f"{settings.webhook_base_url}{settings.webhook_path}"
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=["message", "callback_query", "pre_checkout_query", "inline_query"],
        drop_pending_updates=True,
    )
    me = await bot.get_me()
    logger.info("Webhook set to %s for @%s", webhook_url, me.username)

    # Start background scheduler
    asyncio.create_task(run_scheduler(bot))


async def on_shutdown(bot: Bot) -> None:
    # NOTE: intentionally NOT calling bot.delete_webhook() here.
    # Render briefly overlaps old/new instances during zero-downtime deploys.
    # If the old instance deletes the webhook AFTER the new one has set it,
    # Telegram is left with no webhook at all — bot stops responding completely.
    logger.info("Bot shutdown complete.")


def main() -> None:
    settings.validate(webhook_mode=True)
    init_sentry()

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

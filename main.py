"""
Long-polling entry point.
Usage: python main.py
"""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.middlewares import FloodControlMiddleware

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
    # Start background scheduler after the event loop is fully running
    asyncio.create_task(run_scheduler(bot))
    me = await bot.get_me()
    logger.info("Bot started: @%s (polling)", me.username)


async def main() -> None:
    settings.validate()
    init_sentry()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.message.middleware(FloodControlMiddleware())
    dp.include_router(router)
    dp.startup.register(on_startup)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

"""
All Telegram update handlers live here: /start, /help, /status, /grant
(admin) and the catch-all text handler that drives the AI chat.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from bot import db
from bot.ai import generate_reply, GeminiError
from bot.config import settings

logger = logging.getLogger(__name__)
router = Router(name="main")


WELCOME_TEXT = (
    "👋 Salam! Mən AI chat botam (Gemini ilə işləyirəm).\n\n"
    "Mənə istənilən sualını yaz, cavab verim. Söhbət tarixçəni yadda saxlayıram, "
    "ona görə kontekstli davam edə bilərsən.\n\n"
    "Komandalar:\n"
    "/start — botu başlat\n"
    "/help — kömək\n"
    "/status — planın və günlük limitin\n"
)

HELP_TEXT = (
    "ℹ️ İstifadə qaydası:\n"
    "Sadəcə mesaj yaz, AI cavab verəcək.\n\n"
    "/status — plan (free/premium) və günlük limitin neçə qalıb\n"
    "/start — yenidən başlatma mesajı\n"
)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    user = message.from_user
    await asyncio.to_thread(
        db.get_or_create_user, user.id, user.username, user.first_name
    )
    await message.answer(WELCOME_TEXT)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    user = message.from_user
    row = await asyncio.to_thread(
        db.get_or_create_user, user.id, user.username, user.first_name
    )
    plan = row.get("plan", "free")
    limit = db.get_daily_limit(plan)
    usage = row.get("daily_usage", 0)
    used_today = usage if row.get("last_usage_date") == db.today() else 0
    remaining = max(limit - used_today, 0)

    await message.answer(
        f"📊 Plan: <b>{plan}</b>\n"
        f"Bugünkü istifadə: {used_today}/{limit}\n"
        f"Qalan limit: {remaining}",
        parse_mode="HTML",
    )


@router.message(Command("grant"))
async def cmd_grant(message: Message, command: CommandObject) -> None:
    """Admin-only: /grant <user_id> <free|premium> — upgrade/downgrade a user.
    Useful as the hook point for a future payment webhook (Stripe/Click/Payme)."""
    if message.from_user.id not in settings.admin_ids:
        return  # silently ignore for non-admins

    if not command.args:
        await message.answer("İstifadə: /grant <user_id> <free|premium>")
        return

    parts = command.args.split()
    if len(parts) != 2 or parts[1] not in ("free", "premium"):
        await message.answer("İstifadə: /grant <user_id> <free|premium>")
        return

    target_id, plan = int(parts[0]), parts[1]
    await asyncio.to_thread(db.set_plan, target_id, plan)
    await message.answer(f"✅ User {target_id} → plan: {plan}")


@router.message(F.text & ~F.text.startswith("/"))
async def handle_ai_chat(message: Message) -> None:
    user = message.from_user
    user_text = message.text.strip()
    if not user_text:
        return

    await asyncio.to_thread(
        db.get_or_create_user, user.id, user.username, user.first_name
    )

    allowed, remaining, limit = await asyncio.to_thread(
        db.check_and_increment_usage, user.id
    )
    if not allowed:
        await message.answer(
            "⛔ Bugünkü mesaj limitin bitdi "
            f"({limit}/{limit}). Limit sabah sıfırlanacaq, "
            "ya da premium plana keçərək limiti artıra bilərsən."
        )
        return

    await message.bot.send_chat_action(message.chat.id, "typing")

    history = await asyncio.to_thread(db.get_recent_messages, user.id)

    try:
        reply_text = await asyncio.to_thread(
            generate_reply, history, user_text, user.language_code
        )
    except GeminiError:
        logger.exception("Gemini call failed for user %s", user.id)
        await message.answer(
            "😕 Hazırda AI cavab verə bilmədi, bir az sonra yenidən cəhd et."
        )
        return

    await asyncio.to_thread(db.save_message, user.id, "user", user_text)
    await asyncio.to_thread(db.save_message, user.id, "assistant", reply_text)

    await message.answer(reply_text)
    if remaining <= 3:
        await message.answer(f"ℹ️ Bugün üçün qalan limit: {remaining}/{limit}")

"""
All Telegram update handlers live here: /start, /help, /status, /grant
(admin) and the catch-all text handler that drives the AI chat.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

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
    "/upgrade — Telegram Stars ilə premiuma keç\n"
)

HELP_TEXT = (
    "ℹ️ İstifadə qaydası:\n"
    "Sadəcə mesaj yaz, AI cavab verəcək.\n\n"
    "/status — plan (free/premium) və günlük limitin neçə qalıb\n"
    "/upgrade — Telegram Stars ilə premiuma keç (limitin artır)\n"
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
    plan = await asyncio.to_thread(db.effective_plan, row)
    limit = db.get_daily_limit(plan)
    usage = row.get("daily_usage", 0)
    used_today = usage if row.get("last_usage_date") == db.today() else 0
    remaining = max(limit - used_today, 0)

    lines = [
        f"📊 Plan: <b>{plan}</b>",
        f"Bugünkü istifadə: {used_today}/{limit}",
        f"Qalan limit: {remaining}",
    ]
    if plan == "premium" and row.get("premium_until"):
        lines.append(f"Premium bitmə tarixi: {row['premium_until'][:10]}")
    elif plan == "free":
        lines.append(f"\n⭐ Premium almaq üçün: /upgrade")

    await message.answer("\n".join(lines), parse_mode="HTML")


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


@router.message(Command("upgrade"))
async def cmd_upgrade(message: Message) -> None:
    """Sends a Telegram Stars invoice to upgrade to premium.
    Stars (currency 'XTR') need no payment provider/bank setup — Telegram
    handles the payment itself, and it works in every country."""
    row = await asyncio.to_thread(
        db.get_or_create_user,
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )
    plan = await asyncio.to_thread(db.effective_plan, row)
    if plan == "premium":
        await message.answer(
            f"✅ Artıq premium istifadəçisisən "
            f"(bitmə tarixi: {row.get('premium_until', '—')[:10] if row.get('premium_until') else 'sonsuz'})."
        )
        return

    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title="Premium plan",
        description=(
            f"{settings.premium_duration_days} gün premium: "
            f"günlük {settings.premium_daily_limit} mesaj limiti."
        ),
        payload=f"premium_upgrade:{message.from_user.id}",
        currency="XTR",
        prices=[LabeledPrice(label="Premium", amount=settings.stars_price)],
        provider_token="",  # not needed for Telegram Stars
    )


@router.pre_checkout_query()
async def handle_pre_checkout(pre_checkout_query: PreCheckoutQuery) -> None:
    # Always approve here unless you need to re-validate stock/price; the
    # actual upgrade happens only after successful_payment below.
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def handle_successful_payment(message: Message) -> None:
    until = await asyncio.to_thread(
        db.activate_premium, message.from_user.id, settings.premium_duration_days
    )
    await message.answer(
        "🎉 Ödəniş uğurla alındı! Premium aktivləşdi.\n"
        f"Bitmə tarixi: {until.date().isoformat()}\n"
        f"Günlük limit: {settings.premium_daily_limit} mesaj."
    )


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

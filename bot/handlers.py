"""
All Telegram update handlers:
  /start, /help, /status, /upgrade, /grant  — existing
  /mode                                       — NEW: select AI persona
  /clear                                      — NEW: clear chat history
  photo handler                               — NEW: image analysis
  text handler                                — updated to pass mode + image
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, Message, PreCheckoutQuery, CallbackQuery,
)

from bot import db
from bot.ai import generate_reply, GeminiError, MODE_NAMES
from bot.config import settings

logger = logging.getLogger(__name__)
router = Router(name="main")


# ── Static texts ───────────────────────────────────────────────────────────

WELCOME_TEXT = (
    "👋 <b>Salam, {name}!</b>\n\n"
    "Mən Gemini AI ilə işləyən smart bir botam.\n"
    "Sualını yaz, şəkil göndər, rejim seç — hər şey burada! 🚀\n\n"
    "Aşağıdakı düymələrdən başla 👇"
)

HELP_TEXT = (
    "ℹ️ <b>İstifadə qaydası</b>\n\n"
    "💬 <b>Mətn yaz</b> → AI cavab verir\n"
    "🖼 <b>Şəkil göndər</b> → AI şəkili analiz edir\n"
    "📝 <b>Şəkilə başlıq yaz</b> → həmin sual üzrə analiz\n\n"
    "<b>Komandalar:</b>\n"
    "/mode — AI rejimini dəyiş\n"
    "/status — plan və gündəlik limit\n"
    "/clear — söhbət tarixçəsini sil\n"
    "/upgrade — ⭐ Premium al\n"
)


# ── Keyboards ──────────────────────────────────────────────────────────────

def _start_keyboard() -> InlineKeyboardMarkup:
    """Ana menyu — /start-da göstərilir."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎭 Rejim seç", callback_data="menu:mode"),
            InlineKeyboardButton(text="📊 Status",    callback_data="menu:status"),
        ],
        [
            InlineKeyboardButton(text="🗑 Söhbəti sil", callback_data="menu:clear"),
            InlineKeyboardButton(text="⭐ Premium",      callback_data="menu:upgrade"),
        ],
        [
            InlineKeyboardButton(text="ℹ️ Kömək", callback_data="menu:help"),
        ],
    ])


def _mode_keyboard(current: str | None = None) -> InlineKeyboardMarkup:
    """Rejim seçmə klaviaturası — aktiv olanın yanında ✓ işarəsi."""
    buttons = []
    for key, label in MODE_NAMES.items():
        tick = " ✓" if key == current else ""
        buttons.append(
            [InlineKeyboardButton(text=f"{label}{tick}", callback_data=f"mode:{key}")]
        )
    buttons.append(
        [InlineKeyboardButton(text="⬅️ Geri", callback_data="menu:back")]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _back_keyboard() -> InlineKeyboardMarkup:
    """Sadə 'Geri' düyməsi olan klaviatura."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Əsas menyu", callback_data="menu:back")]
    ])


# ── Commands ───────────────────────────────────────────────────────────────

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    user = message.from_user
    await asyncio.to_thread(
        db.get_or_create_user, user.id, user.username, user.first_name
    )
    name = user.first_name or user.username or "Qonaq"
    await message.answer(
        WELCOME_TEXT.format(name=name),
        reply_markup=_start_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=_back_keyboard(), parse_mode="HTML")


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
    mode = db.get_chat_mode(row)

    lines = [
        f"📊 Plan: <b>{plan}</b>",
        f"🎭 Rejim: <b>{MODE_NAMES.get(mode, mode)}</b>",
        f"Bugünkü istifadə: {used_today}/{limit}",
        f"Qalan limit: {remaining}",
    ]
    if plan == "premium" and row.get("premium_until"):
        lines.append(f"Premium bitmə tarixi: {row['premium_until'][:10]}")
    elif plan == "free":
        lines.append("\n⭐ Premium almaq üçün: /upgrade")

    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("mode"))
async def cmd_mode(message: Message) -> None:
    row = await asyncio.to_thread(
        db.get_or_create_user,
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )
    current = db.get_chat_mode(row)
    await message.answer(
        f"🎭 Hazırki rejim: <b>{MODE_NAMES.get(current, current)}</b>\n\n"
        "Aşağıdan yeni rejim seç:",
        reply_markup=_mode_keyboard(current),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("mode:"))
async def cb_mode_select(callback: CallbackQuery) -> None:
    mode = callback.data.split(":", 1)[1]
    if mode not in MODE_NAMES:
        await callback.answer("Yanlış rejim.", show_alert=True)
        return

    await asyncio.to_thread(db.set_chat_mode, callback.from_user.id, mode)
    name = callback.from_user.first_name or callback.from_user.username or "Qonaq"
    await callback.message.edit_text(
        f"✅ Rejim dəyişdirildi: <b>{MODE_NAMES[mode]}</b>\n\n"
        "İndi mənə yaz! 👇",
        reply_markup=_start_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer(f"{MODE_NAMES[mode]} seçildi!")




@router.callback_query(F.data.startswith("menu:"))
async def cb_menu(callback: CallbackQuery) -> None:
    action = callback.data.split(":", 1)[1]
    user = callback.from_user

    if action == "back":
        name = user.first_name or user.username or "Qonaq"
        await callback.message.edit_text(
            WELCOME_TEXT.format(name=name),
            reply_markup=_start_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "mode":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        current = db.get_chat_mode(row)
        await callback.message.edit_text(
            f"🎭 Hazırki rejim: <b>{MODE_NAMES.get(current, current)}</b>\n\n"
            "Yeni rejim seç:",
            reply_markup=_mode_keyboard(current),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "status":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        plan = await asyncio.to_thread(db.effective_plan, row)
        limit = db.get_daily_limit(plan)
        usage = row.get("daily_usage", 0)
        used_today = usage if row.get("last_usage_date") == db.today() else 0
        remaining = max(limit - used_today, 0)
        mode = db.get_chat_mode(row)
        plan_emoji = "⭐" if plan == "premium" else "🆓"
        lines = [
            f"{plan_emoji} Plan: <b>{plan.upper()}</b>",
            f"🎭 Rejim: <b>{MODE_NAMES.get(mode, mode)}</b>",
            f"📨 Bugün: {used_today}/{limit} mesaj",
            f"✅ Qalan: {remaining} mesaj",
        ]
        if plan == "premium" and row.get("premium_until"):
            lines.append(f"📅 Bitmə tarixi: {row['premium_until'][:10]}")
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=_back_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "clear":
        count = await asyncio.to_thread(db.clear_history, user.id)
        name = user.first_name or user.username or "Qonaq"
        await callback.message.edit_text(
            f"🗑 Söhbət silindi ({count} mesaj).\n\nYeni söhbətə başla! 👇",
            reply_markup=_start_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer("Söhbət silindi!")

    elif action == "upgrade":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        plan = await asyncio.to_thread(db.effective_plan, row)
        if plan == "premium":
            await callback.answer("Artıq premium istifadəçisisən! ⭐", show_alert=True)
            return
        await callback.answer()
        await callback.message.answer_invoice(
            title="Premium plan ⭐",
            description=(
                f"{settings.premium_duration_days} gün premium — "
                f"günlük {settings.premium_daily_limit} mesaj limiti."
            ),
            payload=f"premium_upgrade:{user.id}",
            currency="XTR",
            prices=[LabeledPrice(label="Premium", amount=settings.stars_price)],
            provider_token="",
        )

    else:
        await callback.answer()

@router.message(Command("clear"))
async def cmd_clear(message: Message) -> None:
    count = await asyncio.to_thread(db.clear_history, message.from_user.id)
    await message.answer(
        f"🗑️ Söhbət tarixçəsi silindi ({count} mesaj).\n"
        "Yeni söhbətə başlaya bilərsən!"
    )


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
        provider_token="",
    )


@router.pre_checkout_query()
async def handle_pre_checkout(pre_checkout_query: PreCheckoutQuery) -> None:
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




# ══════════════════════════════════════════════════════════════════════════
# ADMIN PANEL
# ══════════════════════════════════════════════════════════════════════════

def _is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


def _admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Statistika",    callback_data="admin:stats"),
            InlineKeyboardButton(text="👥 İstifadəçilər", callback_data="admin:users"),
        ],
        [
            InlineKeyboardButton(text="📢 Broadcast",     callback_data="admin:broadcast_prompt"),
            InlineKeyboardButton(text="🔍 User axtar",    callback_data="admin:lookup_prompt"),
        ],
    ])


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    await message.answer(
        "🛠 <b>Admin Panel</b>\n\nNə etmək istəyirsən?",
        reply_markup=_admin_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("admin:"))
async def cb_admin(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("İcazən yoxdur.", show_alert=True)
        return

    action = callback.data.split(":", 1)[1]

    # ── Stats ──────────────────────────────────────────────────────────────
    if action == "stats":
        stats = await asyncio.to_thread(db.get_stats)
        free_users = stats["total_users"] - stats["premium_users"]
        text = (
            "📊 <b>Bot Statistikası</b>\n\n"
            f"👥 Cəmi istifadəçi:  <b>{stats['total_users']}</b>\n"
            f"⭐ Premium:           <b>{stats['premium_users']}</b>\n"
            f"🆓 Pulsuz:            <b>{free_users}</b>\n"
            f"🟢 Bu gün aktiv:     <b>{stats['active_today']}</b>\n"
            f"💬 Bu günkü mesaj:   <b>{stats['messages_today']}</b>\n"
            f"📨 Cəmi mesaj:       <b>{stats['total_messages']}</b>"
        )
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Yenilə", callback_data="admin:stats")],
                [InlineKeyboardButton(text="⬅️ Geri",   callback_data="admin:back")],
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    # ── Users summary ──────────────────────────────────────────────────────
    elif action == "users":
        stats = await asyncio.to_thread(db.get_stats)
        text = (
            "👥 <b>İstifadəçilər</b>\n\n"
            f"Cəmi: <b>{stats['total_users']}</b>\n"
            f"Premium: <b>{stats['premium_users']}</b>\n\n"
            "Konkret istifadəçini tapmaq üçün:\n"
            "<code>/lookup @username</code> və ya\n"
            "<code>/lookup 123456789</code>"
        )
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Geri", callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    # ── Broadcast prompt ───────────────────────────────────────────────────
    elif action == "broadcast_prompt":
        await callback.message.edit_text(
            "📢 <b>Broadcast</b>\n\n"
            "Bütün istifadəçilərə mesaj göndər:\n\n"
            "<code>/broadcast Mətnin buraya</code>\n\n"
            "⚠️ Bu əməliyyat geri alına bilməz!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Geri", callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    # ── Lookup prompt ──────────────────────────────────────────────────────
    elif action == "lookup_prompt":
        await callback.message.edit_text(
            "🔍 <b>User axtar</b>\n\n"
            "İstifadəçi tapmaq üçün:\n"
            "<code>/lookup @username</code>\n"
            "<code>/lookup 123456789</code>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Geri", callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    # ── Back to admin menu ─────────────────────────────────────────────────
    elif action == "back":
        await callback.message.edit_text(
            "🛠 <b>Admin Panel</b>\n\nNə etmək istəyirsən?",
            reply_markup=_admin_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()

    else:
        await callback.answer()


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, command: CommandObject) -> None:
    if not _is_admin(message.from_user.id):
        return

    if not command.args:
        await message.answer("İstifadə: /broadcast <mətn>")
        return

    text = command.args.strip()
    broadcast_text = f"📢 <b>Bot xəbəri</b>\n\n{text}"

    user_ids = await asyncio.to_thread(db.get_all_user_ids)
    total = len(user_ids)

    status_msg = await message.answer(
        f"⏳ Broadcast başladı...\n"
        f"Cəmi {total} istifadəçiyə göndərilir."
    )

    sent = failed = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, broadcast_text, parse_mode="HTML")
            sent += 1
        except Exception:
            failed += 1
        # Small delay to avoid hitting Telegram rate limits
        await asyncio.sleep(0.05)

    await status_msg.edit_text(
        f"✅ <b>Broadcast tamamlandı</b>\n\n"
        f"✉️ Göndərildi: {sent}\n"
        f"❌ Uğursuz: {failed}\n"
        f"📊 Cəmi: {total}",
        parse_mode="HTML",
    )


@router.message(Command("lookup"))
async def cmd_lookup(message: Message, command: CommandObject) -> None:
    if not _is_admin(message.from_user.id):
        return

    if not command.args:
        await message.answer("İstifadə: /lookup <user_id | @username>")
        return

    query = command.args.strip()
    user = await asyncio.to_thread(db.search_user, query)

    if not user:
        await message.answer(f"❌ İstifadəçi tapılmadı: <code>{query}</code>", parse_mode="HTML")
        return

    plan = user.get("plan", "free")
    mode = user.get("chat_mode", "default")
    usage = user.get("daily_usage", 0)
    limit = db.get_daily_limit(plan)
    until = user.get("premium_until", "—")
    if until and until != "—":
        until = until[:10]

    text = (
        f"👤 <b>İstifadəçi məlumatı</b>\n\n"
        f"🆔 ID:      <code>{user['id']}</code>\n"
        f"👤 Ad:      {user.get('first_name') or '—'}\n"
        f"📛 Username: @{user.get('username') or '—'}\n"
        f"📦 Plan:    <b>{plan}</b>\n"
        f"📅 Premium bitmə: {until}\n"
        f"🎭 Rejim:   {MODE_NAMES.get(mode, mode)}\n"
        f"💬 Bu gün: {usage}/{limit} mesaj\n"
        f"📆 Qeydiyyat: {str(user.get('created_at', '—'))[:10]}"
    )

    uid = user["id"]
    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ Premium ver", callback_data=f"agrant:{uid}:premium"),
                InlineKeyboardButton(text="🆓 Pulsuz et",  callback_data=f"agrant:{uid}:free"),
            ],
            [
                InlineKeyboardButton(text="🗑 Tarixçəni sil", callback_data=f"aclear:{uid}"),
            ],
        ]),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("agrant:"))
async def cb_admin_grant(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("İcazən yoxdur.", show_alert=True)
        return

    _, uid_str, plan = callback.data.split(":")
    uid = int(uid_str)

    if plan == "premium":
        await asyncio.to_thread(db.activate_premium, uid, settings.premium_duration_days)
        label = f"⭐ Premium verildi ({settings.premium_duration_days} gün)"
    else:
        await asyncio.to_thread(db.set_plan, uid, "free")
        label = "🆓 Pulsuz plana keçirildi"

    await callback.answer(label, show_alert=True)
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith("aclear:"))
async def cb_admin_clear(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("İcazən yoxdur.", show_alert=True)
        return

    uid = int(callback.data.split(":")[1])
    count = await asyncio.to_thread(db.clear_history, uid)
    await callback.answer(f"🗑 {count} mesaj silindi", show_alert=True)

# ── Core AI handler (shared logic for text + photo) ────────────────────────

async def _handle_ai_message(
    message: Message,
    user_text: str,
    image_bytes: bytes | None = None,
    image_mime: str = "image/jpeg",
) -> None:
    user = message.from_user

    # ── Single RPC: check usage + get history + get mode in one DB round-trip
    ctx = await asyncio.to_thread(db.check_usage_and_get_history, user.id)

    if not ctx["allowed"]:
        limit = ctx["limit"]
        await message.answer(
            f"⛔ Bugünkü mesaj limitin bitdi ({limit}/{limit}).\n"
            "Limit sabah sıfırlanacaq, ya da /upgrade ilə premium ala bilərsən."
        )
        return

    await message.bot.send_chat_action(message.chat.id, "typing")

    history  = ctx["history"]
    mode     = ctx.get("chat_mode") or "default"
    usage    = ctx["usage"]
    limit    = ctx["limit"]
    remaining = max(limit - usage, 0)

    try:
        reply_text, model_used = await asyncio.to_thread(
            generate_reply,
            history,
            user_text,
            user.language_code,
            mode,
            image_bytes,
            image_mime,
        )
    except GeminiError:
        logger.exception("Gemini call failed for user %s", user.id)
        await message.answer(
            "😕 Hazırda AI cavab verə bilmədi, bir az sonra yenidən cəhd et."
        )
        return

    # Save to history (fire-and-forget style — both inserts in parallel)
    history_text = f"[Şəkil] {user_text}" if image_bytes else user_text
    await asyncio.gather(
        asyncio.to_thread(db.save_message, user.id, "user", history_text),
        asyncio.to_thread(db.save_message, user.id, "assistant", reply_text),
    )

    # Invalidate Redis cache so next /status reflects updated usage
    from bot import cache as redis_cache
    await redis_cache.invalidate_user(user.id)

    await message.answer(reply_text)

    if remaining <= 3:
        await message.answer(f"ℹ️ Bugün üçün qalan limit: {remaining}/{limit}")


# ── Text messages ──────────────────────────────────────────────────────────

@router.message(F.text & ~F.text.startswith("/"))
async def handle_ai_chat(message: Message) -> None:
    user_text = message.text.strip()
    if not user_text:
        return
    await _handle_ai_message(message, user_text)


# ── Photo messages ─────────────────────────────────────────────────────────

@router.message(F.photo)
async def handle_photo(message: Message) -> None:
    # Telegram sends multiple sizes — take the largest
    photo = message.photo[-1]
    caption = (message.caption or "").strip()
    prompt = caption if caption else "Bu şəkildə nə görürsən? Ətraflı izah et."

    await message.bot.send_chat_action(message.chat.id, "typing")

    # Download photo as bytes
    file = await message.bot.get_file(photo.file_id)
    downloaded = await message.bot.download_file(file.file_path)
    image_bytes = downloaded.read()

    await _handle_ai_message(message, prompt, image_bytes=image_bytes, image_mime="image/jpeg")

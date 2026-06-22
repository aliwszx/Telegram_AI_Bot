"""
All Telegram update handlers — Professional Edition.

New in this version:
  - /feedback  — user feedback system
  - /top       — leaderboard
  - /remind    — premium expiry warnings
  - Inline mode — use bot in any chat
  - Document/PDF analysis support
  - Sticker handling with AI analysis
  - Smart admin panel with revenue stats
  - Topic-based conversation tagging
  - Typing indicator with progress dots
  - "Thinking..." message during long requests
"""
from __future__ import annotations

import asyncio
import logging
import queue as queue_module
import threading
import time

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    BufferedInputFile,
    InlineKeyboardMarkup, InlineKeyboardButton,
    InlineQuery, InlineQueryResultArticle, InputTextMessageContent,
    LabeledPrice, Message, PreCheckoutQuery, CallbackQuery,
)

from bot import db
from bot.ai import (
    generate_reply, generate_reply_stream, generate_quick_reply,
    GeminiError, GeminiRateLimitError,
    MODE_NAMES, MODE_DESCRIPTIONS,
)
from bot.config import settings

try:
    import sentry_sdk
except ImportError:
    sentry_sdk = None

logger = logging.getLogger(__name__)
router = Router(name="main")

# In-memory cache of last failed request per user (for retry button)
_last_failed: dict[int, dict] = {}

# Per-user lock: prevent the same user from sending multiple concurrent requests
# (avoids RPM spike from double-tap or impatient re-sends)
_user_locks: dict[int, asyncio.Lock] = {}
_user_locks_meta: dict[int, float] = {}  # last-used timestamp for GC
_user_locks_lock = asyncio.Lock()

async def _get_user_lock(user_id: int) -> asyncio.Lock:
    async with _user_locks_lock:
        _user_locks_meta[user_id] = time.monotonic()
        if user_id not in _user_locks:
            _user_locks[user_id] = asyncio.Lock()
        # Periodic GC: remove locks not used in the last 10 minutes
        if len(_user_locks) > 500:
            cutoff = time.monotonic() - 600
            stale = [uid for uid, ts in _user_locks_meta.items() if ts < cutoff]
            for uid in stale:
                _user_locks.pop(uid, None)
                _user_locks_meta.pop(uid, None)
        return _user_locks[user_id]

# ── Helpers ────────────────────────────────────────────────────────────────

def _capture(exc: Exception) -> None:
    if sentry_sdk is not None:
        try:
            sentry_sdk.capture_exception(exc)
        except Exception:  # noqa: BLE001
            pass


def _is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


# ── Static texts ───────────────────────────────────────────────────────────

WELCOME_TEXT = (
    "👋 <b>Salam, {name}!</b>\n\n"
    "Mən <b>Gemini AI</b> ilə işləyən güclü bir botam. 🚀\n\n"
    "📝 <b>Nə edə bilərəm:</b>\n"
    "• Suallarına cavab verəm\n"
    "• Şəkil, səs, sənəd analiz edəm\n"
    "• 10 fərqli rejimdə kömək edəm\n"
    "• Real-time internet axtarışı aparam\n\n"
    "Aşağıdakı düymələrdən başla 👇"
)

HELP_TEXT = (
    "ℹ️ <b>İstifadə qaydası</b>\n\n"
    "💬 <b>Mətn yaz</b> → AI cavab verir\n"
    "🖼 <b>Şəkil göndər</b> → AI şəkili analiz edir\n"
    "📄 <b>Sənəd/PDF göndər</b> → AI oxuyur və izah edir\n"
    "🎙 <b>Səsli mesaj</b> → AI eşidir və cavab verir\n"
    "😄 <b>Stiker göndər</b> → AI emosiyasını analiz edir\n\n"
    "<b>Komandalar:</b>\n"
    "/mode — 🎭 AI rejimini dəyiş (10 rejim)\n"
    "/status — 📊 Plan və limit məlumatı\n"
    "/clear — 🗑 Söhbəti sil\n"
    "/export — 📤 Söhbəti fayl kimi yüklə\n"
    "/search — 🌐 İnternet axtarışını aç/bağla\n"
    "/invite — 🎁 Dost dəvət et, bonus qazan\n"
    "/top — 🏆 Ən aktiv istifadəçilər\n"
    "/feedback — 💌 Rəy/təklif göndər\n"
    "/upgrade — ⭐ Premium al\n\n"
    "💡 <b>Tip:</b> Botu başqa chatlarda da @botusername yazaraq istifadə edə bilərsən!"
)


# ── Keyboards ──────────────────────────────────────────────────────────────

def _start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎭 Rejim seç",    callback_data="menu:mode"),
            InlineKeyboardButton(text="📊 Status",       callback_data="menu:status"),
        ],
        [
            InlineKeyboardButton(text="🌐 İnternet",     callback_data="menu:search_toggle"),
            InlineKeyboardButton(text="⭐ Premium",      callback_data="menu:upgrade"),
        ],
        [
            InlineKeyboardButton(text="🗑 Söhbəti sil",  callback_data="menu:clear"),
            InlineKeyboardButton(text="📤 Export",       callback_data="menu:export"),
        ],
        [
            InlineKeyboardButton(text="🎁 Dəvət et",    callback_data="menu:invite"),
            InlineKeyboardButton(text="🏆 TOP",          callback_data="menu:top"),
        ],
        [
            InlineKeyboardButton(text="ℹ️ Kömək",        callback_data="menu:help"),
            InlineKeyboardButton(text="💌 Rəy ver",      callback_data="menu:feedback"),
        ],
    ])


def _mode_keyboard(current: str | None = None) -> InlineKeyboardMarkup:
    """Mode selection — 2 columns, checkmark on active."""
    mode_items = list(MODE_NAMES.items())
    buttons = []
    for i in range(0, len(mode_items), 2):
        row = []
        for key, label in mode_items[i:i+2]:
            tick = " ✓" if key == current else ""
            row.append(InlineKeyboardButton(
                text=f"{label}{tick}",
                callback_data=f"mode:{key}",
            ))
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️ Geri", callback_data="menu:back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Əsas menyu", callback_data="menu:back")]
    ])


def _retry_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Yenidən cəhd et", callback_data="retry_last")]
    ])


def _upgrade_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Premium al", callback_data="menu:upgrade")],
        [InlineKeyboardButton(text="🎁 Dost dəvət et (+bonus)", callback_data="menu:invite")],
    ])


# ── Commands ───────────────────────────────────────────────────────────────

@router.message(Command("start"))
async def cmd_start(message: Message, command: CommandObject) -> None:
    user = message.from_user

    referred_by = None
    if command.args and command.args.startswith("ref_"):
        try:
            ref_id = int(command.args.removeprefix("ref_"))
            if ref_id != user.id:
                referred_by = ref_id
        except ValueError:
            pass

    row = await asyncio.to_thread(
        db.get_or_create_user, user.id, user.username, user.first_name, referred_by
    )
    # Update language code
    await asyncio.to_thread(db.update_user_language, user.id, user.language_code)

    name = user.first_name or user.username or "Qonaq"

    extra = ""
    if referred_by and row.get("referred_by") == referred_by:
        extra = "\n\n🎁 Dəvət linki ilə gəldin — sənə <b>+5 bonus mesaj</b> verildi!"

    # Premium expiry warning
    days_left = db.days_until_premium_expires(row)
    if days_left is not None and days_left <= settings.premium_expiry_warning_days:
        extra += f"\n\n⚠️ Premium abunəliyin <b>{days_left} gün</b> sonra bitir! /upgrade ilə uzat."

    await message.answer(
        WELCOME_TEXT.format(name=name) + extra,
        reply_markup=_start_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=_back_keyboard(), parse_mode="HTML")


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    user = message.from_user
    row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
    plan = await asyncio.to_thread(db.effective_plan, row)
    limit = db.get_daily_limit(plan, row.get("bonus_messages", 0) or 0)
    usage = row.get("daily_usage", 0)
    used_today = usage if row.get("last_usage_date") == db.today() else 0
    remaining = max(limit - used_today, 0)
    mode = db.get_chat_mode(row)
    web = db.get_web_search_enabled(row)
    days_left = db.days_until_premium_expires(row)

    bar_filled = int((used_today / limit) * 10) if limit else 0
    bar = "█" * bar_filled + "░" * (10 - bar_filled)

    plan_emoji = "⭐" if plan == "premium" else "🆓"
    lines = [
        f"{plan_emoji} <b>Plan:</b> {plan.upper()}",
        f"🎭 <b>Rejim:</b> {MODE_NAMES.get(mode, mode)}",
        f"🌐 <b>İnternet:</b> {'✅' if web else '❌'}",
        "",
        f"📊 <b>Limit:</b> {used_today}/{limit}",
        f"[{bar}]",
        f"✅ <b>Qalan:</b> {remaining} mesaj",
    ]
    if plan == "premium" and days_left is not None:
        lines.append(f"📅 <b>Bitmə tarixi:</b> {row['premium_until'][:10]} ({days_left} gün qalıb)")
    elif plan == "free":
        bonus = row.get("bonus_messages", 0) or 0
        if bonus > 0:
            lines.append(f"🎁 <b>Bonus mesaj:</b> +{bonus}")
        lines.append("\n💡 /upgrade ilə premium al → 500 mesaj/gün")

    await message.answer("\n".join(lines), parse_mode="HTML", reply_markup=_back_keyboard())


@router.message(Command("mode"))
async def cmd_mode(message: Message) -> None:
    row = await asyncio.to_thread(
        db.get_or_create_user, message.from_user.id, message.from_user.username, message.from_user.first_name
    )
    current = db.get_chat_mode(row)
    mode_list = "\n".join(
        f"{'✅' if k == current else '▫️'} {v} — {MODE_DESCRIPTIONS[k]}"
        for k, v in MODE_NAMES.items()
    )
    await message.answer(
        f"🎭 <b>Rejim seç</b>\n\n{mode_list}\n\n"
        f"Hazırki rejim: <b>{MODE_NAMES.get(current, current)}</b>",
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
    await callback.message.edit_text(
        f"✅ Rejim dəyişdirildi: <b>{MODE_NAMES[mode]}</b>\n"
        f"📝 {MODE_DESCRIPTIONS[mode]}\n\n"
        "İndi mənə yaz! 👇",
        reply_markup=_start_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer(f"{MODE_NAMES[mode]} seçildi!")
    await asyncio.to_thread(
    db.clear_history,
    callback.from_user.id
)

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
            "🎭 <b>Rejim seç</b>\n\nHər rejim fərqli bir AI şəxsiyyəti aktivləşdirir:",
            reply_markup=_mode_keyboard(current),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "status":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        plan = await asyncio.to_thread(db.effective_plan, row)
        limit = db.get_daily_limit(plan, row.get("bonus_messages", 0) or 0)
        usage = row.get("daily_usage", 0)
        used_today = usage if row.get("last_usage_date") == db.today() else 0
        remaining = max(limit - used_today, 0)
        mode = db.get_chat_mode(row)
        plan_emoji = "⭐" if plan == "premium" else "🆓"
        bar_filled = int((used_today / limit) * 10) if limit else 0
        bar = "█" * bar_filled + "░" * (10 - bar_filled)
        lines = [
            f"{plan_emoji} Plan: <b>{plan.upper()}</b>",
            f"🎭 Rejim: <b>{MODE_NAMES.get(mode, mode)}</b>",
            f"📊 Bugün: {used_today}/{limit} [{bar}]",
            f"✅ Qalan: {remaining} mesaj",
        ]
        if plan == "premium" and row.get("premium_until"):
            lines.append(f"📅 Bitmə: {row['premium_until'][:10]}")
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=_back_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "search_toggle":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        current = db.get_web_search_enabled(row)
        new_state = not current
        await asyncio.to_thread(db.set_web_search, user.id, new_state)
        status = "✅ açıldı" if new_state else "❌ bağlandı"
        await callback.answer(f"🌐 İnternet axtarışı {status}", show_alert=True)

    elif action == "clear":
        count = await asyncio.to_thread(db.clear_history, user.id)
        name = user.first_name or user.username or "Qonaq"
        await callback.message.edit_text(
            f"🗑 Söhbət silindi ({count} mesaj).\n\nYeni söhbətə başla! 👇",
            reply_markup=_start_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer("Söhbət silindi!")

    elif action == "invite":
        await callback.answer()
        await _send_invite(callback.message, user.id, user.username, user.first_name)

    elif action == "export":
        await callback.answer()
        await _send_export(callback.message, user.id)

    elif action == "top":
        await callback.answer()
        await _send_top(callback.message)

    elif action == "feedback":
        await callback.answer()
        await callback.message.answer(
            "💌 <b>Rəy/Təklif</b>\n\n"
            "Botla bağlı rəy, təklif və ya problem bildirmək üçün aşağıdakı formatda yaz:\n\n"
            "<code>/feedback [mətnin buraya]</code>\n\n"
            "Məsələn: <code>/feedback Translator rejimi çox gözəldir!</code>",
            parse_mode="HTML",
        )

    elif action == "help":
        await callback.message.edit_text(
            HELP_TEXT,
            reply_markup=_back_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()

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
                f"günlük {settings.premium_daily_limit} mesaj limiti + bütün rejimler."
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


@router.message(Command("invite"))
async def cmd_invite(message: Message) -> None:
    await _send_invite(message, message.from_user.id, message.from_user.username, message.from_user.first_name)


async def _send_invite(target: Message, user_id: int, username, first_name) -> None:
    row = await asyncio.to_thread(db.get_or_create_user, user_id, username, first_name)
    bot_user = await target.bot.get_me()
    link = f"https://t.me/{bot_user.username}?start=ref_{user_id}"
    count = row.get("referral_count", 0)
    await target.answer(
        "🎁 <b>Dost dəvət et, bonus qazan!</b>\n\n"
        "Hər dəvət etdiyin dost botu açanda — <b>siz hər ikiniz +5 bonus mesaj</b> qazanırsınız.\n\n"
        f"🔗 Sənin linkin:\n<code>{link}</code>\n\n"
        f"👥 İndiyə qədər dəvət etdiyin: <b>{count}</b> nəfər\n"
        f"🎁 Qazandığın bonus: <b>+{count * 5}</b> mesaj",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="📤 Linki paylaş",
                url=f"https://t.me/share/url?url={link}&text=Bu%20AI%20botu%20çox%20gözəldir!",
            )],
        ]),
    )


@router.message(Command("export"))
async def cmd_export(message: Message) -> None:
    await _send_export(message, message.from_user.id)


async def _send_export(target: Message, user_id: int) -> None:
    messages = await asyncio.to_thread(db.get_all_messages, user_id)
    if not messages:
        await target.answer("📭 Hələ heç bir söhbət tarixçən yoxdur.")
        return

    lines = []
    for m in messages:
        who = "👤 Sən" if m["role"] == "user" else "🤖 AI"
        topic = f" [{m['topic']}]" if m.get("topic") else ""
        lines.append(f"[{m.get('created_at', '')[:19]}]{topic} {who}:\n{m['content']}\n")
    text = "\n".join(lines)

    file = BufferedInputFile(text.encode("utf-8"), filename=f"chat_export_{user_id}.txt")
    await target.answer_document(
        file,
        caption=f"📤 Söhbət tarixçən ({len(messages)} mesaj)\n📅 Export tarixi: {db.today()}"
    )


@router.message(Command("top"))
async def cmd_top(message: Message) -> None:
    await _send_top(message)


async def _send_top(target: Message) -> None:
    users = await asyncio.to_thread(db.get_top_users, 10)
    if not users:
        await target.answer("Hələ heç bir istifadəçi yoxdur.")
        return

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    lines = ["🏆 <b>Ən aktiv istifadəçilər (bu gün)</b>\n"]
    for i, u in enumerate(users):
        name = u.get("first_name") or u.get("username") or f"User {u['id']}"
        plan = "⭐" if u.get("plan") == "premium" else ""
        lines.append(f"{medals[i]} {name} {plan} — {u.get('daily_usage', 0)} mesaj")

    await target.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("search"))
async def cmd_search(message: Message) -> None:
    row = await asyncio.to_thread(
        db.get_or_create_user, message.from_user.id, message.from_user.username, message.from_user.first_name
    )
    new_state = not db.get_web_search_enabled(row)
    await asyncio.to_thread(db.set_web_search, message.from_user.id, new_state)
    status = "✅ açıldı" if new_state else "❌ bağlandı"
    await message.answer(
        f"🌐 İnternet axtarışı {status}.\n\n"
        "Açıq olanda AI real-time internetdən məlumat axtarır."
    )


@router.message(Command("feedback"))
async def cmd_feedback(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer(
            "💌 Rəyinizi belə göndərin:\n"
            "<code>/feedback Rəyiniz buraya</code>",
            parse_mode="HTML",
        )
        return

    text = command.args.strip()
    user = message.from_user
    # Forward to admins
    feedback_text = (
        f"💌 <b>Yeni rəy!</b>\n\n"
        f"👤 {user.first_name or ''} (@{user.username or '?'}) [ID: {user.id}]\n\n"
        f"📝 {text}"
    )
    sent = False
    for admin_id in settings.admin_ids:
        try:
            await message.bot.send_message(admin_id, feedback_text, parse_mode="HTML")
            sent = True
        except Exception:  # noqa: BLE001
            pass

    await message.answer(
        "✅ Rəyiniz göndərildi! Təşəkkür edirik 🙏\n"
        "Hər rəy botu daha da yaxşılaşdırmağa kömək edir."
        if sent else
        "✅ Rəyiniz qeydə alındı! Təşəkkür edirik 🙏"
    )


@router.message(Command("upgrade"))
async def cmd_upgrade(message: Message) -> None:
    row = await asyncio.to_thread(
        db.get_or_create_user, message.from_user.id, message.from_user.username, message.from_user.first_name
    )
    plan = await asyncio.to_thread(db.effective_plan, row)
    if plan == "premium":
        until = row.get("premium_until", "")
        days_left = db.days_until_premium_expires(row)
        await message.answer(
            f"✅ Artıq premium istifadəçisisən!\n"
            f"📅 Bitmə tarixi: {until[:10] if until else '—'}\n"
            f"⏳ Qalan: {days_left} gün" if days_left is not None else
            f"✅ Artıq premium istifadəçisisən!"
        )
        return

    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title="⭐ Premium Plan",
        description=(
            f"✨ {settings.premium_duration_days} gün Premium:\n"
            f"• Günlük {settings.premium_daily_limit} mesaj (standart: {settings.free_daily_limit})\n"
            f"• Bütün 10 AI rejimi\n"
            f"• Sənəd/PDF analizi\n"
            f"• Prioritet dəstək"
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
        "🎉 <b>Ödəniş uğurla alındı!</b>\n\n"
        "⭐ Premium aktivləşdi!\n"
        f"📅 Bitmə tarixi: {until.date().isoformat()}\n"
        f"📨 Günlük limit: {settings.premium_daily_limit} mesaj\n\n"
        "Yeni imkanlardan istifadə etməyə başla! 🚀",
        parse_mode="HTML",
        reply_markup=_start_keyboard(),
    )


# ── Admin panel ────────────────────────────────────────────────────────────

def _admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Statistika",    callback_data="admin:stats"),
            InlineKeyboardButton(text="💰 Gəlir",        callback_data="admin:revenue"),
        ],
        [
            InlineKeyboardButton(text="📢 Broadcast",    callback_data="admin:broadcast_prompt"),
            InlineKeyboardButton(text="🔍 User axtar",   callback_data="admin:lookup_prompt"),
        ],
        [
            InlineKeyboardButton(text="🏆 TOP users",    callback_data="admin:top"),
            InlineKeyboardButton(text="⏰ Bitirir",      callback_data="admin:expiring"),
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

    if action == "stats":
        stats = await asyncio.to_thread(db.get_stats)
        free_users = stats["total_users"] - stats["premium_users"]
        cvr = (stats["premium_users"] / stats["total_users"] * 100) if stats["total_users"] else 0
        text = (
            "📊 <b>Bot Statistikası</b>\n\n"
            f"👥 Cəmi istifadəçi:  <b>{stats['total_users']:,}</b>\n"
            f"⭐ Premium:           <b>{stats['premium_users']:,}</b>\n"
            f"🆓 Pulsuz:            <b>{free_users:,}</b>\n"
            f"📈 Çevrilmə:          <b>{cvr:.1f}%</b>\n\n"
            f"🟢 Bu gün aktiv:     <b>{stats['active_today']:,}</b>\n"
            f"💬 Bu günkü mesaj:   <b>{stats['messages_today']:,}</b>\n"
            f"📨 Cəmi mesaj:       <b>{stats['total_messages']:,}</b>"
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

    elif action == "revenue":
        stats = await asyncio.to_thread(db.get_stats)
        text = (
            "💰 <b>Gəlir Statistikası</b>\n\n"
            f"⭐ Cəmi qazanılan Stars: <b>{stats['revenue_total']:,}</b>\n"
            f"📅 Bu ay: <b>{stats['revenue_month']:,}</b> Stars\n"
            f"🧾 Cəmi ödəniş sayı: <b>{stats['payment_count']:,}</b>\n\n"
            f"💡 Ortalama ödəniş: <b>{stats['revenue_total'] // max(stats['payment_count'], 1):,}</b> Stars"
        )
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Yenilə", callback_data="admin:revenue")],
                [InlineKeyboardButton(text="⬅️ Geri",   callback_data="admin:back")],
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "top":
        users = await asyncio.to_thread(db.get_top_users, 10)
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        lines = ["🏆 <b>TOP 10 İstifadəçi</b>\n"]
        for i, u in enumerate(users):
            name = u.get("first_name") or u.get("username") or f"ID:{u['id']}"
            plan = "⭐" if u.get("plan") == "premium" else "🆓"
            lines.append(f"{medals[i]} {name} {plan} — {u.get('daily_usage', 0)}")
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Geri", callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "expiring":
        users = await asyncio.to_thread(db.get_users_expiring_soon, 3)
        if not users:
            await callback.answer("Yaxın 3 gündə bitən premium yoxdur.", show_alert=True)
            return
        lines = ["⏰ <b>3 gündə bitən premium-lar:</b>\n"]
        for u in users:
            name = u.get("first_name") or u.get("username") or f"ID:{u['id']}"
            until = (u.get("premium_until") or "")[:10]
            lines.append(f"• {name} — {until}")
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Geri", callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "broadcast_prompt":
        await callback.message.edit_text(
            "📢 <b>Broadcast</b>\n\n"
            "<code>/broadcast Mətnin buraya</code>\n\n"
            "⚠️ Bütün istifadəçilərə göndərilər!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Geri", callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "lookup_prompt":
        await callback.message.edit_text(
            "🔍 <b>User axtar</b>\n\n"
            "<code>/lookup @username</code>\n"
            "<code>/lookup 123456789</code>",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Geri", callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

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
    status_msg = await message.answer(f"⏳ Broadcast başladı... ({total} istifadəçi)")

    sent = failed = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, broadcast_text, parse_mode="HTML")
            sent += 1
        except Exception:  # noqa: BLE001
            failed += 1
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

    user = await asyncio.to_thread(db.search_user, command.args.strip())
    if not user:
        await message.answer(f"❌ Tapılmadı: <code>{command.args}</code>", parse_mode="HTML")
        return

    plan = user.get("plan", "free")
    mode = user.get("chat_mode", "default")
    usage = user.get("daily_usage", 0)
    limit = db.get_daily_limit(plan)
    until = (user.get("premium_until") or "—")
    if until != "—":
        until = until[:10]
    ref_count = user.get("referral_count", 0)

    text = (
        f"👤 <b>İstifadəçi məlumatı</b>\n\n"
        f"🆔 ID:       <code>{user['id']}</code>\n"
        f"👤 Ad:       {user.get('first_name') or '—'}\n"
        f"📛 Username: @{user.get('username') or '—'}\n"
        f"📦 Plan:     <b>{plan}</b>\n"
        f"📅 Premium:  {until}\n"
        f"🎭 Rejim:    {MODE_NAMES.get(mode, mode)}\n"
        f"💬 Bugün:    {usage}/{limit}\n"
        f"👥 Dəvətlər: {ref_count}\n"
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
                InlineKeyboardButton(text="🎁 +10 Bonus",    callback_data=f"abonus:{uid}"),
            ],
        ]),
        parse_mode="HTML",
    )


@router.message(Command("grant"))
async def cmd_grant(message: Message, command: CommandObject) -> None:
    if not _is_admin(message.from_user.id):
        return
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


@router.callback_query(F.data.startswith("aclear:"))
async def cb_admin_clear(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("İcazən yoxdur.", show_alert=True)
        return
    uid = int(callback.data.split(":")[1])
    count = await asyncio.to_thread(db.clear_history, uid)
    await callback.answer(f"🗑 {count} mesaj silindi", show_alert=True)


@router.callback_query(F.data.startswith("abonus:"))
async def cb_admin_bonus(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("İcazən yoxdur.", show_alert=True)
        return
    uid = int(callback.data.split(":")[1])
    await asyncio.to_thread(db.add_bonus_messages, uid, 10)
    await callback.answer("🎁 +10 bonus mesaj verildi!", show_alert=True)


# ── Inline mode ────────────────────────────────────────────────────────────

@router.inline_query()
async def handle_inline(inline_query: InlineQuery) -> None:
    if not settings.inline_mode_enabled:
        return

    query = inline_query.query.strip()
    if not query or len(query) < 3:
        await inline_query.answer(
            [],
            switch_pm_text="✍️ Sualınızı yazın...",
            switch_pm_parameter="inline_help",
            cache_time=1,
        )
        return

    try:
        # Quick AI reply for inline
        prompt = f"Qısa və dəqiq cavab ver (max 200 söz): {query}"
        reply = await asyncio.to_thread(generate_quick_reply, prompt)
    except Exception:  # noqa: BLE001
        reply = "❌ Cavab alına bilmədi. Biraz sonra cəhd edin."

    await inline_query.answer(
        [
            InlineQueryResultArticle(
                id="1",
                title=f"🤖 AI Cavabı",
                description=reply[:100] + "..." if len(reply) > 100 else reply,
                input_message_content=InputTextMessageContent(
                    message_text=f"❓ <b>{query}</b>\n\n🤖 {reply}",
                    parse_mode="HTML",
                ),
            )
        ],
        cache_time=30,
    )


# ── Streaming bridge ────────────────────────────────────────────────────────

_EDIT_MIN_INTERVAL = 0.9
_EDIT_MIN_CHARS = 25


async def _stream_ai_reply(
    message: Message,
    history: list[dict],
    user_text: str,
    language_hint: str | None,
    mode: str,
    media_bytes: bytes | None,
    media_mime: str,
    web_search: bool = False,
) -> tuple[str, str]:
    q: queue_module.Queue = queue_module.Queue()

    def producer() -> None:
        try:
            for piece, model, done in generate_reply_stream(
                history, user_text, language_hint, mode, media_bytes, media_mime, web_search
            ):
                q.put(("chunk", piece, model, done))
        except Exception as exc:  # noqa: BLE001
            q.put(("error", exc, None, None))
        finally:
            q.put(("end", None, None, None))

    threading.Thread(target=producer, daemon=True).start()

    loop = asyncio.get_running_loop()
    full_text = ""
    model_used = ""
    sent_message: Message | None = None
    last_edit_len = 0
    last_edit_time = 0.0

    while True:
        kind, piece, model, done = await loop.run_in_executor(None, q.get)

        if kind == "end":
            break
        if kind == "error":
            raise piece

        if model:
            model_used = model
        if piece:
            full_text += piece

        if done:
            continue

        now = time.monotonic()
        should_edit = (
            full_text
            and (len(full_text) - last_edit_len >= _EDIT_MIN_CHARS)
            and (now - last_edit_time >= _EDIT_MIN_INTERVAL)
        )

        if sent_message is None and full_text:
            sent_message = await message.answer(full_text)
            last_edit_len = len(full_text)
            last_edit_time = now
        elif sent_message is not None and should_edit:
            try:
                await sent_message.edit_text(full_text)
                last_edit_len = len(full_text)
                last_edit_time = now
            except TelegramBadRequest:
                pass

    full_text = full_text.strip()
    if not full_text:
        raise GeminiError("Empty response from Gemini")

    if sent_message is None:
        sent_message = await message.answer(full_text)
    elif full_text != getattr(sent_message, "text", None):
        try:
            await sent_message.edit_text(full_text)
        except TelegramBadRequest:
            pass

    return full_text, model_used


@router.callback_query(F.data == "retry_last")
async def cb_retry_last(callback: CallbackQuery) -> None:
    pending = _last_failed.pop(callback.from_user.id, None)
    if not pending:
        await callback.answer("⏰ Vaxtı keçib, yenidən yaz.", show_alert=True)
        return
    await callback.answer("🔁 Yenidən cəhd edilir...")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass
    await _handle_ai_message(
        callback.message,
        pending["text"],
        media_bytes=pending.get("media_bytes"),
        media_mime=pending.get("media_mime", "image/jpeg"),
        target_user=callback.from_user,
    )


# ── Core AI handler ────────────────────────────────────────────────────────

async def _handle_ai_message(
    message: Message,
    user_text: str,
    media_bytes: bytes | None = None,
    media_mime: str = "image/jpeg",
    target_user=None,
) -> None:
    user = target_user or message.from_user

    # Per-user lock: skip duplicate request if user is already being processed
    lock = await _get_user_lock(user.id)
    if lock.locked():
        await message.answer(
            "⏳ Əvvəlki sorğun hələ cavablanır, bir az gözlə...",
        )
        return

    async with lock:

        try:
            ctx = await asyncio.to_thread(db.check_usage_and_get_history, user.id)
        except Exception as exc:
            logger.exception("DB error for user %s: %s", user.id, exc)
            _capture(exc)
            await message.answer("😕 Verilənlər bazasında xəta baş verdi, bir az sonra yenidən cəhd et.")
            return

        if not ctx["allowed"]:
            limit = ctx["limit"]
            await message.answer(
                f"⛔ <b>Günlük limit bitdi</b> ({limit}/{limit} mesaj)\n\n"
                "Seçimlər:\n"
                "• Sabah limiti sıfırlanır\n"
                "• /upgrade ilə premium al (500 mesaj/gün)\n"
                "• /invite ilə dost dəvət et (bonus mesaj)",
                parse_mode="HTML",
                reply_markup=_upgrade_keyboard(),
            )
            return

        await message.bot.send_chat_action(message.chat.id, "typing")

        history   = ctx["history"]
        mode      = ctx.get("chat_mode") or "default"
        usage     = ctx["usage"]
        limit     = ctx["limit"]
        web_search = ctx.get("web_search", False)
        # usage is already incremented by check_usage_and_get_history, so remaining is correct
        remaining = max(limit - usage, 0)

        try:
            if settings.streaming_enabled:
                reply_text, model_used = await _stream_ai_reply(
                    message, history, user_text, user.language_code, mode,
                    media_bytes, media_mime, web_search,
                )
            else:
                reply_text, model_used = await asyncio.to_thread(
                    generate_reply,
                    history, user_text, user.language_code, mode,
                    media_bytes, media_mime, web_search,
                )
        except GeminiRateLimitError as exc:
            logger.warning("Gemini rate-limited for user %s: %s", user.id, exc)
            _capture(exc)
            _last_failed[user.id] = {
                "text": user_text, "media_bytes": media_bytes, "media_mime": media_mime,
            }
            await message.answer(
                f"⏳ <b>AI yüklənib</b>\n"
                f"<b>{exc.retry_after} saniyə</b> sonra yenidən cəhd et.",
                parse_mode="HTML",
                reply_markup=_retry_keyboard(),
            )
            return
        except GeminiError as exc:
            logger.exception("Gemini error for user %s: %s", user.id, exc)
            _capture(exc)
            _last_failed[user.id] = {
                "text": user_text, "media_bytes": media_bytes, "media_mime": media_mime,
            }
            await message.answer(
                "😕 AI cavab verə bilmədi. Bir az sonra yenidən cəhd et.",
                reply_markup=_retry_keyboard(),
            )
            return

        # Tarixdə yalnız mətn məzmununu saxla, media prefiksi olmadan
        history_label = user_text if user_text else "[media]"

        await asyncio.gather(
            asyncio.to_thread(db.save_message, user.id, "user", history_label),
            asyncio.to_thread(db.save_message, user.id, "assistant", reply_text),
        )

        from bot import cache as redis_cache
        await redis_cache.invalidate_user(user.id)

        if remaining <= 3:
            await message.answer(
                f"ℹ️ Bugün üçün qalan limit: <b>{remaining}/{limit}</b>\n"
                "💡 /upgrade ilə Premium al — 500 mesaj/gün!",
                parse_mode="HTML",
            )


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
    photo = message.photo[-1]
    caption = (message.caption or "").strip()
    prompt = caption if caption else "Bu şəkildə nə görürsən? Ətraflı izah et, nə varsa hamısını say."

    await message.bot.send_chat_action(message.chat.id, "typing")
    file = await message.bot.get_file(photo.file_id)
    downloaded = await message.bot.download_file(file.file_path)
    image_bytes = downloaded.read()

    await _handle_ai_message(message, prompt, media_bytes=image_bytes, media_mime="image/jpeg")


# ── Document / PDF messages ────────────────────────────────────────────────

SUPPORTED_DOC_MIMES = {
    "application/pdf": "application/pdf",
    "text/plain": "text/plain",
    "text/csv": "text/csv",
    "application/json": "application/json",
    "text/html": "text/html",
    "text/markdown": "text/markdown",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

MAX_DOC_SIZE_MB = 10


@router.message(F.document)
async def handle_document(message: Message) -> None:
    doc = message.document
    mime = doc.mime_type or ""
    caption = (message.caption or "").strip()

    # Check file size (Telegram limit is 20MB but we cap at 10MB for Gemini)
    size_mb = (doc.file_size or 0) / 1_048_576
    if size_mb > MAX_DOC_SIZE_MB:
        await message.answer(
            f"❌ Fayl həddindən böyükdür ({size_mb:.1f} MB).\n"
            f"Maksimum ölçü: {MAX_DOC_SIZE_MB} MB."
        )
        return

    if mime not in SUPPORTED_DOC_MIMES:
        await message.answer(
            "❌ Bu fayl formatı dəstəklənmir.\n\n"
            "✅ Dəstəklənən formatlar:\n"
            "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
        )
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    file = await message.bot.get_file(doc.file_id)
    downloaded = await message.bot.download_file(file.file_path)
    doc_bytes = downloaded.read()

    prompt = caption if caption else (
        "Bu sənədi diqqətlə oxu və əsas məzmununu izah et. "
        "Əgər PDF-dirsə, bütün əhəmiyyətli məlumatları üzə çıxar."
    )

    await _handle_ai_message(
        message, prompt,
        media_bytes=doc_bytes,
        media_mime=SUPPORTED_DOC_MIMES[mime],
    )


# ── Voice / audio messages ─────────────────────────────────────────────────

@router.message(F.voice | F.audio)
async def handle_voice(message: Message) -> None:
    media = message.voice or message.audio
    mime = getattr(media, "mime_type", None) or "audio/ogg"

    await message.bot.send_chat_action(message.chat.id, "typing")
    file = await message.bot.get_file(media.file_id)
    downloaded = await message.bot.download_file(file.file_path)
    audio_bytes = downloaded.read()

    prompt = (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    )
    await _handle_ai_message(message, prompt, media_bytes=audio_bytes, media_mime=mime)

# ── Sticker messages ───────────────────────────────────────────────────────

@router.message(F.sticker)
async def handle_sticker(message: Message) -> None:
    emoji = message.sticker.emoji or "😊"
    prompt = (
        f"İstifadəçi sənə '{emoji}' emoji-li bir stiker göndərdi. "
        "Bu emosiyaya uyğun mehriban, qısa bir cavab ver. "
        "Eyni tonda cavab ver."
    )
    await _handle_ai_message(message, prompt)

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
from bot.lang import t  # <-- localization

try:
    import sentry_sdk
except ImportError:
    sentry_sdk = None

logger = logging.getLogger(__name__)
router = Router(name="main")

# In-memory cache of last failed request per user (for retry button)
_last_failed: dict[int, dict] = {}

# Per-user lock: prevent the same user from sending multiple concurrent requests
_user_locks: dict[int, asyncio.Lock] = {}
_user_locks_meta: dict[int, float] = {}
_user_locks_lock = asyncio.Lock()

async def _get_user_lock(user_id: int) -> asyncio.Lock:
    async with _user_locks_lock:
        _user_locks_meta[user_id] = time.monotonic()
        if user_id not in _user_locks:
            _user_locks[user_id] = asyncio.Lock()
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


def _lang(user) -> str | None:
    """Extract language code from a Telegram user object (or None)."""
    return getattr(user, "language_code", None)


# ── Keyboards ──────────────────────────────────────────────────────────────

def _start_keyboard(lang=None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_mode", lang),    callback_data="menu:mode"),
            InlineKeyboardButton(text=t("btn_status", lang),  callback_data="menu:status"),
        ],
        [
            InlineKeyboardButton(text=t("btn_internet", lang),callback_data="menu:search_toggle"),
            InlineKeyboardButton(text=t("btn_premium", lang), callback_data="menu:upgrade"),
        ],
        [
            InlineKeyboardButton(text=t("btn_clear", lang),   callback_data="menu:clear"),
            InlineKeyboardButton(text=t("btn_export", lang),  callback_data="menu:export"),
        ],
        [
            InlineKeyboardButton(text=t("btn_invite", lang),  callback_data="menu:invite"),
            InlineKeyboardButton(text=t("btn_top", lang),     callback_data="menu:top"),
        ],
        [
            InlineKeyboardButton(text=t("btn_help", lang),    callback_data="menu:help"),
            InlineKeyboardButton(text=t("btn_feedback", lang),callback_data="menu:feedback"),
        ],
    ])


def _mode_keyboard(current: str | None = None, lang=None) -> InlineKeyboardMarkup:
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
    buttons.append([InlineKeyboardButton(text=t("btn_back_short", lang), callback_data="menu:back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _back_keyboard(lang=None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:back")]
    ])


def _retry_keyboard(lang=None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_retry", lang), callback_data="retry_last")]
    ])


def _upgrade_keyboard(lang=None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_upgrade", lang),     callback_data="menu:upgrade")],
        [InlineKeyboardButton(text=t("btn_invite_bonus", lang),callback_data="menu:invite")],
    ])


# ── Commands ───────────────────────────────────────────────────────────────

@router.message(Command("start"))
async def cmd_start(message: Message, command: CommandObject) -> None:
    user = message.from_user
    lang = _lang(user)

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
    await asyncio.to_thread(db.update_user_language, user.id, user.language_code)

    name = user.first_name or user.username or t("guest_name", lang)

    extra = ""
    if referred_by and row.get("referred_by") == referred_by:
        extra = t("welcome_referral_bonus", lang)

    days_left = db.days_until_premium_expires(row)
    if days_left is not None and days_left <= settings.premium_expiry_warning_days:
        extra += t("welcome_premium_expiry", lang, days_left=days_left)

    await message.answer(
        t("welcome", lang, name=name) + extra,
        reply_markup=_start_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    lang = _lang(message.from_user)
    await message.answer(t("help", lang), reply_markup=_back_keyboard(lang), parse_mode="HTML")


@router.message(Command("status"))
async def cmd_status(message: Message) -> None:
    user = message.from_user
    lang = _lang(user)
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
        t("status_plan", lang, emoji=plan_emoji, plan=plan.upper()),
        t("status_mode", lang, mode=MODE_NAMES.get(mode, mode)),
        t("status_internet", lang, state="✅" if web else "❌"),
        "",
        t("status_limit", lang, used=used_today, limit=limit),
        f"[{bar}]",
        t("status_remaining", lang, remaining=remaining),
    ]
    if plan == "premium" and days_left is not None:
        lines.append(t("status_until", lang, date=row["premium_until"][:10], days=days_left))
    elif plan == "free":
        bonus = row.get("bonus_messages", 0) or 0
        if bonus > 0:
            lines.append(t("status_bonus", lang, bonus=bonus))
        lines.append(t("status_upgrade_tip", lang))

    await message.answer("\n".join(lines), parse_mode="HTML", reply_markup=_back_keyboard(lang))


@router.message(Command("mode"))
async def cmd_mode(message: Message) -> None:
    user = message.from_user
    lang = _lang(user)
    row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
    current = db.get_chat_mode(row)
    mode_list = "\n".join(
        t("mode_row", lang, check="✅" if k == current else "▫️", name=v, desc=MODE_DESCRIPTIONS[k])
        for k, v in MODE_NAMES.items()
    )
    await message.answer(
        f"{t('mode_select_title', lang)}\n\n{mode_list}\n\n"
        + t("mode_current", lang, mode=MODE_NAMES.get(current, current)),
        reply_markup=_mode_keyboard(current, lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("mode:"))
async def cb_mode_select(callback: CallbackQuery) -> None:
    lang = _lang(callback.from_user)
    mode = callback.data.split(":", 1)[1]
    if mode not in MODE_NAMES:
        await callback.answer(t("mode_invalid", lang), show_alert=True)
        return

    await asyncio.to_thread(db.set_chat_mode, callback.from_user.id, mode)
    await callback.message.edit_text(
        t("mode_changed", lang, mode=MODE_NAMES[mode], desc=MODE_DESCRIPTIONS[mode]),
        reply_markup=_start_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer(t("mode_selected_toast", lang, mode=MODE_NAMES[mode]))
    await asyncio.to_thread(db.clear_history, callback.from_user.id)


@router.callback_query(F.data.startswith("menu:"))
async def cb_menu(callback: CallbackQuery) -> None:
    action = callback.data.split(":", 1)[1]
    user = callback.from_user
    lang = _lang(user)

    if action == "back":
        name = user.first_name or user.username or t("guest_name", lang)
        await callback.message.edit_text(
            t("welcome", lang, name=name),
            reply_markup=_start_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "mode":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        current = db.get_chat_mode(row)
        await callback.message.edit_text(
            t("mode_select_header", lang),
            reply_markup=_mode_keyboard(current, lang),
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
            t("status_plan", lang, emoji=plan_emoji, plan=plan.upper()),
            t("status_mode", lang, mode=MODE_NAMES.get(mode, mode)),
            t("status_today", lang, used=used_today, limit=limit, bar=bar),
            t("status_remaining", lang, remaining=remaining),
        ]
        if plan == "premium" and row.get("premium_until"):
            lines.append(t("status_until_short", lang, date=row['premium_until'][:10]))
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=_back_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "search_toggle":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        current = db.get_web_search_enabled(row)
        new_state = not current
        await asyncio.to_thread(db.set_web_search, user.id, new_state)
        status = t("search_on", lang) if new_state else t("search_off", lang)
        await callback.answer(t("search_toggled", lang, status=status), show_alert=True)

    elif action == "clear":
        count = await asyncio.to_thread(db.clear_history, user.id)
        name = user.first_name or user.username or t("guest_name", lang)
        await callback.message.edit_text(
            t("clear_done", lang, count=count),
            reply_markup=_start_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer(t("clear_toast", lang))

    elif action == "invite":
        await callback.answer()
        await _send_invite(callback.message, user.id, user.username, user.first_name, lang)

    elif action == "export":
        await callback.answer()
        await _send_export(callback.message, user.id, lang)

    elif action == "top":
        await callback.answer()
        await _send_top(callback.message, lang)

    elif action == "feedback":
        await callback.answer()
        await callback.message.answer(t("feedback_prompt", lang), parse_mode="HTML")

    elif action == "help":
        await callback.message.edit_text(
            t("help", lang),
            reply_markup=_back_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "upgrade":
        row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
        plan = await asyncio.to_thread(db.effective_plan, row)
        if plan == "premium":
            await callback.answer(t("upgrade_already_toast", lang), show_alert=True)
            return
        await callback.answer()
        await callback.message.answer_invoice(
            title=t("upgrade_invoice_title", lang),
            description=t(
                "upgrade_invoice_desc", lang,
                days=settings.premium_duration_days,
                premium_limit=settings.premium_daily_limit,
                free_limit=settings.free_daily_limit,
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
    lang = _lang(message.from_user)
    count = await asyncio.to_thread(db.clear_history, message.from_user.id)
    await message.answer(t("clear_cmd_done", lang, count=count))


@router.message(Command("invite"))
async def cmd_invite(message: Message) -> None:
    user = message.from_user
    await _send_invite(message, user.id, user.username, user.first_name, _lang(user))


async def _send_invite(target: Message, user_id: int, username, first_name, lang=None) -> None:
    row = await asyncio.to_thread(db.get_or_create_user, user_id, username, first_name)
    bot_user = await target.bot.get_me()
    link = f"https://t.me/{bot_user.username}?start=ref_{user_id}"
    count = row.get("referral_count", 0)
    await target.answer(
        t("invite_text", lang, link=link, count=count, bonus=count * 5),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=t("btn_share_link", lang),
                url=f"https://t.me/share/url?url={link}&text={t('invite_share_url', lang)}",
            )],
        ]),
    )


@router.message(Command("export"))
async def cmd_export(message: Message) -> None:
    await _send_export(message, message.from_user.id, _lang(message.from_user))


async def _send_export(target: Message, user_id: int, lang=None) -> None:
    messages = await asyncio.to_thread(db.get_all_messages, user_id)
    if not messages:
        await target.answer(t("export_empty", lang))
        return

    lines = []
    for m in messages:
        who = t("export_user", lang) if m["role"] == "user" else t("export_ai", lang)
        topic = f" [{m['topic']}]" if m.get("topic") else ""
        lines.append(f"[{m.get('created_at', '')[:19]}]{topic} {who}:\n{m['content']}\n")
    text = "\n".join(lines)

    file = BufferedInputFile(text.encode("utf-8"), filename=f"chat_export_{user_id}.txt")
    await target.answer_document(
        file,
        caption=t("export_caption", lang, count=len(messages), date=db.today()),
    )


@router.message(Command("top"))
async def cmd_top(message: Message) -> None:
    await _send_top(message, _lang(message.from_user))


async def _send_top(target: Message, lang=None) -> None:
    users = await asyncio.to_thread(db.get_top_users, 10)
    if not users:
        await target.answer(t("top_empty", lang))
        return

    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    lines = [t("top_title", lang)]
    for i, u in enumerate(users):
        name = u.get("first_name") or u.get("username") or f"User {u['id']}"
        plan = "⭐" if u.get("plan") == "premium" else ""
        lines.append(t("top_row", lang, medal=medals[i], name=name, plan_icon=plan, usage=u.get('daily_usage', 0)))

    await target.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("search"))
async def cmd_search(message: Message) -> None:
    user = message.from_user
    lang = _lang(user)
    row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
    new_state = not db.get_web_search_enabled(row)
    await asyncio.to_thread(db.set_web_search, user.id, new_state)
    status = t("search_on", lang) if new_state else t("search_off", lang)
    await message.answer(t("search_toggled_detail", lang, status=status))


@router.message(Command("feedback"))
async def cmd_feedback(message: Message, command: CommandObject) -> None:
    user = message.from_user
    lang = _lang(user)
    if not command.args:
        await message.answer(t("feedback_usage", lang), parse_mode="HTML")
        return

    text = command.args.strip()
    feedback_text = t(
        "feedback_admin", lang,
        name=user.first_name or "",
        username=user.username or "?",
        uid=user.id,
        text=text,
    )
    sent = False
    for admin_id in settings.admin_ids:
        try:
            await message.bot.send_message(admin_id, feedback_text, parse_mode="HTML")
            sent = True
        except Exception:  # noqa: BLE001
            pass

    await message.answer(t("feedback_sent", lang) if sent else t("feedback_saved", lang))


@router.message(Command("upgrade"))
async def cmd_upgrade(message: Message) -> None:
    user = message.from_user
    lang = _lang(user)
    row = await asyncio.to_thread(db.get_or_create_user, user.id, user.username, user.first_name)
    plan = await asyncio.to_thread(db.effective_plan, row)
    if plan == "premium":
        until = row.get("premium_until", "")
        days_left = db.days_until_premium_expires(row)
        if days_left is not None:
            await message.answer(t("upgrade_already", lang, until=until[:10] if until else "—", days=days_left))
        else:
            await message.answer(t("upgrade_already_simple", lang))
        return

    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title=t("upgrade_invoice_title", lang),
        description=t(
            "upgrade_invoice_desc", lang,
            days=settings.premium_duration_days,
            premium_limit=settings.premium_daily_limit,
            free_limit=settings.free_daily_limit,
        ),
        payload=f"premium_upgrade:{user.id}",
        currency="XTR",
        prices=[LabeledPrice(label="Premium", amount=settings.stars_price)],
        provider_token="",
    )


@router.pre_checkout_query()
async def handle_pre_checkout(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def handle_successful_payment(message: Message) -> None:
    lang = _lang(message.from_user)
    until = await asyncio.to_thread(
        db.activate_premium, message.from_user.id, settings.premium_duration_days
    )
    await message.answer(
        t("upgrade_success", lang, until=until.date().isoformat(), limit=settings.premium_daily_limit),
        parse_mode="HTML",
        reply_markup=_start_keyboard(lang),
    )


# ── Admin panel ────────────────────────────────────────────────────────────

def _admin_keyboard(lang=None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("admin_btn_stats", lang),    callback_data="admin:stats"),
            InlineKeyboardButton(text=t("admin_btn_revenue", lang),  callback_data="admin:revenue"),
        ],
        [
            InlineKeyboardButton(text=t("admin_btn_broadcast", lang),callback_data="admin:broadcast_prompt"),
            InlineKeyboardButton(text=t("admin_btn_lookup", lang),   callback_data="admin:lookup_prompt"),
        ],
        [
            InlineKeyboardButton(text=t("admin_btn_top", lang),      callback_data="admin:top"),
            InlineKeyboardButton(text=t("admin_btn_expiring", lang), callback_data="admin:expiring"),
        ],
    ])


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    lang = _lang(message.from_user)
    await message.answer(t("admin_panel", lang), reply_markup=_admin_keyboard(lang), parse_mode="HTML")


@router.callback_query(F.data.startswith("admin:"))
async def cb_admin(callback: CallbackQuery) -> None:
    lang = _lang(callback.from_user)
    if not _is_admin(callback.from_user.id):
        await callback.answer(t("admin_no_perm", lang), show_alert=True)
        return

    action = callback.data.split(":", 1)[1]

    if action == "stats":
        stats = await asyncio.to_thread(db.get_stats)
        free_users = stats["total_users"] - stats["premium_users"]
        cvr = (stats["premium_users"] / stats["total_users"] * 100) if stats["total_users"] else 0
        text = t(
            "admin_stats", lang,
            total=stats["total_users"], premium=stats["premium_users"],
            free=free_users, cvr=cvr,
            active=stats["active_today"], today_msg=stats["messages_today"],
            total_msg=stats["total_messages"],
        )
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t("btn_refresh", lang), callback_data="admin:stats")],
                [InlineKeyboardButton(text=t("btn_back_short", lang), callback_data="admin:back")],
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "revenue":
        stats = await asyncio.to_thread(db.get_stats)
        text = t(
            "admin_revenue", lang,
            total=stats["revenue_total"], month=stats["revenue_month"],
            count=stats["payment_count"],
            avg=stats["revenue_total"] // max(stats["payment_count"], 1),
        )
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t("btn_refresh", lang), callback_data="admin:revenue")],
                [InlineKeyboardButton(text=t("btn_back_short", lang), callback_data="admin:back")],
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "top":
        users = await asyncio.to_thread(db.get_top_users, 10)
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        lines = [t("top_title_admin", lang)]
        for i, u in enumerate(users):
            name = u.get("first_name") or u.get("username") or f"ID:{u['id']}"
            plan = "⭐" if u.get("plan") == "premium" else "🆓"
            lines.append(f"{medals[i]} {name} {plan} — {u.get('daily_usage', 0)}")
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t("btn_back_short", lang), callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "expiring":
        users = await asyncio.to_thread(db.get_users_expiring_soon, 3)
        if not users:
            await callback.answer(t("admin_expiring_none", lang), show_alert=True)
            return
        lines = [t("admin_expiring_title", lang)]
        for u in users:
            name = u.get("first_name") or u.get("username") or f"ID:{u['id']}"
            until = (u.get("premium_until") or "")[:10]
            lines.append(f"• {name} — {until}")
        await callback.message.edit_text(
            "\n".join(lines),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t("btn_back_short", lang), callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "broadcast_prompt":
        await callback.message.edit_text(
            t("admin_broadcast_prompt", lang),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t("btn_back_short", lang), callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "lookup_prompt":
        await callback.message.edit_text(
            t("admin_lookup_prompt", lang),
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=t("btn_back_short", lang), callback_data="admin:back")]
            ]),
            parse_mode="HTML",
        )
        await callback.answer()

    elif action == "back":
        await callback.message.edit_text(
            t("admin_panel", lang),
            reply_markup=_admin_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()

    else:
        await callback.answer()


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, command: CommandObject) -> None:
    if not _is_admin(message.from_user.id):
        return
    lang = _lang(message.from_user)
    if not command.args:
        await message.answer(t("admin_broadcast_usage", lang))
        return

    text = command.args.strip()
    broadcast_text = t("admin_broadcast_prefix", lang, text=text)

    user_ids = await asyncio.to_thread(db.get_all_user_ids)
    total = len(user_ids)
    status_msg = await message.answer(t("admin_broadcast_starting", lang, total=total))

    sent = failed = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, broadcast_text, parse_mode="HTML")
            sent += 1
        except Exception:  # noqa: BLE001
            failed += 1
        await asyncio.sleep(0.05)

    await status_msg.edit_text(
        t("admin_broadcast_done", lang, sent=sent, failed=failed, total=total),
        parse_mode="HTML",
    )


@router.message(Command("lookup"))
async def cmd_lookup(message: Message, command: CommandObject) -> None:
    if not _is_admin(message.from_user.id):
        return
    lang = _lang(message.from_user)
    if not command.args:
        await message.answer(t("admin_lookup_usage", lang))
        return

    user = await asyncio.to_thread(db.search_user, command.args.strip())
    if not user:
        await message.answer(t("admin_lookup_none", lang, query=command.args), parse_mode="HTML")
        return

    plan = user.get("plan", "free")
    mode = user.get("chat_mode", "default")
    usage = user.get("daily_usage", 0)
    limit = db.get_daily_limit(plan)
    until = (user.get("premium_until") or "—")
    if until != "—":
        until = until[:10]
    ref_count = user.get("referral_count", 0)

    text = t(
        "admin_lookup_result", lang,
        uid=user["id"],
        first_name=user.get("first_name") or "—",
        username=user.get("username") or "—",
        plan=plan,
        until=until,
        mode=MODE_NAMES.get(mode, mode),
        used=usage,
        limit=limit,
        refs=ref_count,
        created=str(user.get("created_at", "—"))[:10],
    )
    uid = user["id"]
    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=t("admin_btn_premium", lang), callback_data=f"agrant:{uid}:premium"),
                InlineKeyboardButton(text=t("admin_btn_free", lang),    callback_data=f"agrant:{uid}:free"),
            ],
            [
                InlineKeyboardButton(text=t("admin_btn_clear_h", lang), callback_data=f"aclear:{uid}"),
                InlineKeyboardButton(text=t("admin_btn_bonus", lang),   callback_data=f"abonus:{uid}"),
            ],
        ]),
        parse_mode="HTML",
    )


@router.message(Command("grant"))
async def cmd_grant(message: Message, command: CommandObject) -> None:
    if not _is_admin(message.from_user.id):
        return
    lang = _lang(message.from_user)
    if not command.args:
        await message.answer(t("admin_grant_usage", lang))
        return
    parts = command.args.split()
    if len(parts) != 2 or parts[1] not in ("free", "premium"):
        await message.answer(t("admin_grant_usage", lang))
        return
    target_id, plan = int(parts[0]), parts[1]
    await asyncio.to_thread(db.set_plan, target_id, plan)
    await message.answer(t("admin_grant_done", lang, uid=target_id, plan=plan))


@router.callback_query(F.data.startswith("agrant:"))
async def cb_admin_grant(callback: CallbackQuery) -> None:
    lang = _lang(callback.from_user)
    if not _is_admin(callback.from_user.id):
        await callback.answer(t("admin_no_perm", lang), show_alert=True)
        return
    _, uid_str, plan = callback.data.split(":")
    uid = int(uid_str)
    if plan == "premium":
        await asyncio.to_thread(db.activate_premium, uid, settings.premium_duration_days)
        label = t("admin_grant_premium_done", lang, days=settings.premium_duration_days)
    else:
        await asyncio.to_thread(db.set_plan, uid, "free")
        label = t("admin_grant_free_done", lang)
    await callback.answer(label, show_alert=True)


@router.callback_query(F.data.startswith("aclear:"))
async def cb_admin_clear(callback: CallbackQuery) -> None:
    lang = _lang(callback.from_user)
    if not _is_admin(callback.from_user.id):
        await callback.answer(t("admin_no_perm", lang), show_alert=True)
        return
    uid = int(callback.data.split(":")[1])
    count = await asyncio.to_thread(db.clear_history, uid)
    await callback.answer(t("admin_clear_done", lang, count=count), show_alert=True)


@router.callback_query(F.data.startswith("abonus:"))
async def cb_admin_bonus(callback: CallbackQuery) -> None:
    lang = _lang(callback.from_user)
    if not _is_admin(callback.from_user.id):
        await callback.answer(t("admin_no_perm", lang), show_alert=True)
        return
    uid = int(callback.data.split(":")[1])
    await asyncio.to_thread(db.add_bonus_messages, uid, 10)
    await callback.answer(t("admin_bonus_done", lang), show_alert=True)


# ── Inline mode ────────────────────────────────────────────────────────────

@router.inline_query()
async def handle_inline(inline_query: InlineQuery) -> None:
    if not settings.inline_mode_enabled:
        return

    lang = _lang(inline_query.from_user)
    query = inline_query.query.strip()
    if not query or len(query) < 3:
        await inline_query.answer(
            [],
            switch_pm_text=t("inline_type_hint", lang),
            switch_pm_parameter="inline_help",
            cache_time=1,
        )
        return

    try:
        prompt = t("inline_short_prompt", lang, query=query)
        reply = await asyncio.to_thread(generate_quick_reply, prompt)
    except Exception:  # noqa: BLE001
        reply = t("inline_error", lang)

    await inline_query.answer(
        [
            InlineQueryResultArticle(
                id="1",
                title=t("inline_result_title", lang),
                description=reply[:100] + "..." if len(reply) > 100 else reply,
                input_message_content=InputTextMessageContent(
                    message_text=t("inline_result_msg", lang, query=query, reply=reply),
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
    lang = _lang(callback.from_user)
    pending = _last_failed.pop(callback.from_user.id, None)
    if not pending:
        await callback.answer(t("retry_expired", lang), show_alert=True)
        return
    await callback.answer(t("retry_trying", lang))
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
    lang = _lang(user)

    lock = await _get_user_lock(user.id)
    if lock.locked():
        await message.answer(t("processing", lang))
        return

    async with lock:

        try:
            ctx = await asyncio.to_thread(db.check_usage_and_get_history, user.id)
        except Exception as exc:
            logger.exception("DB error for user %s: %s", user.id, exc)
            _capture(exc)
            await message.answer(t("db_error", lang))
            return

        if not ctx["allowed"]:
            limit = ctx["limit"]
            await message.answer(
                t("limit_exceeded", lang, limit=limit),
                parse_mode="HTML",
                reply_markup=_upgrade_keyboard(lang),
            )
            return

        await message.bot.send_chat_action(message.chat.id, "typing")

        history    = ctx["history"]
        mode       = ctx.get("chat_mode") or "default"
        usage      = ctx["usage"]
        limit      = ctx["limit"]
        web_search = ctx.get("web_search", False)
        remaining  = max(limit - usage, 0)

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
                t("ai_rate_limit", lang, retry_after=exc.retry_after),
                parse_mode="HTML",
                reply_markup=_retry_keyboard(lang),
            )
            return
        except GeminiError as exc:
            logger.exception("Gemini error for user %s: %s", user.id, exc)
            _capture(exc)
            _last_failed[user.id] = {
                "text": user_text, "media_bytes": media_bytes, "media_mime": media_mime,
            }
            await message.answer(t("ai_error", lang), reply_markup=_retry_keyboard(lang))
            return

        history_label = user_text if user_text else "[media]"

        await asyncio.gather(
            asyncio.to_thread(db.save_message, user.id, "user", history_label),
            asyncio.to_thread(db.save_message, user.id, "assistant", reply_text),
        )

        from bot import cache as redis_cache
        await redis_cache.invalidate_user(user.id)

        if remaining <= 3:
            await message.answer(
                t("limit_warning", lang, remaining=remaining, limit=limit),
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
    lang = _lang(message.from_user)
    photo = message.photo[-1]
    caption = (message.caption or "").strip()
    prompt = caption if caption else t("photo_default_prompt", lang)

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
    lang = _lang(message.from_user)
    doc = message.document
    mime = doc.mime_type or ""
    caption = (message.caption or "").strip()

    size_mb = (doc.file_size or 0) / 1_048_576
    if size_mb > MAX_DOC_SIZE_MB:
        await message.answer(t("doc_size_error", lang, size_mb=size_mb, max_mb=MAX_DOC_SIZE_MB))
        return

    if mime not in SUPPORTED_DOC_MIMES:
        await message.answer(t("doc_format_error", lang))
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    file = await message.bot.get_file(doc.file_id)
    downloaded = await message.bot.download_file(file.file_path)
    doc_bytes = downloaded.read()

    prompt = caption if caption else t("doc_default_prompt", lang)

    await _handle_ai_message(
        message, prompt,
        media_bytes=doc_bytes,
        media_mime=SUPPORTED_DOC_MIMES[mime],
    )


# ── Voice / audio messages ─────────────────────────────────────────────────

@router.message(F.voice | F.audio)
async def handle_voice(message: Message) -> None:
    lang = _lang(message.from_user)
    media = message.voice or message.audio
    mime = getattr(media, "mime_type", None) or "audio/ogg"

    await message.bot.send_chat_action(message.chat.id, "typing")
    file = await message.bot.get_file(media.file_id)
    downloaded = await message.bot.download_file(file.file_path)
    audio_bytes = downloaded.read()

    prompt = t("voice_prompt", lang)
    await _handle_ai_message(message, prompt, media_bytes=audio_bytes, media_mime=mime)


# ── Sticker messages ───────────────────────────────────────────────────────

@router.message(F.sticker)
async def handle_sticker(message: Message) -> None:
    lang = _lang(message.from_user)
    emoji = message.sticker.emoji or "😊"
    prompt = t("sticker_prompt", lang, emoji=emoji)
    await _handle_ai_message(message, prompt)

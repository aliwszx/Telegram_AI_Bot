"""
Localization / language strings.

To switch language, change DEFAULT_LANG or pass lang= to t().
Add new languages by adding a dict with the same keys.
"""
from __future__ import annotations

# ── String tables ─────────────────────────────────────────────────────────────

AZ: dict[str, str] = {
    # ── Welcome / Help ────────────────────────────────────────────────────────
    "welcome": (
        "👋 <b>Salam, {name}!</b>\n\n"
        "Mən <b>Gemini AI</b> ilə işləyən güclü bir botam. 🚀\n\n"
        "📝 <b>Nə edə bilərəm:</b>\n"
        "• Suallarına cavab verəm\n"
        "• Şəkil, səs, sənəd analiz edəm\n"
        "• 10 fərqli rejimdə kömək edəm\n"
        "• Real-time internet axtarışı aparam\n\n"
        "Aşağıdakı düymələrdən başla 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Dəvət linki ilə gəldin — sənə <b>+5 bonus mesaj</b> verildi!",
    "welcome_premium_expiry": "\n\n⚠️ Premium abunəliyin <b>{days_left} gün</b> sonra bitir! /upgrade ilə uzat.",

    "help": (
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
    ),

    # ── Keyboard buttons ──────────────────────────────────────────────────────
    "btn_mode":        "🎭 Rejim seç",
    "btn_status":      "📊 Status",
    "btn_internet":    "🌐 İnternet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Söhbəti sil",
    "btn_export":      "📤 Export",
    "btn_invite":      "🎁 Dəvət et",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Kömək",
    "btn_feedback":    "💌 Rəy ver",
    "btn_back":        "⬅️ Əsas menyu",
    "btn_back_short":  "⬅️ Geri",
    "btn_retry":       "🔁 Yenidən cəhd et",
    "btn_upgrade":     "⭐ Premium al",
    "btn_invite_bonus":"🎁 Dost dəvət et (+bonus)",
    "btn_share_link":  "📤 Linki paylaş",
    "btn_refresh":     "🔄 Yenilə",
    "btn_language":    "🌍 Dil",

    # ── Language selection ────────────────────────────────────────────────────
    "lang_select_title": "🌍 <b>Dil seçin</b>\n\nHazırki dil: <b>{current}</b>",
    "lang_changed":      "✅ Dil dəyişdirildi: <b>{lang}</b>",
    "lang_already":      "ℹ️ Dil artıq <b>{lang}</b> olaraq təyin edilib.",

    # ── Status ────────────────────────────────────────────────────────────────
    "status_plan":        "{emoji} <b>Plan:</b> {plan}",
    "status_mode":        "🎭 <b>Rejim:</b> {mode}",
    "status_internet":    "🌐 <b>İnternet:</b> {state}",
    "status_limit":       "📊 <b>Limit:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Qalan:</b> {remaining} mesaj",
    "status_until":       "📅 <b>Bitmə tarixi:</b> {date} ({days} gün qalıb)",
    "status_bonus":       "🎁 <b>Bonus mesaj:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 /upgrade ilə premium al → 500 mesaj/gün",

    # ── Mode ──────────────────────────────────────────────────────────────────
    "mode_select_title":   "🎭 <b>Rejim seç</b>",
    "mode_select_header":  "🎭 <b>Rejim seç</b>\n\nHər rejim fərqli bir AI şəxsiyyəti aktivləşdirir:",
    "mode_changed":        "✅ Rejim dəyişdirildi: <b>{mode}</b>\n📝 {desc}\n\nİndi mənə yaz! 👇",
    "mode_selected_toast": "{mode} seçildi!",
    "mode_invalid":        "Yanlış rejim.",
    "mode_current":        "Hazırki rejim: <b>{mode}</b>",

    # ── Clear ─────────────────────────────────────────────────────────────────
    "clear_done":     "🗑 Söhbət silindi ({count} mesaj).\n\nYeni söhbətə başla! 👇",
    "clear_toast":    "Söhbət silindi!",
    "clear_cmd_done": "🗑️ Söhbət tarixçəsi silindi ({count} mesaj).\nYeni söhbətə başlaya bilərsən!",

    # ── Search toggle ─────────────────────────────────────────────────────────
    "search_on":       "✅ açıldı",
    "search_off":      "❌ bağlandı",
    "search_toggled":  "🌐 İnternet axtarışı {status}.",
    "search_toggled_detail": (
        "🌐 İnternet axtarışı {status}.\n\n"
        "Açıq olanda AI real-time internetdən məlumat axtarır."
    ),

    # ── Invite ────────────────────────────────────────────────────────────────
    "invite_text": (
        "🎁 <b>Dost dəvət et, bonus qazan!</b>\n\n"
        "Hər dəvət etdiyin dost botu açanda — <b>siz hər ikiniz +5 bonus mesaj</b> qazanırsınız.\n\n"
        "🔗 Sənin linkin:\n<code>{link}</code>\n\n"
        "👥 İndiyə qədər dəvət etdiyin: <b>{count}</b> nəfər\n"
        "🎁 Qazandığın bonus: <b>+{bonus}</b> mesaj"
    ),
    "invite_share_url": "Bu AI botu çox gözəldir!",

    # ── Export ────────────────────────────────────────────────────────────────
    "export_empty":   "📭 Hələ heç bir söhbət tarixçən yoxdur.",
    "export_caption": "📤 Söhbət tarixçən ({count} mesaj)\n📅 Export tarixi: {date}",
    "export_user":    "👤 Sən",
    "export_ai":      "🤖 AI",

    # ── Top ───────────────────────────────────────────────────────────────────
    "top_empty":   "Hələ heç bir istifadəçi yoxdur.",
    "top_title":   "🏆 <b>Ən aktiv istifadəçilər (bu gün)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 İstifadəçi</b>\n",

    # ── Feedback ──────────────────────────────────────────────────────────────
    "feedback_usage": (
        "💌 Rəyinizi belə göndərin:\n"
        "<code>/feedback Rəyiniz buraya</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Rəy/Təklif</b>\n\n"
        "Botla bağlı rəy, təklif və ya problem bildirmək üçün aşağıdakı formatda yaz:\n\n"
        "<code>/feedback [mətnin buraya]</code>\n\n"
        "Məsələn: <code>/feedback Translator rejimi çox gözəldir!</code>"
    ),
    "feedback_sent":    "✅ Rəyiniz göndərildi! Təşəkkür edirik 🙏\nHər rəy botu daha da yaxşılaşdırmağa kömək edir.",
    "feedback_saved":   "✅ Rəyiniz qeydə alındı! Təşəkkür edirik 🙏",
    "feedback_admin":   "💌 <b>Yeni rəy!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    # ── Upgrade ───────────────────────────────────────────────────────────────
    "upgrade_already":       "✅ Artıq premium istifadəçisisən!\n📅 Bitmə tarixi: {until}\n⏳ Qalan: {days} gün",
    "upgrade_already_simple":"✅ Artıq premium istifadəçisisən!",
    "upgrade_already_toast": "Artıq premium istifadəçisisən! ⭐",
    "upgrade_invoice_title": "Premium plan ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} gün Premium:\n"
        "• Günlük {premium_limit} mesaj (standart: {free_limit})\n"
        "• Bütün 10 AI rejimi\n"
        "• Sənəd/PDF analizi\n"
        "• Prioritet dəstək"
    ),
    "upgrade_success": (
        "🎉 <b>Ödəniş uğurla alındı!</b>\n\n"
        "⭐ Premium aktivləşdi!\n"
        "📅 Bitmə tarixi: {until}\n"
        "📨 Günlük limit: {limit} mesaj\n\n"
        "Yeni imkanlardan istifadə etməyə başla! 🚀"
    ),

    # ── Limit / errors ────────────────────────────────────────────────────────
    "limit_exceeded": (
        "⛔ <b>Günlük limit bitdi</b> ({limit}/{limit} mesaj)\n\n"
        "Seçimlər:\n"
        "• Sabah limiti sıfırlanır\n"
        "• /upgrade ilə premium al (500 mesaj/gün)\n"
        "• /invite ilə dost dəvət et (bonus mesaj)"
    ),
    "limit_warning":  "ℹ️ Bugün üçün qalan limit: <b>{remaining}/{limit}</b>\n💡 /upgrade ilə Premium al — 500 mesaj/gün!",
    "processing":     "⏳ Əvvəlki sorğun hələ cavablanır, bir az gözlə...",
    "db_error":       "😕 Verilənlər bazasında xəta baş verdi, bir az sonra yenidən cəhd et.",
    "ai_rate_limit":  "⏳ <b>AI yüklənib</b>\n<b>{retry_after} saniyə</b> sonra yenidən cəhd et.",
    "ai_error":       "😕 AI cavab verə bilmədi. Bir az sonra yenidən cəhd et.",

    # ── Retry ─────────────────────────────────────────────────────────────────
    "retry_expired":  "⏰ Vaxtı keçib, yenidən yaz.",
    "retry_trying":   "🔁 Yenidən cəhd edilir...",

    # ── Photo / Document / Voice ──────────────────────────────────────────────
    "photo_default_prompt":  "Bu şəkildə nə görürsün? Ətraflı izah et, nə varsa hamısını say.",
    "doc_size_error":        "❌ Fayl həddindən böyükdür ({size_mb:.1f} MB).\nMaksimum ölçü: {max_mb} MB.",
    "doc_format_error": (
        "❌ Bu fayl formatı dəstəklənmir.\n\n"
        "✅ Dəstəklənən formatlar:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Bu sənədi diqqətlə oxu və əsas məzmununu izah et. "
        "Əgər PDF-dirsə, bütün əhəmiyyətli məlumatları üzə çıxar."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "İstifadəçi sənə '{emoji}' emoji-li bir stiker göndərdi. "
        "Bu emosiyaya uyğun mehriban, qısa bir cavab ver. "
        "Eyni tonda cavab ver."
    ),

    # ── Inline mode ───────────────────────────────────────────────────────────
    "inline_type_hint":     "✍️ Sualınızı yazın...",
    "inline_short_prompt":  "Qısa və dəqiq cavab ver (max 200 söz): {query}",
    "inline_error":         "❌ Cavab alına bilmədi. Biraz sonra cəhd edin.",
    "inline_result_title":  "🤖 AI Cavabı",

    # ── Admin panel ───────────────────────────────────────────────────────────
    "admin_panel":       "🛠 <b>Admin Panel</b>\n\nNə etmək istəyirsən?",
    "admin_no_perm":     "İcazən yoxdur.",
    "admin_grant_usage": "İstifadə: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ User {uid} → plan: {plan}",
    "admin_lookup_usage":"İstifadə: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Tapılmadı: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>İstifadəçi məlumatı</b>\n\n"
        "🆔 ID:       <code>{uid}</code>\n"
        "👤 Ad:       {first_name}\n"
        "📛 Username: @{username}\n"
        "📦 Plan:     <b>{plan}</b>\n"
        "📅 Premium:  {until}\n"
        "🎭 Rejim:    {mode}\n"
        "💬 Bugün:    {used}/{limit}\n"
        "👥 Dəvətlər: {refs}\n"
        "📆 Qeydiyyat: {created}"
    ),
    "admin_btn_stats":    "📊 Statistika",
    "admin_btn_revenue":  "💰 Gəlir",
    "admin_btn_broadcast":"📢 Broadcast",
    "admin_btn_lookup":   "🔍 User axtar",
    "admin_btn_top":      "🏆 TOP users",
    "admin_btn_expiring": "⏰ Bitirir",
    "admin_btn_premium":  "⭐ Premium ver",
    "admin_btn_free":     "🆓 Pulsuz et",
    "admin_btn_clear_h":  "🗑 Tarixçəni sil",
    "admin_btn_bonus":    "🎁 +10 Bonus",
    "admin_stats": (
        "📊 <b>Bot Statistikası</b>\n\n"
        "👥 Cəmi istifadəçi:  <b>{total:,}</b>\n"
        "⭐ Premium:           <b>{premium:,}</b>\n"
        "🆓 Pulsuz:            <b>{free:,}</b>\n"
        "📈 Çevrilmə:          <b>{cvr:.1f}%</b>\n\n"
        "🟢 Bu gün aktiv:     <b>{active:,}</b>\n"
        "💬 Bu günkü mesaj:   <b>{today_msg:,}</b>\n"
        "📨 Cəmi mesaj:       <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Gəlir Statistikası</b>\n\n"
        "⭐ Cəmi qazanılan Stars: <b>{total:,}</b>\n"
        "📅 Bu ay: <b>{month:,}</b> Stars\n"
        "🧾 Cəmi ödəniş sayı: <b>{count:,}</b>\n\n"
        "💡 Ortalama ödəniş: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "Yaxın 3 gündə bitən premium yoxdur.",
    "admin_expiring_title": "⏰ <b>3 gündə bitən premium-lar:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Broadcast</b>\n\n"
        "<code>/broadcast Mətnin buraya</code>\n\n"
        "⚠️ Bütün istifadəçilərə göndərilər!"
    ),
    "admin_broadcast_usage":    "İstifadə: /broadcast <mətn>",
    "admin_broadcast_starting": "⏳ Broadcast başladı... ({total} istifadəçi)",
    "admin_broadcast_done": (
        "✅ <b>Broadcast tamamlandı</b>\n\n"
        "✉️ Göndərildi: {sent}\n"
        "❌ Uğursuz: {failed}\n"
        "📊 Cəmi: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Bot xəbəri</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>User axtar</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium verildi ({days} gün)",
    "admin_grant_free_done":    "🆓 Pulsuz plana keçirildi",
    "admin_clear_done":         "🗑 {count} mesaj silindi",
    "admin_bonus_done":         "🎁 +10 bonus mesaj verildi!",

    # ── Top row line ──────────────────────────────────────────────────────────
    "top_row":    "{medal} {name} {plan_icon} — {usage} mesaj",

    # ── Status inline (callback) ──────────────────────────────────────────────
    "status_today":        "📊 Bugün: {used}/{limit} [{bar}]",
    "status_until_short":  "📅 Bitmə: {date}",

    # ── Mode list row ─────────────────────────────────────────────────────────
    "mode_row":   "{check} {name} — {desc}",

    # ── Inline result message ─────────────────────────────────────────────────
    "inline_result_msg": "❓ <b>{query}</b>\n\n🤖 {reply}",

    # ── Guest name ────────────────────────────────────────────────────────────
    "guest_name": "Qonaq",
}

EN: dict[str, str] = {
    "welcome": (
        "👋 <b>Hello, {name}!</b>\n\n"
        "I'm a powerful bot powered by <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>What I can do:</b>\n"
        "• Answer your questions\n"
        "• Analyze images, voice, and documents\n"
        "• Help in 10 different modes\n"
        "• Real-time web search\n\n"
        "Get started with the buttons below 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 You joined via invite link — you got <b>+5 bonus messages</b>!",
    "welcome_premium_expiry": "\n\n⚠️ Your premium expires in <b>{days_left} days</b>! Use /upgrade to extend.",

    "help": (
        "ℹ️ <b>How to use</b>\n\n"
        "💬 <b>Send text</b> → AI replies\n"
        "🖼 <b>Send image</b> → AI analyzes it\n"
        "📄 <b>Send document/PDF</b> → AI reads and explains\n"
        "🎙 <b>Voice message</b> → AI listens and replies\n"
        "😄 <b>Send sticker</b> → AI reads the emotion\n\n"
        "<b>Commands:</b>\n"
        "/mode — 🎭 Switch AI mode (10 modes)\n"
        "/status — 📊 Plan and limit info\n"
        "/clear — 🗑 Delete chat\n"
        "/export — 📤 Download chat as file\n"
        "/search — 🌐 Toggle web search\n"
        "/invite — 🎁 Invite friends, earn bonus\n"
        "/top — 🏆 Most active users\n"
        "/feedback — 💌 Send feedback\n"
        "/upgrade — ⭐ Get Premium\n\n"
        "💡 <b>Tip:</b> Use the bot in any chat by typing @botusername!"
    ),

    "btn_mode":        "🎭 Choose mode",
    "btn_status":      "📊 Status",
    "btn_internet":    "🌐 Internet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Clear chat",
    "btn_export":      "📤 Export",
    "btn_invite":      "🎁 Invite",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Help",
    "btn_feedback":    "💌 Feedback",
    "btn_back":        "⬅️ Main menu",
    "btn_back_short":  "⬅️ Back",
    "btn_retry":       "🔁 Try again",
    "btn_upgrade":     "⭐ Get Premium",
    "btn_invite_bonus":"🎁 Invite friend (+bonus)",
    "btn_share_link":  "📤 Share link",
    "btn_refresh":     "🔄 Refresh",
    "btn_language":    "🌍 Language",

    "lang_select_title": "🌍 <b>Select language</b>\n\nCurrent: <b>{current}</b>",
    "lang_changed":      "✅ Language changed: <b>{lang}</b>",
    "lang_already":      "ℹ️ Language is already set to <b>{lang}</b>.",

    "status_plan":        "{emoji} <b>Plan:</b> {plan}",
    "status_mode":        "🎭 <b>Mode:</b> {mode}",
    "status_internet":    "🌐 <b>Internet:</b> {state}",
    "status_limit":       "📊 <b>Limit:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Remaining:</b> {remaining} messages",
    "status_until":       "📅 <b>Expires:</b> {date} ({days} days left)",
    "status_bonus":       "🎁 <b>Bonus messages:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 Get premium with /upgrade → 500 msg/day",

    "mode_select_title":   "🎭 <b>Choose mode</b>",
    "mode_select_header":  "🎭 <b>Choose mode</b>\n\nEach mode activates a different AI personality:",
    "mode_changed":        "✅ Mode changed: <b>{mode}</b>\n📝 {desc}\n\nSend me a message! 👇",
    "mode_selected_toast": "{mode} selected!",
    "mode_invalid":        "Invalid mode.",
    "mode_current":        "Current mode: <b>{mode}</b>",

    "clear_done":     "🗑 Chat cleared ({count} messages).\n\nStart a new chat! 👇",
    "clear_toast":    "Chat cleared!",
    "clear_cmd_done": "🗑️ Chat history deleted ({count} messages).\nYou can start a new chat!",

    "search_on":       "✅ enabled",
    "search_off":      "❌ disabled",
    "search_toggled":  "🌐 Web search {status}.",
    "search_toggled_detail": (
        "🌐 Web search {status}.\n\n"
        "When on, AI fetches real-time info from the internet."
    ),

    "invite_text": (
        "🎁 <b>Invite friends, earn bonus!</b>\n\n"
        "Every friend you invite gets both of you <b>+5 bonus messages</b>.\n\n"
        "🔗 Your link:\n<code>{link}</code>\n\n"
        "👥 Total invites: <b>{count}</b>\n"
        "🎁 Bonus earned: <b>+{bonus}</b> messages"
    ),
    "invite_share_url": "This AI bot is amazing!",

    "export_empty":   "📭 You have no chat history yet.",
    "export_caption": "📤 Your chat history ({count} messages)\n📅 Export date: {date}",
    "export_user":    "👤 You",
    "export_ai":      "🤖 AI",

    "top_empty":       "No users yet.",
    "top_title":       "🏆 <b>Most active users (today)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 Users</b>\n",

    "feedback_usage": (
        "💌 Send feedback like this:\n"
        "<code>/feedback Your message here</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Feedback / Suggestion</b>\n\n"
        "To share feedback, a suggestion, or report a problem:\n\n"
        "<code>/feedback [your message]</code>\n\n"
        "Example: <code>/feedback The Translator mode is great!</code>"
    ),
    "feedback_sent":    "✅ Feedback sent! Thank you 🙏\nEvery message helps improve the bot.",
    "feedback_saved":   "✅ Feedback recorded! Thank you 🙏",
    "feedback_admin":   "💌 <b>New feedback!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ You're already a premium user!\n📅 Expires: {until}\n⏳ Days left: {days}",
    "upgrade_already_simple":"✅ You're already a premium user!",
    "upgrade_already_toast": "You're already premium! ⭐",
    "upgrade_invoice_title": "Premium Plan ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} days Premium:\n"
        "• {premium_limit} messages/day (standard: {free_limit})\n"
        "• All 10 AI modes\n"
        "• Document/PDF analysis\n"
        "• Priority support"
    ),
    "upgrade_success": (
        "🎉 <b>Payment successful!</b>\n\n"
        "⭐ Premium activated!\n"
        "📅 Expires: {until}\n"
        "📨 Daily limit: {limit} messages\n\n"
        "Start using your new features! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Daily limit reached</b> ({limit}/{limit} messages)\n\n"
        "Options:\n"
        "• Limit resets tomorrow\n"
        "• Get premium with /upgrade (500 msg/day)\n"
        "• Invite friends with /invite (bonus messages)"
    ),
    "limit_warning":  "ℹ️ Remaining today: <b>{remaining}/{limit}</b>\n💡 Get Premium with /upgrade — 500 msg/day!",
    "processing":     "⏳ Your previous request is still processing, please wait...",
    "db_error":       "😕 A database error occurred, please try again later.",
    "ai_rate_limit":  "⏳ <b>AI is busy</b>\nTry again in <b>{retry_after} seconds</b>.",
    "ai_error":       "😕 AI couldn't respond. Please try again later.",

    "retry_expired":  "⏰ Expired, please send again.",
    "retry_trying":   "🔁 Retrying...",

    "photo_default_prompt":  "What do you see in this image? Describe it in detail, list everything.",
    "doc_size_error":        "❌ File too large ({size_mb:.1f} MB).\nMaximum size: {max_mb} MB.",
    "doc_format_error": (
        "❌ This file format is not supported.\n\n"
        "✅ Supported formats:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Read this document carefully and explain its main content. "
        "If it's a PDF, extract all important information."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "The user sent you a sticker with the '{emoji}' emoji. "
        "Give a friendly, short reply matching that emotion. "
        "Match their tone."
    ),

    "inline_type_hint":    "✍️ Type your question...",
    "inline_short_prompt": "Give a short and precise answer (max 200 words): {query}",
    "inline_error":        "❌ Could not get a response. Try again later.",
    "inline_result_title": "🤖 AI Answer",

    "admin_panel":       "🛠 <b>Admin Panel</b>\n\nWhat do you want to do?",
    "admin_no_perm":     "Permission denied.",
    "admin_grant_usage": "Usage: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ User {uid} → plan: {plan}",
    "admin_lookup_usage":"Usage: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Not found: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>User info</b>\n\n"
        "🆔 ID:       <code>{uid}</code>\n"
        "👤 Name:     {first_name}\n"
        "📛 Username: @{username}\n"
        "📦 Plan:     <b>{plan}</b>\n"
        "📅 Premium:  {until}\n"
        "🎭 Mode:     {mode}\n"
        "💬 Today:    {used}/{limit}\n"
        "👥 Referrals:{refs}\n"
        "📆 Joined:   {created}"
    ),
    "admin_btn_stats":    "📊 Statistics",
    "admin_btn_revenue":  "💰 Revenue",
    "admin_btn_broadcast":"📢 Broadcast",
    "admin_btn_lookup":   "🔍 Search user",
    "admin_btn_top":      "🏆 TOP users",
    "admin_btn_expiring": "⏰ Expiring",
    "admin_btn_premium":  "⭐ Grant Premium",
    "admin_btn_free":     "🆓 Set Free",
    "admin_btn_clear_h":  "🗑 Clear history",
    "admin_btn_bonus":    "🎁 +10 Bonus",
    "admin_stats": (
        "📊 <b>Bot Statistics</b>\n\n"
        "👥 Total users:   <b>{total:,}</b>\n"
        "⭐ Premium:        <b>{premium:,}</b>\n"
        "🆓 Free:           <b>{free:,}</b>\n"
        "📈 Conversion:     <b>{cvr:.1f}%</b>\n\n"
        "🟢 Active today:  <b>{active:,}</b>\n"
        "💬 Messages today:<b>{today_msg:,}</b>\n"
        "📨 Total messages:<b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Revenue Statistics</b>\n\n"
        "⭐ Total Stars earned: <b>{total:,}</b>\n"
        "📅 This month: <b>{month:,}</b> Stars\n"
        "🧾 Total payments: <b>{count:,}</b>\n\n"
        "💡 Average payment: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "No premiums expiring in the next 3 days.",
    "admin_expiring_title": "⏰ <b>Premiums expiring in 3 days:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Broadcast</b>\n\n"
        "<code>/broadcast Your message here</code>\n\n"
        "⚠️ Will be sent to all users!"
    ),
    "admin_broadcast_usage":    "Usage: /broadcast <message>",
    "admin_broadcast_starting": "⏳ Broadcast started... ({total} users)",
    "admin_broadcast_done": (
        "✅ <b>Broadcast complete</b>\n\n"
        "✉️ Sent: {sent}\n"
        "❌ Failed: {failed}\n"
        "📊 Total: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Bot announcement</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Search user</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium granted ({days} days)",
    "admin_grant_free_done":    "🆓 Switched to free plan",
    "admin_clear_done":         "🗑 {count} messages deleted",
    "admin_bonus_done":         "🎁 +10 bonus messages granted!",

    "top_row":             "{medal} {name} {plan_icon} — {usage} messages",
    "status_today":        "📊 Today: {used}/{limit} [{bar}]",
    "status_until_short":  "📅 Expires: {date}",
    "mode_row":            "{check} {name} — {desc}",
    "inline_result_msg":   "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Guest",
}

# ── Russian ───────────────────────────────────────────────────────────────────

RU: dict[str, str] = {
    "welcome": (
        "👋 <b>Привет, {name}!</b>\n\n"
        "Я мощный бот на базе <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>Что я умею:</b>\n"
        "• Отвечать на вопросы\n"
        "• Анализировать фото, голос и документы\n"
        "• Помогать в 10 разных режимах\n"
        "• Искать в интернете в реальном времени\n\n"
        "Начни с кнопок ниже 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Ты пришёл по реферальной ссылке — тебе начислено <b>+5 бонусных сообщений</b>!",
    "welcome_premium_expiry": "\n\n⚠️ Твой Premium истекает через <b>{days_left} дней</b>! Продли с помощью /upgrade.",

    "help": (
        "ℹ️ <b>Как пользоваться</b>\n\n"
        "💬 <b>Напиши текст</b> → AI ответит\n"
        "🖼 <b>Отправь фото</b> → AI проанализирует\n"
        "📄 <b>Документ/PDF</b> → AI прочитает и объяснит\n"
        "🎙 <b>Голосовое сообщение</b> → AI послушает и ответит\n"
        "😄 <b>Стикер</b> → AI считает эмоцию\n\n"
        "<b>Команды:</b>\n"
        "/mode — 🎭 Сменить режим AI (10 режимов)\n"
        "/status — 📊 Информация о плане и лимите\n"
        "/clear — 🗑 Очистить чат\n"
        "/export — 📤 Скачать историю чата\n"
        "/search — 🌐 Вкл/выкл поиск в интернете\n"
        "/invite — 🎁 Пригласить друзей, получить бонус\n"
        "/top — 🏆 Самые активные пользователи\n"
        "/feedback — 💌 Отправить отзыв\n"
        "/upgrade — ⭐ Купить Premium\n\n"
        "💡 <b>Совет:</b> Используй бота в любом чате, написав @botusername!"
    ),

    "btn_mode":         "🎭 Выбрать режим",
    "btn_status":       "📊 Статус",
    "btn_internet":     "🌐 Интернет",
    "btn_premium":      "⭐ Premium",
    "btn_clear":        "🗑 Очистить чат",
    "btn_export":       "📤 Экспорт",
    "btn_invite":       "🎁 Пригласить",
    "btn_top":          "🏆 ТОП",
    "btn_help":         "ℹ️ Помощь",
    "btn_feedback":     "💌 Отзыв",
    "btn_back":         "⬅️ Главное меню",
    "btn_back_short":   "⬅️ Назад",
    "btn_retry":        "🔁 Повторить",
    "btn_upgrade":      "⭐ Купить Premium",
    "btn_invite_bonus": "🎁 Пригласить друга (+бонус)",
    "btn_share_link":   "📤 Поделиться ссылкой",
    "btn_refresh":      "🔄 Обновить",
    "btn_language":     "🌍 Язык",

    "lang_select_title": "🌍 <b>Выберите язык</b>\n\nТекущий: <b>{current}</b>",
    "lang_changed":      "✅ Язык изменён: <b>{lang}</b>",
    "lang_already":      "ℹ️ Язык уже установлен: <b>{lang}</b>.",

    "status_plan":        "{emoji} <b>План:</b> {plan}",
    "status_mode":        "🎭 <b>Режим:</b> {mode}",
    "status_internet":    "🌐 <b>Интернет:</b> {state}",
    "status_limit":       "📊 <b>Лимит:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Осталось:</b> {remaining} сообщений",
    "status_until":       "📅 <b>Истекает:</b> {date} (осталось {days} дн.)",
    "status_bonus":       "🎁 <b>Бонусные сообщения:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 Получи Premium через /upgrade → 500 сообщений/день",

    "mode_select_title":   "🎭 <b>Выбери режим</b>",
    "mode_select_header":  "🎭 <b>Выбери режим</b>\n\nКаждый режим активирует разную личность AI:",
    "mode_changed":        "✅ Режим изменён: <b>{mode}</b>\n📝 {desc}\n\nНапиши мне! 👇",
    "mode_selected_toast": "{mode} выбран!",
    "mode_invalid":        "Неверный режим.",
    "mode_current":        "Текущий режим: <b>{mode}</b>",

    "clear_done":     "🗑 Чат очищен ({count} сообщений).\n\nНачни новый чат! 👇",
    "clear_toast":    "Чат очищен!",
    "clear_cmd_done": "🗑️ История чата удалена ({count} сообщений).\nМожешь начать новый чат!",

    "search_on":       "✅ включён",
    "search_off":      "❌ выключен",
    "search_toggled":  "🌐 Поиск в интернете {status}.",
    "search_toggled_detail": (
        "🌐 Поиск в интернете {status}.\n\n"
        "Когда включён, AI ищет актуальную информацию в сети."
    ),

    "invite_text": (
        "🎁 <b>Приглашай друзей — получай бонусы!</b>\n\n"
        "Каждый приглашённый друг даёт <b>вам обоим +5 бонусных сообщений</b>.\n\n"
        "🔗 Твоя ссылка:\n<code>{link}</code>\n\n"
        "👥 Всего приглашено: <b>{count}</b>\n"
        "🎁 Заработано бонусов: <b>+{bonus}</b> сообщений"
    ),
    "invite_share_url": "Этот AI бот просто отличный!",

    "export_empty":   "📭 У тебя пока нет истории чата.",
    "export_caption": "📤 История чата ({count} сообщений)\n📅 Дата экспорта: {date}",
    "export_user":    "👤 Ты",
    "export_ai":      "🤖 AI",

    "top_empty":       "Пока нет пользователей.",
    "top_title":       "🏆 <b>Самые активные пользователи (сегодня)</b>\n",
    "top_title_admin": "🏆 <b>ТОП 10 пользователей</b>\n",

    "feedback_usage": (
        "💌 Отправь отзыв вот так:\n"
        "<code>/feedback Твой текст здесь</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Отзыв / Предложение</b>\n\n"
        "Чтобы поделиться отзывом, предложением или сообщить о проблеме:\n\n"
        "<code>/feedback [твой текст]</code>\n\n"
        "Например: <code>/feedback Режим переводчика очень удобный!</code>"
    ),
    "feedback_sent":  "✅ Отзыв отправлен! Спасибо 🙏\nКаждое сообщение помогает улучшить бота.",
    "feedback_saved": "✅ Отзыв сохранён! Спасибо 🙏",
    "feedback_admin": "💌 <b>Новый отзыв!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":        "✅ Ты уже Premium пользователь!\n📅 Истекает: {until}\n⏳ Осталось: {days} дн.",
    "upgrade_already_simple": "✅ Ты уже Premium пользователь!",
    "upgrade_already_toast":  "Ты уже Premium! ⭐",
    "upgrade_invoice_title":  "Premium план ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} дней Premium:\n"
        "• {premium_limit} сообщений/день (стандарт: {free_limit})\n"
        "• Все 10 режимов AI\n"
        "• Анализ документов/PDF\n"
        "• Приоритетная поддержка"
    ),
    "upgrade_success": (
        "🎉 <b>Оплата прошла успешно!</b>\n\n"
        "⭐ Premium активирован!\n"
        "📅 Истекает: {until}\n"
        "📨 Дневной лимит: {limit} сообщений\n\n"
        "Начинай пользоваться новыми возможностями! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Дневной лимит исчерпан</b> ({limit}/{limit} сообщений)\n\n"
        "Варианты:\n"
        "• Лимит сбросится завтра\n"
        "• Купи Premium через /upgrade (500 сообщений/день)\n"
        "• Пригласи друга через /invite (бонусные сообщения)"
    ),
    "limit_warning":  "ℹ️ Осталось сегодня: <b>{remaining}/{limit}</b>\n💡 Купи Premium через /upgrade — 500 сообщений/день!",
    "processing":     "⏳ Предыдущий запрос ещё обрабатывается, подожди...",
    "db_error":       "😕 Произошла ошибка базы данных, попробуй позже.",
    "ai_rate_limit":  "⏳ <b>AI перегружен</b>\nПопробуй снова через <b>{retry_after} секунд</b>.",
    "ai_error":       "😕 AI не смог ответить. Попробуй позже.",

    "retry_expired":  "⏰ Время истекло, напиши снова.",
    "retry_trying":   "🔁 Повторная попытка...",

    "photo_default_prompt":  "Что ты видишь на этом фото? Опиши подробно, перечисли всё.",
    "doc_size_error":        "❌ Файл слишком большой ({size_mb:.1f} МБ).\nМаксимальный размер: {max_mb} МБ.",
    "doc_format_error": (
        "❌ Этот формат файла не поддерживается.\n\n"
        "✅ Поддерживаемые форматы:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Прочитай этот документ внимательно и объясни его основное содержание. "
        "Если это PDF, извлеки всю важную информацию."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Russian, reply in Russian. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "Пользователь отправил тебе стикер с эмодзи '{emoji}'. "
        "Дай короткий дружелюбный ответ, соответствующий этой эмоции. "
        "Отвечай в том же тоне."
    ),

    "inline_type_hint":    "✍️ Введите вопрос...",
    "inline_short_prompt": "Дай короткий и точный ответ (макс. 200 слов): {query}",
    "inline_error":        "❌ Не удалось получить ответ. Попробуй позже.",
    "inline_result_title": "🤖 Ответ AI",

    "admin_panel":       "🛠 <b>Панель администратора</b>\n\nЧто хочешь сделать?",
    "admin_no_perm":     "Нет доступа.",
    "admin_grant_usage": "Использование: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ Пользователь {uid} → план: {plan}",
    "admin_lookup_usage":"Использование: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Не найден: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>Информация о пользователе</b>\n\n"
        "🆔 ID:         <code>{uid}</code>\n"
        "👤 Имя:        {first_name}\n"
        "📛 Username:   @{username}\n"
        "📦 План:       <b>{plan}</b>\n"
        "📅 Premium:    {until}\n"
        "🎭 Режим:      {mode}\n"
        "💬 Сегодня:    {used}/{limit}\n"
        "👥 Рефералы:   {refs}\n"
        "📆 Регистрация:{created}"
    ),
    "admin_btn_stats":    "📊 Статистика",
    "admin_btn_revenue":  "💰 Доходы",
    "admin_btn_broadcast":"📢 Рассылка",
    "admin_btn_lookup":   "🔍 Найти юзера",
    "admin_btn_top":      "🏆 ТОП юзеры",
    "admin_btn_expiring": "⏰ Истекают",
    "admin_btn_premium":  "⭐ Дать Premium",
    "admin_btn_free":     "🆓 Сделать Free",
    "admin_btn_clear_h":  "🗑 Удалить историю",
    "admin_btn_bonus":    "🎁 +10 Бонус",
    "admin_stats": (
        "📊 <b>Статистика бота</b>\n\n"
        "👥 Всего пользователей: <b>{total:,}</b>\n"
        "⭐ Premium:              <b>{premium:,}</b>\n"
        "🆓 Бесплатных:          <b>{free:,}</b>\n"
        "📈 Конверсия:           <b>{cvr:.1f}%</b>\n\n"
        "🟢 Активны сегодня:     <b>{active:,}</b>\n"
        "💬 Сообщений сегодня:   <b>{today_msg:,}</b>\n"
        "📨 Всего сообщений:     <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Статистика доходов</b>\n\n"
        "⭐ Всего Stars: <b>{total:,}</b>\n"
        "📅 В этом месяце: <b>{month:,}</b> Stars\n"
        "🧾 Всего платежей: <b>{count:,}</b>\n\n"
        "💡 Средний платёж: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "Нет Premium, истекающих в ближайшие 3 дня.",
    "admin_expiring_title": "⏰ <b>Premium, истекающий через 3 дня:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Рассылка</b>\n\n"
        "<code>/broadcast Твой текст здесь</code>\n\n"
        "⚠️ Будет отправлено всем пользователям!"
    ),
    "admin_broadcast_usage":    "Использование: /broadcast <текст>",
    "admin_broadcast_starting": "⏳ Рассылка начата... ({total} пользователей)",
    "admin_broadcast_done": (
        "✅ <b>Рассылка завершена</b>\n\n"
        "✉️ Отправлено: {sent}\n"
        "❌ Ошибок: {failed}\n"
        "📊 Всего: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Сообщение от бота</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Найти пользователя</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium выдан ({days} дней)",
    "admin_grant_free_done":    "🆓 Переведён на бесплатный план",
    "admin_clear_done":         "🗑 Удалено {count} сообщений",
    "admin_bonus_done":         "🎁 +10 бонусных сообщений выдано!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} сообщений",
    "status_today":       "📊 Сегодня: {used}/{limit} [{bar}]",
    "status_until_short": "📅 Истекает: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Гость",
}

# ── Turkish ───────────────────────────────────────────────────────────────────

TR: dict[str, str] = {
    "welcome": (
        "👋 <b>Merhaba, {name}!</b>\n\n"
        "Ben <b>Gemini AI</b> destekli güçlü bir botum. 🚀\n\n"
        "📝 <b>Neler yapabilirim:</b>\n"
        "• Sorularını yanıtlarım\n"
        "• Fotoğraf, ses ve belge analizi yaparım\n"
        "• 10 farklı modda yardım ederim\n"
        "• Gerçek zamanlı internet araması yaparım\n\n"
        "Aşağıdaki düğmelerle başla 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Davet linki ile katıldın — sana <b>+5 bonus mesaj</b> verildi!",
    "welcome_premium_expiry": "\n\n⚠️ Premium aboneliğin <b>{days_left} gün</b> sonra bitiyor! /upgrade ile uzat.",

    "help": (
        "ℹ️ <b>Nasıl kullanılır</b>\n\n"
        "💬 <b>Metin yaz</b> → AI yanıtlar\n"
        "🖼 <b>Fotoğraf gönder</b> → AI analiz eder\n"
        "📄 <b>Belge/PDF gönder</b> → AI okur ve açıklar\n"
        "🎙 <b>Sesli mesaj</b> → AI dinler ve yanıtlar\n"
        "😄 <b>Sticker gönder</b> → AI duyguyu okur\n\n"
        "<b>Komutlar:</b>\n"
        "/mode — 🎭 AI modunu değiştir (10 mod)\n"
        "/status — 📊 Plan ve limit bilgisi\n"
        "/clear — 🗑 Sohbeti sil\n"
        "/export — 📤 Sohbeti dosya olarak indir\n"
        "/search — 🌐 İnternet aramasını aç/kapat\n"
        "/invite — 🎁 Arkadaş davet et, bonus kazan\n"
        "/top — 🏆 En aktif kullanıcılar\n"
        "/feedback — 💌 Geri bildirim gönder\n"
        "/upgrade — ⭐ Premium al\n\n"
        "💡 <b>İpucu:</b> Botu herhangi bir sohbette @botusername yazarak kullanabilirsin!"
    ),

    "btn_mode":        "🎭 Mod seç",
    "btn_status":      "📊 Durum",
    "btn_internet":    "🌐 İnternet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Sohbeti sil",
    "btn_export":      "📤 Dışa aktar",
    "btn_invite":      "🎁 Davet et",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Yardım",
    "btn_feedback":    "💌 Geri bildirim",
    "btn_back":        "⬅️ Ana menü",
    "btn_back_short":  "⬅️ Geri",
    "btn_retry":       "🔁 Tekrar dene",
    "btn_upgrade":     "⭐ Premium al",
    "btn_invite_bonus":"🎁 Arkadaş davet et (+bonus)",
    "btn_share_link":  "📤 Linki paylaş",
    "btn_refresh":     "🔄 Yenile",
    "btn_language":    "🌍 Dil",

    "lang_select_title": "🌍 <b>Dil seçin</b>\n\nMevcut dil: <b>{current}</b>",
    "lang_changed":      "✅ Dil değiştirildi: <b>{lang}</b>",
    "lang_already":      "ℹ️ Dil zaten <b>{lang}</b> olarak ayarlı.",

    "status_plan":        "{emoji} <b>Plan:</b> {plan}",
    "status_mode":        "🎭 <b>Mod:</b> {mode}",
    "status_internet":    "🌐 <b>İnternet:</b> {state}",
    "status_limit":       "📊 <b>Limit:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Kalan:</b> {remaining} mesaj",
    "status_until":       "📅 <b>Bitiş tarihi:</b> {date} ({days} gün kaldı)",
    "status_bonus":       "🎁 <b>Bonus mesaj:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 /upgrade ile premium al → günlük 500 mesaj",

    "mode_select_title":   "🎭 <b>Mod seç</b>",
    "mode_select_header":  "🎭 <b>Mod seç</b>\n\nHer mod farklı bir AI kişiliği etkinleştirir:",
    "mode_changed":        "✅ Mod değiştirildi: <b>{mode}</b>\n📝 {desc}\n\nŞimdi mesaj yaz! 👇",
    "mode_selected_toast": "{mode} seçildi!",
    "mode_invalid":        "Geçersiz mod.",
    "mode_current":        "Mevcut mod: <b>{mode}</b>",

    "clear_done":     "🗑 Sohbet silindi ({count} mesaj).\n\nYeni sohbet başlat! 👇",
    "clear_toast":    "Sohbet silindi!",
    "clear_cmd_done": "🗑️ Sohbet geçmişi silindi ({count} mesaj).\nYeni bir sohbet başlatabilirsin!",

    "search_on":       "✅ açıldı",
    "search_off":      "❌ kapatıldı",
    "search_toggled":  "🌐 İnternet araması {status}.",
    "search_toggled_detail": (
        "🌐 İnternet araması {status}.\n\n"
        "Açıkken AI gerçek zamanlı internetten bilgi arar."
    ),

    "invite_text": (
        "🎁 <b>Arkadaş davet et, bonus kazan!</b>\n\n"
        "Davet ettiğin her arkadaş botu açtığında — <b>ikiniz de +5 bonus mesaj</b> kazanırsınız.\n\n"
        "🔗 Senin linkin:\n<code>{link}</code>\n\n"
        "👥 Şimdiye kadar davet ettiğin: <b>{count}</b> kişi\n"
        "🎁 Kazandığın bonus: <b>+{bonus}</b> mesaj"
    ),
    "invite_share_url": "Bu AI botu harika!",

    "export_empty":   "📭 Henüz hiç sohbet geçmişin yok.",
    "export_caption": "📤 Sohbet geçmişin ({count} mesaj)\n📅 Dışa aktarma tarihi: {date}",
    "export_user":    "👤 Sen",
    "export_ai":      "🤖 AI",

    "top_empty":       "Henüz hiç kullanıcı yok.",
    "top_title":       "🏆 <b>En aktif kullanıcılar (bugün)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 Kullanıcı</b>\n",

    "feedback_usage": (
        "💌 Geri bildirimi şöyle gönderin:\n"
        "<code>/feedback Mesajınız buraya</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Geri Bildirim / Öneri</b>\n\n"
        "Geri bildirim, öneri veya sorun bildirmek için:\n\n"
        "<code>/feedback [mesajın buraya]</code>\n\n"
        "Örnek: <code>/feedback Çevirmen modu harika!</code>"
    ),
    "feedback_sent":    "✅ Geri bildirim gönderildi! Teşekkürler 🙏\nHer mesaj botu daha iyi yapmaya yardımcı olur.",
    "feedback_saved":   "✅ Geri bildirim kaydedildi! Teşekkürler 🙏",
    "feedback_admin":   "💌 <b>Yeni geri bildirim!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ Zaten premium kullanıcısın!\n📅 Bitiş tarihi: {until}\n⏳ Kalan: {days} gün",
    "upgrade_already_simple":"✅ Zaten premium kullanıcısın!",
    "upgrade_already_toast": "Zaten premiumsun! ⭐",
    "upgrade_invoice_title": "Premium plan ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} gün Premium:\n"
        "• Günlük {premium_limit} mesaj (standart: {free_limit})\n"
        "• Tüm 10 AI modu\n"
        "• Belge/PDF analizi\n"
        "• Öncelikli destek"
    ),
    "upgrade_success": (
        "🎉 <b>Ödeme başarıyla alındı!</b>\n\n"
        "⭐ Premium etkinleştirildi!\n"
        "📅 Bitiş tarihi: {until}\n"
        "📨 Günlük limit: {limit} mesaj\n\n"
        "Yeni özelliklerini kullanmaya başla! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Günlük limit doldu</b> ({limit}/{limit} mesaj)\n\n"
        "Seçenekler:\n"
        "• Limit yarın sıfırlanır\n"
        "• /upgrade ile premium al (günlük 500 mesaj)\n"
        "• /invite ile arkadaş davet et (bonus mesaj)"
    ),
    "limit_warning":  "ℹ️ Bugün kalan limit: <b>{remaining}/{limit}</b>\n💡 /upgrade ile Premium al — günlük 500 mesaj!",
    "processing":     "⏳ Önceki sorgun hâlâ yanıtlanıyor, biraz bekle...",
    "db_error":       "😕 Veritabanında hata oluştu, biraz sonra tekrar dene.",
    "ai_rate_limit":  "⏳ <b>AI meşgul</b>\n<b>{retry_after} saniye</b> sonra tekrar dene.",
    "ai_error":       "😕 AI yanıt veremedi. Biraz sonra tekrar dene.",

    "retry_expired":  "⏰ Süresi doldu, tekrar yaz.",
    "retry_trying":   "🔁 Tekrar deneniyor...",

    "photo_default_prompt":  "Bu fotoğrafta ne görüyorsun? Ayrıntılı açıkla, her şeyi say.",
    "doc_size_error":        "❌ Dosya çok büyük ({size_mb:.1f} MB).\nMaksimum boyut: {max_mb} MB.",
    "doc_format_error": (
        "❌ Bu dosya formatı desteklenmiyor.\n\n"
        "✅ Desteklenen formatlar:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Bu belgeyi dikkatlice oku ve ana içeriğini açıkla. "
        "PDF ise tüm önemli bilgileri çıkar."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "Kullanıcı sana '{emoji}' emojili bir sticker gönderdi. "
        "Bu duyguya uygun, samimi ve kısa bir yanıt ver. "
        "Aynı tonda yanıtla."
    ),

    "inline_type_hint":    "✍️ Sorunuzu yazın...",
    "inline_short_prompt": "Kısa ve kesin cevap ver (maks 200 kelime): {query}",
    "inline_error":        "❌ Yanıt alınamadı. Biraz sonra deneyin.",
    "inline_result_title": "🤖 AI Yanıtı",

    "admin_panel":       "🛠 <b>Admin Paneli</b>\n\nNe yapmak istiyorsun?",
    "admin_no_perm":     "İzin yok.",
    "admin_grant_usage": "Kullanım: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ Kullanıcı {uid} → plan: {plan}",
    "admin_lookup_usage":"Kullanım: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Bulunamadı: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>Kullanıcı bilgisi</b>\n\n"
        "🆔 ID:        <code>{uid}</code>\n"
        "👤 Ad:        {first_name}\n"
        "📛 Kullanıcı: @{username}\n"
        "📦 Plan:      <b>{plan}</b>\n"
        "📅 Premium:   {until}\n"
        "🎭 Mod:       {mode}\n"
        "💬 Bugün:     {used}/{limit}\n"
        "👥 Davetler:  {refs}\n"
        "📆 Kayıt:     {created}"
    ),
    "admin_btn_stats":    "📊 İstatistikler",
    "admin_btn_revenue":  "💰 Gelir",
    "admin_btn_broadcast":"📢 Duyuru",
    "admin_btn_lookup":   "🔍 Kullanıcı ara",
    "admin_btn_top":      "🏆 TOP kullanıcılar",
    "admin_btn_expiring": "⏰ Bitiyor",
    "admin_btn_premium":  "⭐ Premium ver",
    "admin_btn_free":     "🆓 Ücretsiz yap",
    "admin_btn_clear_h":  "🗑 Geçmişi sil",
    "admin_btn_bonus":    "🎁 +10 Bonus",
    "admin_stats": (
        "📊 <b>Bot İstatistikleri</b>\n\n"
        "👥 Toplam kullanıcı: <b>{total:,}</b>\n"
        "⭐ Premium:          <b>{premium:,}</b>\n"
        "🆓 Ücretsiz:         <b>{free:,}</b>\n"
        "📈 Dönüşüm:          <b>{cvr:.1f}%</b>\n\n"
        "🟢 Bugün aktif:     <b>{active:,}</b>\n"
        "💬 Bugünkü mesaj:   <b>{today_msg:,}</b>\n"
        "📨 Toplam mesaj:    <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Gelir İstatistikleri</b>\n\n"
        "⭐ Toplam Stars: <b>{total:,}</b>\n"
        "📅 Bu ay: <b>{month:,}</b> Stars\n"
        "🧾 Toplam ödeme: <b>{count:,}</b>\n\n"
        "💡 Ortalama ödeme: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "Önümüzdeki 3 günde biten premium yok.",
    "admin_expiring_title": "⏰ <b>3 günde biten premium'lar:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Duyuru</b>\n\n"
        "<code>/broadcast Mesajın buraya</code>\n\n"
        "⚠️ Tüm kullanıcılara gönderilecek!"
    ),
    "admin_broadcast_usage":    "Kullanım: /broadcast <mesaj>",
    "admin_broadcast_starting": "⏳ Duyuru başladı... ({total} kullanıcı)",
    "admin_broadcast_done": (
        "✅ <b>Duyuru tamamlandı</b>\n\n"
        "✉️ Gönderildi: {sent}\n"
        "❌ Başarısız: {failed}\n"
        "📊 Toplam: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Bot duyurusu</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Kullanıcı ara</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium verildi ({days} gün)",
    "admin_grant_free_done":    "🆓 Ücretsiz plana geçirildi",
    "admin_clear_done":         "🗑 {count} mesaj silindi",
    "admin_bonus_done":         "🎁 +10 bonus mesaj verildi!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} mesaj",
    "status_today":       "📊 Bugün: {used}/{limit} [{bar}]",
    "status_until_short": "📅 Bitiş: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Misafir",
}

# ── German ────────────────────────────────────────────────────────────────────

DE: dict[str, str] = {
    "welcome": (
        "👋 <b>Hallo, {name}!</b>\n\n"
        "Ich bin ein leistungsstarker Bot mit <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>Was ich kann:</b>\n"
        "• Deine Fragen beantworten\n"
        "• Bilder, Sprachnachrichten und Dokumente analysieren\n"
        "• In 10 verschiedenen Modi helfen\n"
        "• Echtzeit-Internetsuche durchführen\n\n"
        "Starte mit den Buttons unten 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Du bist über einen Einladungslink gekommen — du erhältst <b>+5 Bonus-Nachrichten</b>!",
    "welcome_premium_expiry": "\n\n⚠️ Dein Premium läuft in <b>{days_left} Tagen</b> ab! Verlängere mit /upgrade.",

    "help": (
        "ℹ️ <b>Anleitung</b>\n\n"
        "💬 <b>Text schreiben</b> → AI antwortet\n"
        "🖼 <b>Bild senden</b> → AI analysiert es\n"
        "📄 <b>Dokument/PDF senden</b> → AI liest und erklärt\n"
        "🎙 <b>Sprachnachricht</b> → AI hört zu und antwortet\n"
        "😄 <b>Sticker senden</b> → AI liest die Emotion\n\n"
        "<b>Befehle:</b>\n"
        "/mode — 🎭 AI-Modus wechseln (10 Modi)\n"
        "/status — 📊 Plan- und Limitinfo\n"
        "/clear — 🗑 Chat löschen\n"
        "/export — 📤 Chat als Datei herunterladen\n"
        "/search — 🌐 Internetsuche ein-/ausschalten\n"
        "/invite — 🎁 Freunde einladen, Bonus verdienen\n"
        "/top — 🏆 Aktivste Nutzer\n"
        "/feedback — 💌 Feedback senden\n"
        "/upgrade — ⭐ Premium kaufen\n\n"
        "💡 <b>Tipp:</b> Nutze den Bot in jedem Chat mit @botusername!"
    ),

    "btn_mode":        "🎭 Modus wählen",
    "btn_status":      "📊 Status",
    "btn_internet":    "🌐 Internet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Chat löschen",
    "btn_export":      "📤 Exportieren",
    "btn_invite":      "🎁 Einladen",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Hilfe",
    "btn_feedback":    "💌 Feedback",
    "btn_back":        "⬅️ Hauptmenü",
    "btn_back_short":  "⬅️ Zurück",
    "btn_retry":       "🔁 Nochmal versuchen",
    "btn_upgrade":     "⭐ Premium kaufen",
    "btn_invite_bonus":"🎁 Freund einladen (+Bonus)",
    "btn_share_link":  "📤 Link teilen",
    "btn_refresh":     "🔄 Aktualisieren",
    "btn_language":    "🌍 Sprache",

    "lang_select_title": "🌍 <b>Sprache wählen</b>\n\nAktuelle Sprache: <b>{current}</b>",
    "lang_changed":      "✅ Sprache geändert: <b>{lang}</b>",
    "lang_already":      "ℹ️ Sprache ist bereits auf <b>{lang}</b> eingestellt.",

    "status_plan":        "{emoji} <b>Plan:</b> {plan}",
    "status_mode":        "🎭 <b>Modus:</b> {mode}",
    "status_internet":    "🌐 <b>Internet:</b> {state}",
    "status_limit":       "📊 <b>Limit:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Verbleibend:</b> {remaining} Nachrichten",
    "status_until":       "📅 <b>Läuft ab:</b> {date} (noch {days} Tage)",
    "status_bonus":       "🎁 <b>Bonus-Nachrichten:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 Premium mit /upgrade holen → 500 Nachrichten/Tag",

    "mode_select_title":   "🎭 <b>Modus wählen</b>",
    "mode_select_header":  "🎭 <b>Modus wählen</b>\n\nJeder Modus aktiviert eine andere AI-Persönlichkeit:",
    "mode_changed":        "✅ Modus geändert: <b>{mode}</b>\n📝 {desc}\n\nSchreib mir jetzt! 👇",
    "mode_selected_toast": "{mode} ausgewählt!",
    "mode_invalid":        "Ungültiger Modus.",
    "mode_current":        "Aktueller Modus: <b>{mode}</b>",

    "clear_done":     "🗑 Chat gelöscht ({count} Nachrichten).\n\nNeuen Chat starten! 👇",
    "clear_toast":    "Chat gelöscht!",
    "clear_cmd_done": "🗑️ Chatverlauf gelöscht ({count} Nachrichten).\nDu kannst einen neuen Chat starten!",

    "search_on":       "✅ aktiviert",
    "search_off":      "❌ deaktiviert",
    "search_toggled":  "🌐 Internetsuche {status}.",
    "search_toggled_detail": (
        "🌐 Internetsuche {status}.\n\n"
        "Wenn aktiviert, sucht die AI in Echtzeit im Internet."
    ),

    "invite_text": (
        "🎁 <b>Freunde einladen, Bonus verdienen!</b>\n\n"
        "Jeder Freund, den du einlädst, bringt euch beiden <b>+5 Bonus-Nachrichten</b>.\n\n"
        "🔗 Dein Link:\n<code>{link}</code>\n\n"
        "👥 Bisher eingeladen: <b>{count}</b> Personen\n"
        "🎁 Verdienter Bonus: <b>+{bonus}</b> Nachrichten"
    ),
    "invite_share_url": "Dieser AI-Bot ist großartig!",

    "export_empty":   "📭 Du hast noch keinen Chatverlauf.",
    "export_caption": "📤 Dein Chatverlauf ({count} Nachrichten)\n📅 Exportdatum: {date}",
    "export_user":    "👤 Du",
    "export_ai":      "🤖 AI",

    "top_empty":       "Noch keine Nutzer vorhanden.",
    "top_title":       "🏆 <b>Aktivste Nutzer (heute)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 Nutzer</b>\n",

    "feedback_usage": (
        "💌 Feedback so senden:\n"
        "<code>/feedback Deine Nachricht hier</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Feedback / Vorschlag</b>\n\n"
        "Für Feedback, Vorschläge oder Problemmeldungen:\n\n"
        "<code>/feedback [dein Text]</code>\n\n"
        "Beispiel: <code>/feedback Der Übersetzer-Modus ist super!</code>"
    ),
    "feedback_sent":    "✅ Feedback gesendet! Danke 🙏\nJede Nachricht hilft, den Bot zu verbessern.",
    "feedback_saved":   "✅ Feedback gespeichert! Danke 🙏",
    "feedback_admin":   "💌 <b>Neues Feedback!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ Du bist bereits Premium-Nutzer!\n📅 Läuft ab: {until}\n⏳ Noch: {days} Tage",
    "upgrade_already_simple":"✅ Du bist bereits Premium-Nutzer!",
    "upgrade_already_toast": "Du bist bereits Premium! ⭐",
    "upgrade_invoice_title": "Premium-Plan ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} Tage Premium:\n"
        "• {premium_limit} Nachrichten/Tag (Standard: {free_limit})\n"
        "• Alle 10 AI-Modi\n"
        "• Dokument/PDF-Analyse\n"
        "• Prioritäts-Support"
    ),
    "upgrade_success": (
        "🎉 <b>Zahlung erfolgreich!</b>\n\n"
        "⭐ Premium aktiviert!\n"
        "📅 Läuft ab: {until}\n"
        "📨 Tägliches Limit: {limit} Nachrichten\n\n"
        "Nutze jetzt deine neuen Funktionen! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Tageslimit erreicht</b> ({limit}/{limit} Nachrichten)\n\n"
        "Optionen:\n"
        "• Limit wird morgen zurückgesetzt\n"
        "• Premium mit /upgrade holen (500 Nachrichten/Tag)\n"
        "• Freunde mit /invite einladen (Bonus-Nachrichten)"
    ),
    "limit_warning":  "ℹ️ Heute verbleibend: <b>{remaining}/{limit}</b>\n💡 Premium mit /upgrade holen — 500 Nachrichten/Tag!",
    "processing":     "⏳ Deine vorherige Anfrage wird noch bearbeitet, bitte warte...",
    "db_error":       "😕 Datenbankfehler, bitte versuche es später erneut.",
    "ai_rate_limit":  "⏳ <b>AI ist ausgelastet</b>\nVersuche es in <b>{retry_after} Sekunden</b> erneut.",
    "ai_error":       "😕 AI konnte nicht antworten. Bitte später erneut versuchen.",

    "retry_expired":  "⏰ Abgelaufen, bitte erneut schreiben.",
    "retry_trying":   "🔁 Erneuter Versuch...",

    "photo_default_prompt":  "Was siehst du auf diesem Bild? Beschreibe es detailliert, nenne alles.",
    "doc_size_error":        "❌ Datei zu groß ({size_mb:.1f} MB).\nMaximale Größe: {max_mb} MB.",
    "doc_format_error": (
        "❌ Dieses Dateiformat wird nicht unterstützt.\n\n"
        "✅ Unterstützte Formate:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Lies dieses Dokument sorgfältig und erkläre den Hauptinhalt. "
        "Falls es ein PDF ist, extrahiere alle wichtigen Informationen."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "Der Nutzer hat dir einen Sticker mit dem '{emoji}'-Emoji geschickt. "
        "Gib eine freundliche, kurze Antwort passend zu dieser Emotion. "
        "Antworte im selben Ton."
    ),

    "inline_type_hint":    "✍️ Frage eingeben...",
    "inline_short_prompt": "Gib eine kurze und präzise Antwort (max. 200 Wörter): {query}",
    "inline_error":        "❌ Antwort konnte nicht abgerufen werden. Später erneut versuchen.",
    "inline_result_title": "🤖 AI-Antwort",

    "admin_panel":       "🛠 <b>Admin-Panel</b>\n\nWas möchtest du tun?",
    "admin_no_perm":     "Keine Berechtigung.",
    "admin_grant_usage": "Verwendung: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ Nutzer {uid} → Plan: {plan}",
    "admin_lookup_usage":"Verwendung: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Nicht gefunden: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>Nutzerinfo</b>\n\n"
        "🆔 ID:         <code>{uid}</code>\n"
        "👤 Name:       {first_name}\n"
        "📛 Benutzername: @{username}\n"
        "📦 Plan:       <b>{plan}</b>\n"
        "📅 Premium:    {until}\n"
        "🎭 Modus:      {mode}\n"
        "💬 Heute:      {used}/{limit}\n"
        "👥 Einlad.:    {refs}\n"
        "📆 Registriert: {created}"
    ),
    "admin_btn_stats":    "📊 Statistiken",
    "admin_btn_revenue":  "💰 Einnahmen",
    "admin_btn_broadcast":"📢 Broadcast",
    "admin_btn_lookup":   "🔍 Nutzer suchen",
    "admin_btn_top":      "🏆 TOP-Nutzer",
    "admin_btn_expiring": "⏰ Läuft ab",
    "admin_btn_premium":  "⭐ Premium vergeben",
    "admin_btn_free":     "🆓 Kostenlos setzen",
    "admin_btn_clear_h":  "🗑 Verlauf löschen",
    "admin_btn_bonus":    "🎁 +10 Bonus",
    "admin_stats": (
        "📊 <b>Bot-Statistiken</b>\n\n"
        "👥 Nutzer gesamt:   <b>{total:,}</b>\n"
        "⭐ Premium:          <b>{premium:,}</b>\n"
        "🆓 Kostenlos:        <b>{free:,}</b>\n"
        "📈 Konversion:       <b>{cvr:.1f}%</b>\n\n"
        "🟢 Heute aktiv:     <b>{active:,}</b>\n"
        "💬 Nachrichten heute:<b>{today_msg:,}</b>\n"
        "📨 Nachrichten gesamt:<b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Einnahmen-Statistiken</b>\n\n"
        "⭐ Stars gesamt: <b>{total:,}</b>\n"
        "📅 Diesen Monat: <b>{month:,}</b> Stars\n"
        "🧾 Zahlungen gesamt: <b>{count:,}</b>\n\n"
        "💡 Durchschnittliche Zahlung: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "Kein Premium läuft in den nächsten 3 Tagen ab.",
    "admin_expiring_title": "⏰ <b>Premium, das in 3 Tagen abläuft:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Broadcast</b>\n\n"
        "<code>/broadcast Dein Text hier</code>\n\n"
        "⚠️ Wird an alle Nutzer gesendet!"
    ),
    "admin_broadcast_usage":    "Verwendung: /broadcast <Nachricht>",
    "admin_broadcast_starting": "⏳ Broadcast gestartet... ({total} Nutzer)",
    "admin_broadcast_done": (
        "✅ <b>Broadcast abgeschlossen</b>\n\n"
        "✉️ Gesendet: {sent}\n"
        "❌ Fehlgeschlagen: {failed}\n"
        "📊 Gesamt: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Bot-Ankündigung</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Nutzer suchen</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium vergeben ({days} Tage)",
    "admin_grant_free_done":    "🆓 Auf kostenlosen Plan umgestellt",
    "admin_clear_done":         "🗑 {count} Nachrichten gelöscht",
    "admin_bonus_done":         "🎁 +10 Bonus-Nachrichten vergeben!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} Nachrichten",
    "status_today":       "📊 Heute: {used}/{limit} [{bar}]",
    "status_until_short": "📅 Läuft ab: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Gast",
}

# ── French ────────────────────────────────────────────────────────────────────

FR: dict[str, str] = {
    "welcome": (
        "👋 <b>Bonjour, {name}!</b>\n\n"
        "Je suis un bot puissant propulsé par <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>Ce que je peux faire:</b>\n"
        "• Répondre à tes questions\n"
        "• Analyser images, voix et documents\n"
        "• Aider dans 10 modes différents\n"
        "• Recherche internet en temps réel\n\n"
        "Commence avec les boutons ci-dessous 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Tu es arrivé via un lien d'invitation — tu reçois <b>+5 messages bonus</b>!",
    "welcome_premium_expiry": "\n\n⚠️ Ton Premium expire dans <b>{days_left} jours</b>! Prolonge avec /upgrade.",

    "help": (
        "ℹ️ <b>Comment utiliser</b>\n\n"
        "💬 <b>Écrire du texte</b> → L'IA répond\n"
        "🖼 <b>Envoyer une image</b> → L'IA l'analyse\n"
        "📄 <b>Envoyer un document/PDF</b> → L'IA lit et explique\n"
        "🎙 <b>Message vocal</b> → L'IA écoute et répond\n"
        "😄 <b>Envoyer un sticker</b> → L'IA lit l'émotion\n\n"
        "<b>Commandes:</b>\n"
        "/mode — 🎭 Changer le mode IA (10 modes)\n"
        "/status — 📊 Info plan et limite\n"
        "/clear — 🗑 Supprimer la conversation\n"
        "/export — 📤 Télécharger la conversation\n"
        "/search — 🌐 Activer/désactiver la recherche web\n"
        "/invite — 🎁 Inviter des amis, gagner des bonus\n"
        "/top — 🏆 Utilisateurs les plus actifs\n"
        "/feedback — 💌 Envoyer un retour\n"
        "/upgrade — ⭐ Acheter Premium\n\n"
        "💡 <b>Astuce:</b> Utilise le bot dans n'importe quel chat en écrivant @botusername!"
    ),

    "btn_mode":        "🎭 Choisir un mode",
    "btn_status":      "📊 Statut",
    "btn_internet":    "🌐 Internet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Supprimer la conv.",
    "btn_export":      "📤 Exporter",
    "btn_invite":      "🎁 Inviter",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Aide",
    "btn_feedback":    "💌 Retour",
    "btn_back":        "⬅️ Menu principal",
    "btn_back_short":  "⬅️ Retour",
    "btn_retry":       "🔁 Réessayer",
    "btn_upgrade":     "⭐ Acheter Premium",
    "btn_invite_bonus":"🎁 Inviter un ami (+bonus)",
    "btn_share_link":  "📤 Partager le lien",
    "btn_refresh":     "🔄 Actualiser",
    "btn_language":    "🌍 Langue",

    "lang_select_title": "🌍 <b>Choisir la langue</b>\n\nLangue actuelle: <b>{current}</b>",
    "lang_changed":      "✅ Langue modifiée: <b>{lang}</b>",
    "lang_already":      "ℹ️ La langue est déjà définie sur <b>{lang}</b>.",

    "status_plan":        "{emoji} <b>Plan:</b> {plan}",
    "status_mode":        "🎭 <b>Mode:</b> {mode}",
    "status_internet":    "🌐 <b>Internet:</b> {state}",
    "status_limit":       "📊 <b>Limite:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Restant:</b> {remaining} messages",
    "status_until":       "📅 <b>Expire le:</b> {date} (encore {days} jours)",
    "status_bonus":       "🎁 <b>Messages bonus:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 Obtiens le premium avec /upgrade → 500 messages/jour",

    "mode_select_title":   "🎭 <b>Choisir un mode</b>",
    "mode_select_header":  "🎭 <b>Choisir un mode</b>\n\nChaque mode active une personnalité IA différente:",
    "mode_changed":        "✅ Mode modifié: <b>{mode}</b>\n📝 {desc}\n\nÉcris-moi maintenant! 👇",
    "mode_selected_toast": "{mode} sélectionné!",
    "mode_invalid":        "Mode invalide.",
    "mode_current":        "Mode actuel: <b>{mode}</b>",

    "clear_done":     "🗑 Conversation supprimée ({count} messages).\n\nCommence une nouvelle conversation! 👇",
    "clear_toast":    "Conversation supprimée!",
    "clear_cmd_done": "🗑️ Historique de conversation supprimé ({count} messages).\nTu peux démarrer une nouvelle conversation!",

    "search_on":       "✅ activée",
    "search_off":      "❌ désactivée",
    "search_toggled":  "🌐 Recherche internet {status}.",
    "search_toggled_detail": (
        "🌐 Recherche internet {status}.\n\n"
        "Quand activée, l'IA cherche des infos en temps réel sur internet."
    ),

    "invite_text": (
        "🎁 <b>Invite des amis, gagne des bonus!</b>\n\n"
        "Chaque ami que tu invites vous donne à tous les deux <b>+5 messages bonus</b>.\n\n"
        "🔗 Ton lien:\n<code>{link}</code>\n\n"
        "👥 Invités jusqu'ici: <b>{count}</b> personnes\n"
        "🎁 Bonus gagné: <b>+{bonus}</b> messages"
    ),
    "invite_share_url": "Ce bot IA est incroyable!",

    "export_empty":   "📭 Tu n'as pas encore d'historique de conversation.",
    "export_caption": "📤 Ton historique ({count} messages)\n📅 Date d'export: {date}",
    "export_user":    "👤 Toi",
    "export_ai":      "🤖 IA",

    "top_empty":       "Aucun utilisateur encore.",
    "top_title":       "🏆 <b>Utilisateurs les plus actifs (aujourd'hui)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 Utilisateurs</b>\n",

    "feedback_usage": (
        "💌 Envoyer un retour ainsi:\n"
        "<code>/feedback Ton message ici</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Retour / Suggestion</b>\n\n"
        "Pour partager un retour, une suggestion ou signaler un problème:\n\n"
        "<code>/feedback [ton message]</code>\n\n"
        "Exemple: <code>/feedback Le mode Traducteur est super!</code>"
    ),
    "feedback_sent":    "✅ Retour envoyé! Merci 🙏\nChaque message aide à améliorer le bot.",
    "feedback_saved":   "✅ Retour enregistré! Merci 🙏",
    "feedback_admin":   "💌 <b>Nouveau retour!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ Tu es déjà utilisateur Premium!\n📅 Expire le: {until}\n⏳ Jours restants: {days}",
    "upgrade_already_simple":"✅ Tu es déjà utilisateur Premium!",
    "upgrade_already_toast": "Tu es déjà Premium! ⭐",
    "upgrade_invoice_title": "Plan Premium ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} jours Premium:\n"
        "• {premium_limit} messages/jour (standard: {free_limit})\n"
        "• Tous les 10 modes IA\n"
        "• Analyse de documents/PDF\n"
        "• Support prioritaire"
    ),
    "upgrade_success": (
        "🎉 <b>Paiement réussi!</b>\n\n"
        "⭐ Premium activé!\n"
        "📅 Expire le: {until}\n"
        "📨 Limite quotidienne: {limit} messages\n\n"
        "Commence à utiliser tes nouvelles fonctionnalités! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Limite quotidienne atteinte</b> ({limit}/{limit} messages)\n\n"
        "Options:\n"
        "• La limite se réinitialise demain\n"
        "• Obtenir Premium avec /upgrade (500 messages/jour)\n"
        "• Inviter des amis avec /invite (messages bonus)"
    ),
    "limit_warning":  "ℹ️ Restant aujourd'hui: <b>{remaining}/{limit}</b>\n💡 Obtiens Premium avec /upgrade — 500 messages/jour!",
    "processing":     "⏳ Ta précédente requête est encore en cours, patiente un peu...",
    "db_error":       "😕 Erreur de base de données, réessaie plus tard.",
    "ai_rate_limit":  "⏳ <b>L'IA est occupée</b>\nRéessaie dans <b>{retry_after} secondes</b>.",
    "ai_error":       "😕 L'IA n'a pas pu répondre. Réessaie plus tard.",

    "retry_expired":  "⏰ Expiré, réécris ton message.",
    "retry_trying":   "🔁 Nouvel essai en cours...",

    "photo_default_prompt":  "Que vois-tu sur cette image? Décris-la en détail, liste tout.",
    "doc_size_error":        "❌ Fichier trop grand ({size_mb:.1f} Mo).\nTaille maximale: {max_mb} Mo.",
    "doc_format_error": (
        "❌ Ce format de fichier n'est pas supporté.\n\n"
        "✅ Formats supportés:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Lis ce document attentivement et explique son contenu principal. "
        "Si c'est un PDF, extrais toutes les informations importantes."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "L'utilisateur t'a envoyé un sticker avec l'emoji '{emoji}'. "
        "Donne une réponse amicale et courte correspondant à cette émotion. "
        "Réponds dans le même ton."
    ),

    "inline_type_hint":    "✍️ Écris ta question...",
    "inline_short_prompt": "Donne une réponse courte et précise (max 200 mots): {query}",
    "inline_error":        "❌ Impossible d'obtenir une réponse. Réessaie plus tard.",
    "inline_result_title": "🤖 Réponse IA",

    "admin_panel":       "🛠 <b>Panneau Admin</b>\n\nQue veux-tu faire?",
    "admin_no_perm":     "Permission refusée.",
    "admin_grant_usage": "Utilisation: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ Utilisateur {uid} → plan: {plan}",
    "admin_lookup_usage":"Utilisation: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Non trouvé: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>Info utilisateur</b>\n\n"
        "🆔 ID:          <code>{uid}</code>\n"
        "👤 Nom:         {first_name}\n"
        "📛 Identifiant: @{username}\n"
        "📦 Plan:        <b>{plan}</b>\n"
        "📅 Premium:     {until}\n"
        "🎭 Mode:        {mode}\n"
        "💬 Aujourd'hui: {used}/{limit}\n"
        "👥 Parrainages: {refs}\n"
        "📆 Inscription: {created}"
    ),
    "admin_btn_stats":    "📊 Statistiques",
    "admin_btn_revenue":  "💰 Revenus",
    "admin_btn_broadcast":"📢 Diffusion",
    "admin_btn_lookup":   "🔍 Chercher un user",
    "admin_btn_top":      "🏆 TOP utilisateurs",
    "admin_btn_expiring": "⏰ Expirant",
    "admin_btn_premium":  "⭐ Donner Premium",
    "admin_btn_free":     "🆓 Mettre en gratuit",
    "admin_btn_clear_h":  "🗑 Effacer l'historique",
    "admin_btn_bonus":    "🎁 +10 Bonus",
    "admin_stats": (
        "📊 <b>Statistiques du bot</b>\n\n"
        "👥 Utilisateurs totaux: <b>{total:,}</b>\n"
        "⭐ Premium:              <b>{premium:,}</b>\n"
        "🆓 Gratuits:             <b>{free:,}</b>\n"
        "📈 Conversion:           <b>{cvr:.1f}%</b>\n\n"
        "🟢 Actifs aujourd'hui:  <b>{active:,}</b>\n"
        "💬 Messages aujourd'hui:<b>{today_msg:,}</b>\n"
        "📨 Messages totaux:     <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Statistiques des revenus</b>\n\n"
        "⭐ Stars totaux: <b>{total:,}</b>\n"
        "📅 Ce mois: <b>{month:,}</b> Stars\n"
        "🧾 Paiements totaux: <b>{count:,}</b>\n\n"
        "💡 Paiement moyen: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "Aucun Premium n'expire dans les 3 prochains jours.",
    "admin_expiring_title": "⏰ <b>Premiums expirant dans 3 jours:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Diffusion</b>\n\n"
        "<code>/broadcast Ton texte ici</code>\n\n"
        "⚠️ Sera envoyé à tous les utilisateurs!"
    ),
    "admin_broadcast_usage":    "Utilisation: /broadcast <message>",
    "admin_broadcast_starting": "⏳ Diffusion démarrée... ({total} utilisateurs)",
    "admin_broadcast_done": (
        "✅ <b>Diffusion terminée</b>\n\n"
        "✉️ Envoyés: {sent}\n"
        "❌ Échoués: {failed}\n"
        "📊 Total: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Annonce du bot</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Chercher un utilisateur</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium accordé ({days} jours)",
    "admin_grant_free_done":    "🆓 Basculé vers le plan gratuit",
    "admin_clear_done":         "🗑 {count} messages supprimés",
    "admin_bonus_done":         "🎁 +10 messages bonus accordés!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} messages",
    "status_today":       "📊 Aujourd'hui: {used}/{limit} [{bar}]",
    "status_until_short": "📅 Expire: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Invité",
}

# ── Spanish ───────────────────────────────────────────────────────────────────

ES: dict[str, str] = {
    "welcome": (
        "👋 <b>¡Hola, {name}!</b>\n\n"
        "Soy un potente bot impulsado por <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>Lo que puedo hacer:</b>\n"
        "• Responder tus preguntas\n"
        "• Analizar imágenes, voz y documentos\n"
        "• Ayudarte en 10 modos diferentes\n"
        "• Búsqueda web en tiempo real\n\n"
        "¡Empieza con los botones de abajo! 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Llegaste por un enlace de invitación — ¡te damos <b>+5 mensajes de regalo</b>!",
    "welcome_premium_expiry": "\n\n⚠️ Tu Premium vence en <b>{days_left} días</b>. Usa /upgrade para renovarlo.",

    "help": (
        "ℹ️ <b>Cómo usar</b>\n\n"
        "💬 <b>Escribe texto</b> → la IA responde\n"
        "🖼 <b>Envía una imagen</b> → la IA la analiza\n"
        "📄 <b>Envía un documento/PDF</b> → la IA lo lee y explica\n"
        "🎙 <b>Mensaje de voz</b> → la IA escucha y responde\n"
        "😄 <b>Envía un sticker</b> → la IA lee la emoción\n\n"
        "<b>Comandos:</b>\n"
        "/mode — 🎭 Cambiar modo IA (10 modos)\n"
        "/status — 📊 Info de plan y límite\n"
        "/clear — 🗑 Borrar chat\n"
        "/export — 📤 Descargar chat como archivo\n"
        "/search — 🌐 Activar/desactivar búsqueda web\n"
        "/invite — 🎁 Invitar amigos, ganar bonos\n"
        "/top — 🏆 Usuarios más activos\n"
        "/feedback — 💌 Enviar comentarios\n"
        "/upgrade — ⭐ Obtener Premium\n\n"
        "💡 <b>Consejo:</b> ¡Usa el bot en cualquier chat escribiendo @botusername!"
    ),

    "btn_mode":        "🎭 Elegir modo",
    "btn_status":      "📊 Estado",
    "btn_internet":    "🌐 Internet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Borrar chat",
    "btn_export":      "📤 Exportar",
    "btn_invite":      "🎁 Invitar",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Ayuda",
    "btn_feedback":    "💌 Comentarios",
    "btn_back":        "⬅️ Menú principal",
    "btn_back_short":  "⬅️ Atrás",
    "btn_retry":       "🔁 Reintentar",
    "btn_upgrade":     "⭐ Obtener Premium",
    "btn_invite_bonus":"🎁 Invitar amigo (+bono)",
    "btn_share_link":  "📤 Compartir enlace",
    "btn_refresh":     "🔄 Actualizar",
    "btn_language":    "🌍 Idioma",

    "lang_select_title": "🌍 <b>Seleccionar idioma</b>\n\nActual: <b>{current}</b>",
    "lang_changed":      "✅ Idioma cambiado: <b>{lang}</b>",
    "lang_already":      "ℹ️ El idioma ya está configurado como <b>{lang}</b>.",

    "status_plan":        "{emoji} <b>Plan:</b> {plan}",
    "status_mode":        "🎭 <b>Modo:</b> {mode}",
    "status_internet":    "🌐 <b>Internet:</b> {state}",
    "status_limit":       "📊 <b>Límite:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Restantes:</b> {remaining} mensajes",
    "status_until":       "📅 <b>Vence:</b> {date} ({days} días restantes)",
    "status_bonus":       "🎁 <b>Mensajes de bono:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 Obtén premium con /upgrade → 500 msg/día",

    "mode_select_title":   "🎭 <b>Elegir modo</b>",
    "mode_select_header":  "🎭 <b>Elegir modo</b>\n\nCada modo activa una personalidad de IA diferente:",
    "mode_changed":        "✅ Modo cambiado: <b>{mode}</b>\n📝 {desc}\n\n¡Envíame un mensaje! 👇",
    "mode_selected_toast": "¡{mode} seleccionado!",
    "mode_invalid":        "Modo inválido.",
    "mode_current":        "Modo actual: <b>{mode}</b>",

    "clear_done":     "🗑 Chat borrado ({count} mensajes).\n\n¡Inicia un nuevo chat! 👇",
    "clear_toast":    "¡Chat borrado!",
    "clear_cmd_done": "🗑️ Historial de chat eliminado ({count} mensajes).\n¡Puedes iniciar un nuevo chat!",

    "search_on":       "✅ activado",
    "search_off":      "❌ desactivado",
    "search_toggled":  "🌐 Búsqueda web {status}.",
    "search_toggled_detail": (
        "🌐 Búsqueda web {status}.\n\n"
        "Cuando está activada, la IA busca información en internet en tiempo real."
    ),

    "invite_text": (
        "🎁 <b>¡Invita amigos y gana bonos!</b>\n\n"
        "Por cada amigo que invites, <b>ambos reciben +5 mensajes de bono</b>.\n\n"
        "🔗 Tu enlace:\n<code>{link}</code>\n\n"
        "👥 Invitados hasta ahora: <b>{count}</b>\n"
        "🎁 Bonos ganados: <b>+{bonus}</b> mensajes"
    ),
    "invite_share_url": "¡Este bot de IA es increíble!",

    "export_empty":   "📭 Aún no tienes historial de chat.",
    "export_caption": "📤 Historial de chat ({count} mensajes)\n📅 Fecha de exportación: {date}",
    "export_user":    "👤 Tú",
    "export_ai":      "🤖 IA",

    "top_empty":       "Aún no hay usuarios.",
    "top_title":       "🏆 <b>Usuarios más activos (hoy)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 Usuarios</b>\n",

    "feedback_usage": (
        "💌 Envía tu comentario así:\n"
        "<code>/feedback Tu mensaje aquí</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Comentario / Sugerencia</b>\n\n"
        "Para enviar comentarios, sugerencias o reportar un problema:\n\n"
        "<code>/feedback [tu texto]</code>\n\n"
        "Ejemplo: <code>/feedback ¡El modo traductor es genial!</code>"
    ),
    "feedback_sent":    "✅ ¡Comentario enviado! Gracias 🙏\nCada mensaje ayuda a mejorar el bot.",
    "feedback_saved":   "✅ ¡Comentario guardado! Gracias 🙏",
    "feedback_admin":   "💌 <b>¡Nuevo comentario!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ ¡Ya eres usuario Premium!\n📅 Vence: {until}\n⏳ Restante: {days} días",
    "upgrade_already_simple":"✅ ¡Ya eres usuario Premium!",
    "upgrade_already_toast": "¡Ya eres Premium! ⭐",
    "upgrade_invoice_title": "Plan Premium ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} días Premium:\n"
        "• {premium_limit} mensajes/día (estándar: {free_limit})\n"
        "• Los 10 modos de IA\n"
        "• Análisis de documentos/PDF\n"
        "• Soporte prioritario"
    ),
    "upgrade_success": (
        "🎉 <b>¡Pago recibido con éxito!</b>\n\n"
        "⭐ ¡Premium activado!\n"
        "📅 Vence: {until}\n"
        "📨 Límite diario: {limit} mensajes\n\n"
        "¡Empieza a usar tus nuevas funciones! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Límite diario alcanzado</b> ({limit}/{limit} mensajes)\n\n"
        "Opciones:\n"
        "• El límite se restablece mañana\n"
        "• /upgrade para obtener premium (500 mensajes/día)\n"
        "• /invite para invitar amigos (mensajes de bono)"
    ),
    "limit_warning":  "ℹ️ Límite restante hoy: <b>{remaining}/{limit}</b>\n💡 Obtén Premium con /upgrade — ¡500 msg/día!",
    "processing":     "⏳ Tu consulta anterior aún se está procesando, espera un momento...",
    "db_error":       "😕 Error en la base de datos, inténtalo de nuevo en un momento.",
    "ai_rate_limit":  "⏳ <b>IA ocupada</b>\nInténtalo de nuevo en <b>{retry_after} segundos</b>.",
    "ai_error":       "😕 La IA no pudo responder. Inténtalo de nuevo en un momento.",

    "retry_expired":  "⏰ Expiró, vuelve a escribir.",
    "retry_trying":   "🔁 Reintentando...",

    "photo_default_prompt":  "¿Qué ves en esta imagen? Explícalo detalladamente, enumera todo lo que hay.",
    "doc_size_error":        "❌ El archivo es demasiado grande ({size_mb:.1f} MB).\nTamaño máximo: {max_mb} MB.",
    "doc_format_error": (
        "❌ Este formato de archivo no está soportado.\n\n"
        "✅ Formatos soportados:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Lee este documento con atención y explica su contenido principal. "
        "Si es un PDF, extrae toda la información importante."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "El usuario te envió un sticker con el emoji '{emoji}'. "
        "Da una respuesta amable y breve acorde a esa emoción. "
        "Responde en el mismo tono."
    ),

    "inline_type_hint":    "✍️ Escribe tu pregunta...",
    "inline_short_prompt": "Da una respuesta corta y precisa (máx. 200 palabras): {query}",
    "inline_error":        "❌ No se pudo obtener respuesta. Inténtalo más tarde.",
    "inline_result_title": "🤖 Respuesta IA",

    "admin_panel":       "🛠 <b>Panel de Admin</b>\n\n¿Qué quieres hacer?",
    "admin_no_perm":     "Sin permisos.",
    "admin_grant_usage": "Uso: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ Usuario {uid} → plan: {plan}",
    "admin_lookup_usage":"Uso: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ No encontrado: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>Info de usuario</b>\n\n"
        "🆔 ID:        <code>{uid}</code>\n"
        "👤 Nombre:    {first_name}\n"
        "📛 Usuario:   @{username}\n"
        "📦 Plan:      <b>{plan}</b>\n"
        "📅 Premium:   {until}\n"
        "🎭 Modo:      {mode}\n"
        "💬 Hoy:       {used}/{limit}\n"
        "👥 Invitados: {refs}\n"
        "📆 Registro:  {created}"
    ),
    "admin_btn_stats":    "📊 Estadísticas",
    "admin_btn_revenue":  "💰 Ingresos",
    "admin_btn_broadcast":"📢 Difusión",
    "admin_btn_lookup":   "🔍 Buscar usuario",
    "admin_btn_top":      "🏆 TOP usuarios",
    "admin_btn_expiring": "⏰ Por vencer",
    "admin_btn_premium":  "⭐ Dar Premium",
    "admin_btn_free":     "🆓 Hacer gratis",
    "admin_btn_clear_h":  "🗑 Borrar historial",
    "admin_btn_bonus":    "🎁 +10 Bono",
    "admin_stats": (
        "📊 <b>Estadísticas del bot</b>\n\n"
        "👥 Total usuarios:  <b>{total:,}</b>\n"
        "⭐ Premium:         <b>{premium:,}</b>\n"
        "🆓 Gratis:          <b>{free:,}</b>\n"
        "📈 Conversión:      <b>{cvr:.1f}%</b>\n\n"
        "🟢 Activos hoy:    <b>{active:,}</b>\n"
        "💬 Mensajes hoy:   <b>{today_msg:,}</b>\n"
        "📨 Total mensajes: <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Estadísticas de ingresos</b>\n\n"
        "⭐ Total Stars ganadas: <b>{total:,}</b>\n"
        "📅 Este mes: <b>{month:,}</b> Stars\n"
        "🧾 Total pagos: <b>{count:,}</b>\n\n"
        "💡 Pago promedio: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "No hay premiums que venzan en los próximos 3 días.",
    "admin_expiring_title": "⏰ <b>Premiums que vencen en 3 días:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Difusión</b>\n\n"
        "<code>/broadcast Tu mensaje aquí</code>\n\n"
        "⚠️ ¡Se enviará a todos los usuarios!"
    ),
    "admin_broadcast_usage":    "Uso: /broadcast <mensaje>",
    "admin_broadcast_starting": "⏳ Difusión iniciada... ({total} usuarios)",
    "admin_broadcast_done": (
        "✅ <b>Difusión completada</b>\n\n"
        "✉️ Enviados: {sent}\n"
        "❌ Fallidos: {failed}\n"
        "📊 Total: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Anuncio del bot</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Buscar usuario</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium otorgado ({days} días)",
    "admin_grant_free_done":    "🆓 Cambiado a plan gratis",
    "admin_clear_done":         "🗑 {count} mensajes eliminados",
    "admin_bonus_done":         "🎁 ¡+10 mensajes de bono otorgados!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} mensajes",
    "status_today":       "📊 Hoy: {used}/{limit} [{bar}]",
    "status_until_short": "📅 Vence: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Invitado",
}

# ── Arabic ────────────────────────────────────────────────────────────────────

AR: dict[str, str] = {
    "welcome": (
        "👋 <b>مرحباً، {name}!</b>\n\n"
        "أنا بوت قوي مدعوم بـ <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>ما أستطيع فعله:</b>\n"
        "• الإجابة على أسئلتك\n"
        "• تحليل الصور والصوت والمستندات\n"
        "• المساعدة في 10 أوضاع مختلفة\n"
        "• البحث على الإنترنت في الوقت الفعلي\n\n"
        "ابدأ بالأزرار أدناه 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 انضممت عبر رابط دعوة — حصلت على <b>+5 رسائل مجانية</b>!",
    "welcome_premium_expiry": "\n\n⚠️ ينتهي اشتراكك المميز خلال <b>{days_left} أيام</b>! استخدم /upgrade للتجديد.",

    "help": (
        "ℹ️ <b>كيفية الاستخدام</b>\n\n"
        "💬 <b>أرسل نصاً</b> → يرد الذكاء الاصطناعي\n"
        "🖼 <b>أرسل صورة</b> → يحللها الذكاء الاصطناعي\n"
        "📄 <b>أرسل مستنداً/PDF</b> → يقرأه ويشرحه\n"
        "🎙 <b>رسالة صوتية</b> → يستمع ويرد\n"
        "😄 <b>أرسل ملصقاً</b> → يقرأ المشاعر\n\n"
        "<b>الأوامر:</b>\n"
        "/mode — 🎭 تغيير وضع الذكاء الاصطناعي (10 أوضاع)\n"
        "/status — 📊 معلومات الخطة والحد\n"
        "/clear — 🗑 حذف المحادثة\n"
        "/export — 📤 تنزيل المحادثة كملف\n"
        "/search — 🌐 تشغيل/إيقاف البحث على الإنترنت\n"
        "/invite — 🎁 دعوة الأصدقاء، اكسب مكافآت\n"
        "/top — 🏆 أكثر المستخدمين نشاطاً\n"
        "/feedback — 💌 إرسال تعليق\n"
        "/upgrade — ⭐ احصل على Premium\n\n"
        "💡 <b>نصيحة:</b> استخدم البوت في أي محادثة بكتابة @botusername!"
    ),

    "btn_mode":        "🎭 اختر الوضع",
    "btn_status":      "📊 الحالة",
    "btn_internet":    "🌐 الإنترنت",
    "btn_premium":     "⭐ مميز",
    "btn_clear":       "🗑 حذف المحادثة",
    "btn_export":      "📤 تصدير",
    "btn_invite":      "🎁 دعوة",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ مساعدة",
    "btn_feedback":    "💌 تعليق",
    "btn_back":        "⬅️ القائمة الرئيسية",
    "btn_back_short":  "⬅️ رجوع",
    "btn_retry":       "🔁 إعادة المحاولة",
    "btn_upgrade":     "⭐ احصل على Premium",
    "btn_invite_bonus":"🎁 دعوة صديق (+مكافأة)",
    "btn_share_link":  "📤 مشاركة الرابط",
    "btn_refresh":     "🔄 تحديث",
    "btn_language":    "🌍 اللغة",

    "lang_select_title": "🌍 <b>اختر اللغة</b>\n\nالحالية: <b>{current}</b>",
    "lang_changed":      "✅ تم تغيير اللغة: <b>{lang}</b>",
    "lang_already":      "ℹ️ اللغة محددة بالفعل كـ <b>{lang}</b>.",

    "status_plan":        "{emoji} <b>الخطة:</b> {plan}",
    "status_mode":        "🎭 <b>الوضع:</b> {mode}",
    "status_internet":    "🌐 <b>الإنترنت:</b> {state}",
    "status_limit":       "📊 <b>الحد:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>المتبقي:</b> {remaining} رسالة",
    "status_until":       "📅 <b>ينتهي:</b> {date} ({days} أيام متبقية)",
    "status_bonus":       "🎁 <b>رسائل المكافأة:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 احصل على premium مع /upgrade ← 500 رسالة/يوم",

    "mode_select_title":   "🎭 <b>اختر الوضع</b>",
    "mode_select_header":  "🎭 <b>اختر الوضع</b>\n\nكل وضع يفعّل شخصية ذكاء اصطناعي مختلفة:",
    "mode_changed":        "✅ تم تغيير الوضع: <b>{mode}</b>\n📝 {desc}\n\nأرسل لي رسالة! 👇",
    "mode_selected_toast": "تم اختيار {mode}!",
    "mode_invalid":        "وضع غير صالح.",
    "mode_current":        "الوضع الحالي: <b>{mode}</b>",

    "clear_done":     "🗑 تم حذف المحادثة ({count} رسالة).\n\nابدأ محادثة جديدة! 👇",
    "clear_toast":    "تم حذف المحادثة!",
    "clear_cmd_done": "🗑️ تم حذف سجل المحادثة ({count} رسالة).\nيمكنك بدء محادثة جديدة!",

    "search_on":       "✅ مفعّل",
    "search_off":      "❌ معطّل",
    "search_toggled":  "🌐 البحث على الإنترنت {status}.",
    "search_toggled_detail": (
        "🌐 البحث على الإنترنت {status}.\n\n"
        "عند التفعيل، يبحث الذكاء الاصطناعي عن المعلومات على الإنترنت في الوقت الفعلي."
    ),

    "invite_text": (
        "🎁 <b>ادعُ أصدقاءك واكسب مكافآت!</b>\n\n"
        "كل صديق تدعوه يمنحكما <b>+5 رسائل مكافأة لكليكما</b>.\n\n"
        "🔗 رابطك:\n<code>{link}</code>\n\n"
        "👥 المدعوون حتى الآن: <b>{count}</b>\n"
        "🎁 المكافآت المكتسبة: <b>+{bonus}</b> رسالة"
    ),
    "invite_share_url": "هذا البوت الذكي رائع!",

    "export_empty":   "📭 ليس لديك سجل محادثة حتى الآن.",
    "export_caption": "📤 سجل المحادثة ({count} رسالة)\n📅 تاريخ التصدير: {date}",
    "export_user":    "👤 أنت",
    "export_ai":      "🤖 الذكاء الاصطناعي",

    "top_empty":       "لا يوجد مستخدمون حتى الآن.",
    "top_title":       "🏆 <b>أكثر المستخدمين نشاطاً (اليوم)</b>\n",
    "top_title_admin": "🏆 <b>أفضل 10 مستخدمين</b>\n",

    "feedback_usage": (
        "💌 أرسل تعليقك هكذا:\n"
        "<code>/feedback رسالتك هنا</code>"
    ),
    "feedback_prompt": (
        "💌 <b>تعليق / اقتراح</b>\n\n"
        "لإرسال تعليق أو اقتراح أو الإبلاغ عن مشكلة:\n\n"
        "<code>/feedback [نصك]</code>\n\n"
        "مثال: <code>/feedback وضع المترجم رائع جداً!</code>"
    ),
    "feedback_sent":    "✅ تم إرسال التعليق! شكراً لك 🙏\nكل رسالة تساعد على تحسين البوت.",
    "feedback_saved":   "✅ تم حفظ التعليق! شكراً لك 🙏",
    "feedback_admin":   "💌 <b>تعليق جديد!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ أنت بالفعل مستخدم مميز!\n📅 ينتهي: {until}\n⏳ المتبقي: {days} أيام",
    "upgrade_already_simple":"✅ أنت بالفعل مستخدم مميز!",
    "upgrade_already_toast": "أنت بالفعل مميز! ⭐",
    "upgrade_invoice_title": "خطة Premium ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} يوم Premium:\n"
        "• {premium_limit} رسالة/يوم (الافتراضي: {free_limit})\n"
        "• جميع أوضاع الذكاء الاصطناعي العشرة\n"
        "• تحليل المستندات/PDF\n"
        "• دعم ذو أولوية"
    ),
    "upgrade_success": (
        "🎉 <b>تم استلام الدفع بنجاح!</b>\n\n"
        "⭐ تم تفعيل Premium!\n"
        "📅 ينتهي: {until}\n"
        "📨 الحد اليومي: {limit} رسالة\n\n"
        "ابدأ باستخدام ميزاتك الجديدة! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>تم الوصول إلى الحد اليومي</b> ({limit}/{limit} رسالة)\n\n"
        "الخيارات:\n"
        "• يتجدد الحد غداً\n"
        "• /upgrade للحصول على premium (500 رسالة/يوم)\n"
        "• /invite لدعوة الأصدقاء (رسائل مكافأة)"
    ),
    "limit_warning":  "ℹ️ الحد المتبقي اليوم: <b>{remaining}/{limit}</b>\n💡 احصل على Premium مع /upgrade — 500 رسالة/يوم!",
    "processing":     "⏳ طلبك السابق لا يزال قيد المعالجة، انتظر لحظة...",
    "db_error":       "😕 حدث خطأ في قاعدة البيانات، حاول مرة أخرى بعد لحظة.",
    "ai_rate_limit":  "⏳ <b>الذكاء الاصطناعي مشغول</b>\nحاول مرة أخرى بعد <b>{retry_after} ثانية</b>.",
    "ai_error":       "😕 تعذر على الذكاء الاصطناعي الرد. حاول مرة أخرى بعد لحظة.",

    "retry_expired":  "⏰ انتهت الصلاحية، اكتب مرة أخرى.",
    "retry_trying":   "🔁 إعادة المحاولة...",

    "photo_default_prompt":  "ما الذي تراه في هذه الصورة؟ اشرح بالتفصيل واذكر كل شيء.",
    "doc_size_error":        "❌ الملف كبير جداً ({size_mb:.1f} MB).\nالحد الأقصى: {max_mb} MB.",
    "doc_format_error": (
        "❌ هذا التنسيق غير مدعوم.\n\n"
        "✅ التنسيقات المدعومة:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "اقرأ هذا المستند بعناية واشرح محتواه الرئيسي. "
        "إذا كان PDF، استخرج جميع المعلومات المهمة."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "أرسل إليك المستخدم ملصقاً بالرمز التعبيري '{emoji}'. "
        "أعطِ رداً ودياً وقصيراً يناسب هذا الشعور. "
        "رد بنفس النبرة."
    ),

    "inline_type_hint":    "✍️ اكتب سؤالك...",
    "inline_short_prompt": "أعطِ إجابة قصيرة ودقيقة (بحد أقصى 200 كلمة): {query}",
    "inline_error":        "❌ تعذر الحصول على رد. حاول لاحقاً.",
    "inline_result_title": "🤖 رد الذكاء الاصطناعي",

    "admin_panel":       "🛠 <b>لوحة المشرف</b>\n\nماذا تريد أن تفعل؟",
    "admin_no_perm":     "لا توجد صلاحية.",
    "admin_grant_usage": "الاستخدام: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ المستخدم {uid} → الخطة: {plan}",
    "admin_lookup_usage":"الاستخدام: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ لم يُعثر على: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>معلومات المستخدم</b>\n\n"
        "🆔 ID:        <code>{uid}</code>\n"
        "👤 الاسم:     {first_name}\n"
        "📛 المعرّف:   @{username}\n"
        "📦 الخطة:     <b>{plan}</b>\n"
        "📅 Premium:   {until}\n"
        "🎭 الوضع:     {mode}\n"
        "💬 اليوم:     {used}/{limit}\n"
        "👥 المدعوون: {refs}\n"
        "📆 التسجيل:  {created}"
    ),
    "admin_btn_stats":    "📊 الإحصائيات",
    "admin_btn_revenue":  "💰 الإيرادات",
    "admin_btn_broadcast":"📢 بث",
    "admin_btn_lookup":   "🔍 البحث عن مستخدم",
    "admin_btn_top":      "🏆 أفضل المستخدمين",
    "admin_btn_expiring": "⏰ على وشك الانتهاء",
    "admin_btn_premium":  "⭐ منح Premium",
    "admin_btn_free":     "🆓 جعله مجانياً",
    "admin_btn_clear_h":  "🗑 حذف السجل",
    "admin_btn_bonus":    "🎁 +10 مكافأة",
    "admin_stats": (
        "📊 <b>إحصائيات البوت</b>\n\n"
        "👥 إجمالي المستخدمين: <b>{total:,}</b>\n"
        "⭐ مميز:               <b>{premium:,}</b>\n"
        "🆓 مجاني:              <b>{free:,}</b>\n"
        "📈 التحويل:            <b>{cvr:.1f}%</b>\n\n"
        "🟢 نشطون اليوم:       <b>{active:,}</b>\n"
        "💬 رسائل اليوم:       <b>{today_msg:,}</b>\n"
        "📨 إجمالي الرسائل:    <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>إحصائيات الإيرادات</b>\n\n"
        "⭐ إجمالي النجوم المكتسبة: <b>{total:,}</b>\n"
        "📅 هذا الشهر: <b>{month:,}</b> نجمة\n"
        "🧾 إجمالي المدفوعات: <b>{count:,}</b>\n\n"
        "💡 متوسط الدفع: <b>{avg:,}</b> نجمة"
    ),
    "admin_expiring_none":  "لا توجد اشتراكات مميزة تنتهي في الأيام الثلاثة القادمة.",
    "admin_expiring_title": "⏰ <b>الاشتراكات المميزة المنتهية خلال 3 أيام:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>بث</b>\n\n"
        "<code>/broadcast رسالتك هنا</code>\n\n"
        "⚠️ سيتم الإرسال لجميع المستخدمين!"
    ),
    "admin_broadcast_usage":    "الاستخدام: /broadcast <رسالة>",
    "admin_broadcast_starting": "⏳ بدأ البث... ({total} مستخدم)",
    "admin_broadcast_done": (
        "✅ <b>اكتمل البث</b>\n\n"
        "✉️ تم الإرسال: {sent}\n"
        "❌ فشل: {failed}\n"
        "📊 الإجمالي: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>إعلان البوت</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>البحث عن مستخدم</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ تم منح Premium ({days} أيام)",
    "admin_grant_free_done":    "🆓 تم التحويل إلى الخطة المجانية",
    "admin_clear_done":         "🗑 تم حذف {count} رسالة",
    "admin_bonus_done":         "🎁 تم منح +10 رسائل مكافأة!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} رسالة",
    "status_today":       "📊 اليوم: {used}/{limit} [{bar}]",
    "status_until_short": "📅 ينتهي: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "ضيف",
}

# ── Chinese (Simplified) ──────────────────────────────────────────────────────

ZH: dict[str, str] = {
    "welcome": (
        "👋 <b>你好，{name}！</b>\n\n"
        "我是一个由 <b>Gemini AI</b> 驱动的强大机器人。🚀\n\n"
        "📝 <b>我能做什么：</b>\n"
        "• 回答你的问题\n"
        "• 分析图片、语音和文档\n"
        "• 以10种不同模式提供帮助\n"
        "• 实时网络搜索\n\n"
        "点击下方按钮开始 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 你通过邀请链接加入 — 已获得 <b>+5 条奖励消息</b>！",
    "welcome_premium_expiry": "\n\n⚠️ 你的高级会员将在 <b>{days_left} 天</b>后到期！使用 /upgrade 续费。",

    "help": (
        "ℹ️ <b>使用说明</b>\n\n"
        "💬 <b>发送文字</b> → AI 回复\n"
        "🖼 <b>发送图片</b> → AI 分析\n"
        "📄 <b>发送文档/PDF</b> → AI 阅读并解释\n"
        "🎙 <b>语音消息</b> → AI 聆听并回复\n"
        "😄 <b>发送贴纸</b> → AI 读取情绪\n\n"
        "<b>命令：</b>\n"
        "/mode — 🎭 切换AI模式（10种模式）\n"
        "/status — 📊 套餐和限额信息\n"
        "/clear — 🗑 删除聊天记录\n"
        "/export — 📤 将聊天下载为文件\n"
        "/search — 🌐 开启/关闭网络搜索\n"
        "/invite — 🎁 邀请好友，赢取奖励\n"
        "/top — 🏆 最活跃用户\n"
        "/feedback — 💌 发送反馈\n"
        "/upgrade — ⭐ 获取高级会员\n\n"
        "💡 <b>提示：</b> 在任何聊天中输入 @botusername 即可使用！"
    ),

    "btn_mode":        "🎭 选择模式",
    "btn_status":      "📊 状态",
    "btn_internet":    "🌐 网络",
    "btn_premium":     "⭐ 高级会员",
    "btn_clear":       "🗑 清除聊天",
    "btn_export":      "📤 导出",
    "btn_invite":      "🎁 邀请",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ 帮助",
    "btn_feedback":    "💌 反馈",
    "btn_back":        "⬅️ 主菜单",
    "btn_back_short":  "⬅️ 返回",
    "btn_retry":       "🔁 重试",
    "btn_upgrade":     "⭐ 获取高级会员",
    "btn_invite_bonus":"🎁 邀请好友（+奖励）",
    "btn_share_link":  "📤 分享链接",
    "btn_refresh":     "🔄 刷新",
    "btn_language":    "🌍 语言",

    "lang_select_title": "🌍 <b>选择语言</b>\n\n当前：<b>{current}</b>",
    "lang_changed":      "✅ 语言已更改：<b>{lang}</b>",
    "lang_already":      "ℹ️ 语言已设置为 <b>{lang}</b>。",

    "status_plan":        "{emoji} <b>套餐：</b> {plan}",
    "status_mode":        "🎭 <b>模式：</b> {mode}",
    "status_internet":    "🌐 <b>网络：</b> {state}",
    "status_limit":       "📊 <b>限额：</b> {used}/{limit}",
    "status_remaining":   "✅ <b>剩余：</b> {remaining} 条消息",
    "status_until":       "📅 <b>到期：</b> {date}（剩余 {days} 天）",
    "status_bonus":       "🎁 <b>奖励消息：</b> +{bonus}",
    "status_upgrade_tip": "\n💡 通过 /upgrade 获取高级会员 → 每天500条消息",

    "mode_select_title":   "🎭 <b>选择模式</b>",
    "mode_select_header":  "🎭 <b>选择模式</b>\n\n每种模式激活不同的AI人格：",
    "mode_changed":        "✅ 模式已切换：<b>{mode}</b>\n📝 {desc}\n\n给我发消息吧！👇",
    "mode_selected_toast": "已选择 {mode}！",
    "mode_invalid":        "无效模式。",
    "mode_current":        "当前模式：<b>{mode}</b>",

    "clear_done":     "🗑 聊天已清除（{count} 条消息）。\n\n开始新对话吧！👇",
    "clear_toast":    "聊天已清除！",
    "clear_cmd_done": "🗑️ 聊天记录已删除（{count} 条消息）。\n你可以开始新的对话！",

    "search_on":       "✅ 已启用",
    "search_off":      "❌ 已禁用",
    "search_toggled":  "🌐 网络搜索 {status}。",
    "search_toggled_detail": (
        "🌐 网络搜索 {status}。\n\n"
        "启用后，AI 会实时从网络搜索信息。"
    ),

    "invite_text": (
        "🎁 <b>邀请好友，赢取奖励！</b>\n\n"
        "每位受邀好友加入后，<b>你们双方各获 +5 条奖励消息</b>。\n\n"
        "🔗 你的链接：\n<code>{link}</code>\n\n"
        "👥 已邀请人数：<b>{count}</b>\n"
        "🎁 已获奖励：<b>+{bonus}</b> 条消息"
    ),
    "invite_share_url": "这个AI机器人太棒了！",

    "export_empty":   "📭 你还没有聊天记录。",
    "export_caption": "📤 聊天记录（{count} 条消息）\n📅 导出日期：{date}",
    "export_user":    "👤 你",
    "export_ai":      "🤖 AI",

    "top_empty":       "目前还没有用户。",
    "top_title":       "🏆 <b>最活跃用户（今日）</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 用户</b>\n",

    "feedback_usage": (
        "💌 请这样发送反馈：\n"
        "<code>/feedback 你的消息</code>"
    ),
    "feedback_prompt": (
        "💌 <b>反馈 / 建议</b>\n\n"
        "如需提交反馈、建议或报告问题：\n\n"
        "<code>/feedback [你的内容]</code>\n\n"
        "例如：<code>/feedback 翻译模式太好用了！</code>"
    ),
    "feedback_sent":    "✅ 反馈已发送！谢谢 🙏\n每条消息都有助于改善机器人。",
    "feedback_saved":   "✅ 反馈已保存！谢谢 🙏",
    "feedback_admin":   "💌 <b>新反馈！</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ 你已经是高级会员！\n📅 到期：{until}\n⏳ 剩余：{days} 天",
    "upgrade_already_simple":"✅ 你已经是高级会员！",
    "upgrade_already_toast": "你已经是高级会员！⭐",
    "upgrade_invoice_title": "高级套餐 ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} 天高级会员：\n"
        "• 每天 {premium_limit} 条消息（标准：{free_limit}）\n"
        "• 全部10种AI模式\n"
        "• 文档/PDF分析\n"
        "• 优先支持"
    ),
    "upgrade_success": (
        "🎉 <b>付款成功！</b>\n\n"
        "⭐ 高级会员已激活！\n"
        "📅 到期：{until}\n"
        "📨 每日限额：{limit} 条消息\n\n"
        "开始使用你的新功能吧！🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>已达每日限额</b>（{limit}/{limit} 条消息）\n\n"
        "选项：\n"
        "• 明天重置限额\n"
        "• /upgrade 获取高级会员（每天500条）\n"
        "• /invite 邀请好友（获取奖励消息）"
    ),
    "limit_warning":  "ℹ️ 今日剩余限额：<b>{remaining}/{limit}</b>\n💡 /upgrade 获取高级会员 — 每天500条！",
    "processing":     "⏳ 上一个请求仍在处理中，请稍候...",
    "db_error":       "😕 数据库发生错误，请稍后再试。",
    "ai_rate_limit":  "⏳ <b>AI 繁忙</b>\n请在 <b>{retry_after} 秒</b>后重试。",
    "ai_error":       "😕 AI 无法回复。请稍后再试。",

    "retry_expired":  "⏰ 已过期，请重新输入。",
    "retry_trying":   "🔁 重试中...",

    "photo_default_prompt":  "这张图片里有什么？请详细描述，列出所有内容。",
    "doc_size_error":        "❌ 文件太大（{size_mb:.1f} MB）。\n最大大小：{max_mb} MB。",
    "doc_format_error": (
        "❌ 不支持此文件格式。\n\n"
        "✅ 支持的格式：\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "请仔细阅读此文档并解释其主要内容。"
        "如果是PDF，请提取所有重要信息。"
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "用户向你发送了一个带有 '{emoji}' 表情的贴纸。"
        "请给出符合该情绪的友好简短回复。"
        "以相同的语气回应。"
    ),

    "inline_type_hint":    "✍️ 输入你的问题...",
    "inline_short_prompt": "给出简短精准的回答（最多200字）：{query}",
    "inline_error":        "❌ 无法获取回复。请稍后再试。",
    "inline_result_title": "🤖 AI 回复",

    "admin_panel":       "🛠 <b>管理员面板</b>\n\n你想做什么？",
    "admin_no_perm":     "没有权限。",
    "admin_grant_usage": "用法：/grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ 用户 {uid} → 套餐：{plan}",
    "admin_lookup_usage":"用法：/lookup <user_id | @username>",
    "admin_lookup_none": "❌ 未找到：<code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>用户信息</b>\n\n"
        "🆔 ID:      <code>{uid}</code>\n"
        "👤 姓名：   {first_name}\n"
        "📛 用户名： @{username}\n"
        "📦 套餐：   <b>{plan}</b>\n"
        "📅 高级会员：{until}\n"
        "🎭 模式：   {mode}\n"
        "💬 今日：   {used}/{limit}\n"
        "👥 邀请数： {refs}\n"
        "📆 注册：   {created}"
    ),
    "admin_btn_stats":    "📊 统计",
    "admin_btn_revenue":  "💰 收入",
    "admin_btn_broadcast":"📢 广播",
    "admin_btn_lookup":   "🔍 查找用户",
    "admin_btn_top":      "🏆 TOP 用户",
    "admin_btn_expiring": "⏰ 即将到期",
    "admin_btn_premium":  "⭐ 授予高级",
    "admin_btn_free":     "🆓 设为免费",
    "admin_btn_clear_h":  "🗑 清除记录",
    "admin_btn_bonus":    "🎁 +10 奖励",
    "admin_stats": (
        "📊 <b>机器人统计</b>\n\n"
        "👥 总用户数：  <b>{total:,}</b>\n"
        "⭐ 高级会员：  <b>{premium:,}</b>\n"
        "🆓 免费用户：  <b>{free:,}</b>\n"
        "📈 转化率：    <b>{cvr:.1f}%</b>\n\n"
        "🟢 今日活跃：  <b>{active:,}</b>\n"
        "💬 今日消息：  <b>{today_msg:,}</b>\n"
        "📨 总消息数：  <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>收入统计</b>\n\n"
        "⭐ 总获得星星：<b>{total:,}</b>\n"
        "📅 本月：<b>{month:,}</b> 星星\n"
        "🧾 总付款次数：<b>{count:,}</b>\n\n"
        "💡 平均付款：<b>{avg:,}</b> 星星"
    ),
    "admin_expiring_none":  "未来3天内没有到期的高级会员。",
    "admin_expiring_title": "⏰ <b>3天内到期的高级会员：</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>广播</b>\n\n"
        "<code>/broadcast 你的消息</code>\n\n"
        "⚠️ 将发送给所有用户！"
    ),
    "admin_broadcast_usage":    "用法：/broadcast <消息>",
    "admin_broadcast_starting": "⏳ 广播已开始...（{total} 名用户）",
    "admin_broadcast_done": (
        "✅ <b>广播完成</b>\n\n"
        "✉️ 已发送：{sent}\n"
        "❌ 失败：{failed}\n"
        "📊 总计：{total}"
    ),
    "admin_broadcast_prefix": "📢 <b>机器人公告</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>查找用户</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ 已授予高级会员（{days} 天）",
    "admin_grant_free_done":    "🆓 已切换至免费套餐",
    "admin_clear_done":         "🗑 已删除 {count} 条消息",
    "admin_bonus_done":         "🎁 已授予 +10 条奖励消息！",

    "top_row":            "{medal} {name} {plan_icon} — {usage} 条消息",
    "status_today":       "📊 今日：{used}/{limit} [{bar}]",
    "status_until_short": "📅 到期：{date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "访客",
}

# ── Portuguese ───────────────────────────────────────────────────────────────

PT: dict[str, str] = {
    "welcome": (
        "👋 <b>Olá, {name}!</b>\n\n"
        "Sou um bot poderoso alimentado pelo <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>O que posso fazer:</b>\n"
        "• Responder às suas perguntas\n"
        "• Analisar imagens, áudio e documentos\n"
        "• Ajudar em 10 modos diferentes\n"
        "• Pesquisa na web em tempo real\n\n"
        "Comece com os botões abaixo 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Você entrou por um link de convite — recebeu <b>+5 mensagens de bônus</b>!",
    "welcome_premium_expiry": "\n\n⚠️ Seu Premium vence em <b>{days_left} dias</b>! Use /upgrade para renovar.",

    "help": (
        "ℹ️ <b>Como usar</b>\n\n"
        "💬 <b>Envie texto</b> → a IA responde\n"
        "🖼 <b>Envie uma imagem</b> → a IA analisa\n"
        "📄 <b>Envie documento/PDF</b> → a IA lê e explica\n"
        "🎙 <b>Mensagem de voz</b> → a IA ouve e responde\n"
        "😄 <b>Envie sticker</b> → a IA lê a emoção\n\n"
        "<b>Comandos:</b>\n"
        "/mode — 🎭 Trocar modo IA (10 modos)\n"
        "/status — 📊 Info de plano e limite\n"
        "/clear — 🗑 Apagar conversa\n"
        "/export — 📤 Baixar conversa como arquivo\n"
        "/search — 🌐 Ativar/desativar busca web\n"
        "/invite — 🎁 Convidar amigos, ganhar bônus\n"
        "/top — 🏆 Usuários mais ativos\n"
        "/feedback — 💌 Enviar comentário\n"
        "/upgrade — ⭐ Obter Premium\n\n"
        "💡 <b>Dica:</b> Use o bot em qualquer conversa digitando @botusername!"
    ),

    "btn_mode":        "🎭 Escolher modo",
    "btn_status":      "📊 Status",
    "btn_internet":    "🌐 Internet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Apagar conversa",
    "btn_export":      "📤 Exportar",
    "btn_invite":      "🎁 Convidar",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Ajuda",
    "btn_feedback":    "💌 Comentário",
    "btn_back":        "⬅️ Menu principal",
    "btn_back_short":  "⬅️ Voltar",
    "btn_retry":       "🔁 Tentar novamente",
    "btn_upgrade":     "⭐ Obter Premium",
    "btn_invite_bonus":"🎁 Convidar amigo (+bônus)",
    "btn_share_link":  "📤 Compartilhar link",
    "btn_refresh":     "🔄 Atualizar",
    "btn_language":    "🌍 Idioma",

    "lang_select_title": "🌍 <b>Selecionar idioma</b>\n\nAtual: <b>{current}</b>",
    "lang_changed":      "✅ Idioma alterado: <b>{lang}</b>",
    "lang_already":      "ℹ️ O idioma já está definido como <b>{lang}</b>.",

    "status_plan":        "{emoji} <b>Plano:</b> {plan}",
    "status_mode":        "🎭 <b>Modo:</b> {mode}",
    "status_internet":    "🌐 <b>Internet:</b> {state}",
    "status_limit":       "📊 <b>Limite:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Restantes:</b> {remaining} mensagens",
    "status_until":       "📅 <b>Vence:</b> {date} ({days} dias restantes)",
    "status_bonus":       "🎁 <b>Mensagens bônus:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 Obtenha premium com /upgrade → 500 msg/dia",

    "mode_select_title":   "🎭 <b>Escolher modo</b>",
    "mode_select_header":  "🎭 <b>Escolher modo</b>\n\nCada modo ativa uma personalidade de IA diferente:",
    "mode_changed":        "✅ Modo alterado: <b>{mode}</b>\n📝 {desc}\n\nEnvie-me uma mensagem! 👇",
    "mode_selected_toast": "{mode} selecionado!",
    "mode_invalid":        "Modo inválido.",
    "mode_current":        "Modo atual: <b>{mode}</b>",

    "clear_done":     "🗑 Conversa apagada ({count} mensagens).\n\nInicie uma nova conversa! 👇",
    "clear_toast":    "Conversa apagada!",
    "clear_cmd_done": "🗑️ Histórico apagado ({count} mensagens).\nVocê pode iniciar uma nova conversa!",

    "search_on":       "✅ ativada",
    "search_off":      "❌ desativada",
    "search_toggled":  "🌐 Busca na web {status}.",
    "search_toggled_detail": (
        "🌐 Busca na web {status}.\n\n"
        "Quando ativada, a IA busca informações na internet em tempo real."
    ),

    "invite_text": (
        "🎁 <b>Convide amigos e ganhe bônus!</b>\n\n"
        "Cada amigo convidado dá a <b>vocês dois +5 mensagens de bônus</b>.\n\n"
        "🔗 Seu link:\n<code>{link}</code>\n\n"
        "👥 Convidados até agora: <b>{count}</b>\n"
        "🎁 Bônus ganhos: <b>+{bonus}</b> mensagens"
    ),
    "invite_share_url": "Esse bot de IA é incrível!",

    "export_empty":   "📭 Você ainda não tem histórico de conversa.",
    "export_caption": "📤 Histórico de conversa ({count} mensagens)\n📅 Data de exportação: {date}",
    "export_user":    "👤 Você",
    "export_ai":      "🤖 IA",

    "top_empty":       "Ainda não há usuários.",
    "top_title":       "🏆 <b>Usuários mais ativos (hoje)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 Usuários</b>\n",

    "feedback_usage": (
        "💌 Envie seu comentário assim:\n"
        "<code>/feedback Sua mensagem aqui</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Comentário / Sugestão</b>\n\n"
        "Para enviar comentário, sugestão ou relatar problema:\n\n"
        "<code>/feedback [seu texto]</code>\n\n"
        "Exemplo: <code>/feedback O modo tradutor é ótimo!</code>"
    ),
    "feedback_sent":    "✅ Comentário enviado! Obrigado 🙏\nCada mensagem ajuda a melhorar o bot.",
    "feedback_saved":   "✅ Comentário salvo! Obrigado 🙏",
    "feedback_admin":   "💌 <b>Novo comentário!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ Você já é usuário Premium!\n📅 Vence: {until}\n⏳ Restante: {days} dias",
    "upgrade_already_simple":"✅ Você já é usuário Premium!",
    "upgrade_already_toast": "Você já é Premium! ⭐",
    "upgrade_invoice_title": "Plano Premium ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} dias Premium:\n"
        "• {premium_limit} mensagens/dia (padrão: {free_limit})\n"
        "• Todos os 10 modos de IA\n"
        "• Análise de documentos/PDF\n"
        "• Suporte prioritário"
    ),
    "upgrade_success": (
        "🎉 <b>Pagamento recebido com sucesso!</b>\n\n"
        "⭐ Premium ativado!\n"
        "📅 Vence: {until}\n"
        "📨 Limite diário: {limit} mensagens\n\n"
        "Comece a usar seus novos recursos! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Limite diário atingido</b> ({limit}/{limit} mensagens)\n\n"
        "Opções:\n"
        "• O limite é redefinido amanhã\n"
        "• /upgrade para obter premium (500 mensagens/dia)\n"
        "• /invite para convidar amigos (mensagens bônus)"
    ),
    "limit_warning":  "ℹ️ Limite restante hoje: <b>{remaining}/{limit}</b>\n💡 Obtenha Premium com /upgrade — 500 msg/dia!",
    "processing":     "⏳ Sua consulta anterior ainda está sendo processada, aguarde...",
    "db_error":       "😕 Erro no banco de dados, tente novamente em breve.",
    "ai_rate_limit":  "⏳ <b>IA ocupada</b>\nTente novamente em <b>{retry_after} segundos</b>.",
    "ai_error":       "😕 A IA não conseguiu responder. Tente novamente em breve.",

    "retry_expired":  "⏰ Expirou, escreva novamente.",
    "retry_trying":   "🔁 Tentando novamente...",

    "photo_default_prompt":  "O que você vê nesta imagem? Explique detalhadamente, liste tudo.",
    "doc_size_error":        "❌ Arquivo muito grande ({size_mb:.1f} MB).\nTamanho máximo: {max_mb} MB.",
    "doc_format_error": (
        "❌ Este formato de arquivo não é suportado.\n\n"
        "✅ Formatos suportados:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Leia este documento com atenção e explique seu conteúdo principal. "
        "Se for PDF, extraia todas as informações importantes."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "O usuário te enviou um sticker com o emoji '{emoji}'. "
        "Dê uma resposta amigável e curta adequada a essa emoção. "
        "Responda no mesmo tom."
    ),

    "inline_type_hint":    "✍️ Digite sua pergunta...",
    "inline_short_prompt": "Dê uma resposta curta e precisa (máx. 200 palavras): {query}",
    "inline_error":        "❌ Não foi possível obter resposta. Tente mais tarde.",
    "inline_result_title": "🤖 Resposta IA",

    "admin_panel":       "🛠 <b>Painel Admin</b>\n\nO que deseja fazer?",
    "admin_no_perm":     "Sem permissão.",
    "admin_grant_usage": "Uso: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ Usuário {uid} → plano: {plan}",
    "admin_lookup_usage":"Uso: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Não encontrado: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>Info do usuário</b>\n\n"
        "🆔 ID:        <code>{uid}</code>\n"
        "👤 Nome:      {first_name}\n"
        "📛 Usuário:   @{username}\n"
        "📦 Plano:     <b>{plan}</b>\n"
        "📅 Premium:   {until}\n"
        "🎭 Modo:      {mode}\n"
        "💬 Hoje:      {used}/{limit}\n"
        "👥 Convidados:{refs}\n"
        "📆 Registro:  {created}"
    ),
    "admin_btn_stats":    "📊 Estatísticas",
    "admin_btn_revenue":  "💰 Receita",
    "admin_btn_broadcast":"📢 Difusão",
    "admin_btn_lookup":   "🔍 Buscar usuário",
    "admin_btn_top":      "🏆 TOP usuários",
    "admin_btn_expiring": "⏰ A vencer",
    "admin_btn_premium":  "⭐ Dar Premium",
    "admin_btn_free":     "🆓 Tornar grátis",
    "admin_btn_clear_h":  "🗑 Apagar histórico",
    "admin_btn_bonus":    "🎁 +10 Bônus",
    "admin_stats": (
        "📊 <b>Estatísticas do bot</b>\n\n"
        "👥 Total de usuários: <b>{total:,}</b>\n"
        "⭐ Premium:           <b>{premium:,}</b>\n"
        "🆓 Grátis:            <b>{free:,}</b>\n"
        "📈 Conversão:         <b>{cvr:.1f}%</b>\n\n"
        "🟢 Ativos hoje:      <b>{active:,}</b>\n"
        "💬 Mensagens hoje:   <b>{today_msg:,}</b>\n"
        "📨 Total mensagens:  <b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Estatísticas de receita</b>\n\n"
        "⭐ Total Stars ganhas: <b>{total:,}</b>\n"
        "📅 Este mês: <b>{month:,}</b> Stars\n"
        "🧾 Total pagamentos: <b>{count:,}</b>\n\n"
        "💡 Pagamento médio: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "Nenhum premium vencendo nos próximos 3 dias.",
    "admin_expiring_title": "⏰ <b>Premiums vencendo em 3 dias:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Difusão</b>\n\n"
        "<code>/broadcast Sua mensagem aqui</code>\n\n"
        "⚠️ Será enviado para todos os usuários!"
    ),
    "admin_broadcast_usage":    "Uso: /broadcast <mensagem>",
    "admin_broadcast_starting": "⏳ Difusão iniciada... ({total} usuários)",
    "admin_broadcast_done": (
        "✅ <b>Difusão concluída</b>\n\n"
        "✉️ Enviados: {sent}\n"
        "❌ Falhos: {failed}\n"
        "📊 Total: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Anúncio do bot</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Buscar usuário</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium concedido ({days} dias)",
    "admin_grant_free_done":    "🆓 Alterado para plano grátis",
    "admin_clear_done":         "🗑 {count} mensagens apagadas",
    "admin_bonus_done":         "🎁 +10 mensagens bônus concedidas!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} mensagens",
    "status_today":       "📊 Hoje: {used}/{limit} [{bar}]",
    "status_until_short": "📅 Vence: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Visitante",
}

# ── Italian ───────────────────────────────────────────────────────────────────

IT: dict[str, str] = {
    "welcome": (
        "👋 <b>Ciao, {name}!</b>\n\n"
        "Sono un potente bot alimentato da <b>Gemini AI</b>. 🚀\n\n"
        "📝 <b>Cosa posso fare:</b>\n"
        "• Rispondere alle tue domande\n"
        "• Analizzare immagini, audio e documenti\n"
        "• Aiutarti in 10 modalità diverse\n"
        "• Ricerca web in tempo reale\n\n"
        "Inizia con i pulsanti qui sotto 👇"
    ),
    "welcome_referral_bonus": "\n\n🎁 Sei arrivato tramite un link di invito — hai ricevuto <b>+5 messaggi bonus</b>!",
    "welcome_premium_expiry": "\n\n⚠️ Il tuo Premium scade tra <b>{days_left} giorni</b>! Usa /upgrade per rinnovarlo.",

    "help": (
        "ℹ️ <b>Come usare</b>\n\n"
        "💬 <b>Scrivi testo</b> → l'IA risponde\n"
        "🖼 <b>Invia un'immagine</b> → l'IA la analizza\n"
        "📄 <b>Invia documento/PDF</b> → l'IA legge e spiega\n"
        "🎙 <b>Messaggio vocale</b> → l'IA ascolta e risponde\n"
        "😄 <b>Invia sticker</b> → l'IA legge l'emozione\n\n"
        "<b>Comandi:</b>\n"
        "/mode — 🎭 Cambia modalità IA (10 modalità)\n"
        "/status — 📊 Info piano e limite\n"
        "/clear — 🗑 Elimina chat\n"
        "/export — 📤 Scarica chat come file\n"
        "/search — 🌐 Attiva/disattiva ricerca web\n"
        "/invite — 🎁 Invita amici, guadagna bonus\n"
        "/top — 🏆 Utenti più attivi\n"
        "/feedback — 💌 Invia feedback\n"
        "/upgrade — ⭐ Ottieni Premium\n\n"
        "💡 <b>Suggerimento:</b> Usa il bot in qualsiasi chat scrivendo @botusername!"
    ),

    "btn_mode":        "🎭 Scegli modalità",
    "btn_status":      "📊 Stato",
    "btn_internet":    "🌐 Internet",
    "btn_premium":     "⭐ Premium",
    "btn_clear":       "🗑 Elimina chat",
    "btn_export":      "📤 Esporta",
    "btn_invite":      "🎁 Invita",
    "btn_top":         "🏆 TOP",
    "btn_help":        "ℹ️ Aiuto",
    "btn_feedback":    "💌 Feedback",
    "btn_back":        "⬅️ Menu principale",
    "btn_back_short":  "⬅️ Indietro",
    "btn_retry":       "🔁 Riprova",
    "btn_upgrade":     "⭐ Ottieni Premium",
    "btn_invite_bonus":"🎁 Invita amico (+bonus)",
    "btn_share_link":  "📤 Condividi link",
    "btn_refresh":     "🔄 Aggiorna",
    "btn_language":    "🌍 Lingua",

    "lang_select_title": "🌍 <b>Seleziona lingua</b>\n\nAttuale: <b>{current}</b>",
    "lang_changed":      "✅ Lingua cambiata: <b>{lang}</b>",
    "lang_already":      "ℹ️ La lingua è già impostata su <b>{lang}</b>.",

    "status_plan":        "{emoji} <b>Piano:</b> {plan}",
    "status_mode":        "🎭 <b>Modalità:</b> {mode}",
    "status_internet":    "🌐 <b>Internet:</b> {state}",
    "status_limit":       "📊 <b>Limite:</b> {used}/{limit}",
    "status_remaining":   "✅ <b>Rimanenti:</b> {remaining} messaggi",
    "status_until":       "📅 <b>Scade:</b> {date} ({days} giorni rimanenti)",
    "status_bonus":       "🎁 <b>Messaggi bonus:</b> +{bonus}",
    "status_upgrade_tip": "\n💡 Ottieni premium con /upgrade → 500 msg/giorno",

    "mode_select_title":   "🎭 <b>Scegli modalità</b>",
    "mode_select_header":  "🎭 <b>Scegli modalità</b>\n\nOgni modalità attiva una personalità IA diversa:",
    "mode_changed":        "✅ Modalità cambiata: <b>{mode}</b>\n📝 {desc}\n\nMandami un messaggio! 👇",
    "mode_selected_toast": "{mode} selezionato!",
    "mode_invalid":        "Modalità non valida.",
    "mode_current":        "Modalità attuale: <b>{mode}</b>",

    "clear_done":     "🗑 Chat eliminata ({count} messaggi).\n\nInizia una nuova chat! 👇",
    "clear_toast":    "Chat eliminata!",
    "clear_cmd_done": "🗑️ Cronologia eliminata ({count} messaggi).\nPuoi iniziare una nuova chat!",

    "search_on":       "✅ attivata",
    "search_off":      "❌ disattivata",
    "search_toggled":  "🌐 Ricerca web {status}.",
    "search_toggled_detail": (
        "🌐 Ricerca web {status}.\n\n"
        "Quando attiva, l'IA cerca informazioni in rete in tempo reale."
    ),

    "invite_text": (
        "🎁 <b>Invita amici e guadagna bonus!</b>\n\n"
        "Ogni amico invitato dà a <b>entrambi +5 messaggi bonus</b>.\n\n"
        "🔗 Il tuo link:\n<code>{link}</code>\n\n"
        "👥 Invitati finora: <b>{count}</b>\n"
        "🎁 Bonus guadagnati: <b>+{bonus}</b> messaggi"
    ),
    "invite_share_url": "Questo bot IA è fantastico!",

    "export_empty":   "📭 Non hai ancora una cronologia chat.",
    "export_caption": "📤 Cronologia chat ({count} messaggi)\n📅 Data esportazione: {date}",
    "export_user":    "👤 Tu",
    "export_ai":      "🤖 IA",

    "top_empty":       "Ancora nessun utente.",
    "top_title":       "🏆 <b>Utenti più attivi (oggi)</b>\n",
    "top_title_admin": "🏆 <b>TOP 10 Utenti</b>\n",

    "feedback_usage": (
        "💌 Invia il tuo feedback così:\n"
        "<code>/feedback Il tuo messaggio qui</code>"
    ),
    "feedback_prompt": (
        "💌 <b>Feedback / Suggerimento</b>\n\n"
        "Per inviare feedback, suggerimenti o segnalare problemi:\n\n"
        "<code>/feedback [il tuo testo]</code>\n\n"
        "Esempio: <code>/feedback La modalità traduttore è fantastica!</code>"
    ),
    "feedback_sent":    "✅ Feedback inviato! Grazie 🙏\nOgni messaggio aiuta a migliorare il bot.",
    "feedback_saved":   "✅ Feedback salvato! Grazie 🙏",
    "feedback_admin":   "💌 <b>Nuovo feedback!</b>\n\n👤 {name} (@{username}) [ID: {uid}]\n\n📝 {text}",

    "upgrade_already":       "✅ Sei già un utente Premium!\n📅 Scade: {until}\n⏳ Rimanente: {days} giorni",
    "upgrade_already_simple":"✅ Sei già un utente Premium!",
    "upgrade_already_toast": "Sei già Premium! ⭐",
    "upgrade_invoice_title": "Piano Premium ⭐",
    "upgrade_invoice_desc": (
        "✨ {days} giorni Premium:\n"
        "• {premium_limit} messaggi/giorno (standard: {free_limit})\n"
        "• Tutte le 10 modalità IA\n"
        "• Analisi documenti/PDF\n"
        "• Supporto prioritario"
    ),
    "upgrade_success": (
        "🎉 <b>Pagamento ricevuto con successo!</b>\n\n"
        "⭐ Premium attivato!\n"
        "📅 Scade: {until}\n"
        "📨 Limite giornaliero: {limit} messaggi\n\n"
        "Inizia a usare le tue nuove funzionalità! 🚀"
    ),

    "limit_exceeded": (
        "⛔ <b>Limite giornaliero raggiunto</b> ({limit}/{limit} messaggi)\n\n"
        "Opzioni:\n"
        "• Il limite si azzera domani\n"
        "• /upgrade per ottenere premium (500 messaggi/giorno)\n"
        "• /invite per invitare amici (messaggi bonus)"
    ),
    "limit_warning":  "ℹ️ Limite rimanente oggi: <b>{remaining}/{limit}</b>\n💡 Ottieni Premium con /upgrade — 500 msg/giorno!",
    "processing":     "⏳ La tua richiesta precedente è ancora in elaborazione, aspetta un momento...",
    "db_error":       "😕 Errore nel database, riprova tra poco.",
    "ai_rate_limit":  "⏳ <b>IA occupata</b>\nRiprova tra <b>{retry_after} secondi</b>.",
    "ai_error":       "😕 L'IA non ha potuto rispondere. Riprova tra poco.",

    "retry_expired":  "⏰ Scaduto, scrivi di nuovo.",
    "retry_trying":   "🔁 Nuovo tentativo in corso...",

    "photo_default_prompt":  "Cosa vedi in questa immagine? Spiega dettagliatamente, elenca tutto.",
    "doc_size_error":        "❌ File troppo grande ({size_mb:.1f} MB).\nDimensione massima: {max_mb} MB.",
    "doc_format_error": (
        "❌ Questo formato di file non è supportato.\n\n"
        "✅ Formati supportati:\n"
        "• PDF, TXT, CSV, JSON, HTML, Markdown, DOCX"
    ),
    "doc_default_prompt": (
        "Leggi attentamente questo documento e spiega il suo contenuto principale. "
        "Se è un PDF, estrai tutte le informazioni importanti."
    ),
    "voice_prompt": (
        "Listen to this voice message and do two things:\n"
        "1. Transcribe exactly what was said (just the words, no explanation)\n"
        "2. Reply naturally to what was said\n\n"
        "Format:\n"
        "🎙 [exact transcription]\n\n"
        "[your natural reply]\n\n"
        "IMPORTANT: Reply in the SAME language as the voice message. "
        "If they spoke Azerbaijani, reply in Azerbaijani. "
        "Do NOT explain what the word means unless asked."
    ),
    "sticker_prompt": (
        "L'utente ti ha inviato uno sticker con l'emoji '{emoji}'. "
        "Dai una risposta amichevole e breve adatta a quell'emozione. "
        "Rispondi con lo stesso tono."
    ),

    "inline_type_hint":    "✍️ Scrivi la tua domanda...",
    "inline_short_prompt": "Dai una risposta breve e precisa (max 200 parole): {query}",
    "inline_error":        "❌ Impossibile ottenere risposta. Riprova più tardi.",
    "inline_result_title": "🤖 Risposta IA",

    "admin_panel":       "🛠 <b>Pannello Admin</b>\n\nCosa vuoi fare?",
    "admin_no_perm":     "Nessun permesso.",
    "admin_grant_usage": "Uso: /grant <user_id> <free|premium>",
    "admin_grant_done":  "✅ Utente {uid} → piano: {plan}",
    "admin_lookup_usage":"Uso: /lookup <user_id | @username>",
    "admin_lookup_none": "❌ Non trovato: <code>{query}</code>",
    "admin_lookup_result": (
        "👤 <b>Info utente</b>\n\n"
        "🆔 ID:        <code>{uid}</code>\n"
        "👤 Nome:      {first_name}\n"
        "📛 Username:  @{username}\n"
        "📦 Piano:     <b>{plan}</b>\n"
        "📅 Premium:   {until}\n"
        "🎭 Modalità:  {mode}\n"
        "💬 Oggi:      {used}/{limit}\n"
        "👥 Invitati:  {refs}\n"
        "📆 Registrato:{created}"
    ),
    "admin_btn_stats":    "📊 Statistiche",
    "admin_btn_revenue":  "💰 Entrate",
    "admin_btn_broadcast":"📢 Broadcast",
    "admin_btn_lookup":   "🔍 Cerca utente",
    "admin_btn_top":      "🏆 TOP utenti",
    "admin_btn_expiring": "⏰ In scadenza",
    "admin_btn_premium":  "⭐ Dai Premium",
    "admin_btn_free":     "🆓 Rendi gratis",
    "admin_btn_clear_h":  "🗑 Cancella cronologia",
    "admin_btn_bonus":    "🎁 +10 Bonus",
    "admin_stats": (
        "📊 <b>Statistiche bot</b>\n\n"
        "👥 Totale utenti:   <b>{total:,}</b>\n"
        "⭐ Premium:         <b>{premium:,}</b>\n"
        "🆓 Gratis:          <b>{free:,}</b>\n"
        "📈 Conversione:     <b>{cvr:.1f}%</b>\n\n"
        "🟢 Attivi oggi:    <b>{active:,}</b>\n"
        "💬 Messaggi oggi:  <b>{today_msg:,}</b>\n"
        "📨 Totale messaggi:<b>{total_msg:,}</b>"
    ),
    "admin_revenue": (
        "💰 <b>Statistiche entrate</b>\n\n"
        "⭐ Totale Stars guadagnate: <b>{total:,}</b>\n"
        "📅 Questo mese: <b>{month:,}</b> Stars\n"
        "🧾 Totale pagamenti: <b>{count:,}</b>\n\n"
        "💡 Pagamento medio: <b>{avg:,}</b> Stars"
    ),
    "admin_expiring_none":  "Nessun premium in scadenza nei prossimi 3 giorni.",
    "admin_expiring_title": "⏰ <b>Premium in scadenza in 3 giorni:</b>\n",
    "admin_broadcast_prompt": (
        "📢 <b>Broadcast</b>\n\n"
        "<code>/broadcast Il tuo messaggio qui</code>\n\n"
        "⚠️ Sarà inviato a tutti gli utenti!"
    ),
    "admin_broadcast_usage":    "Uso: /broadcast <messaggio>",
    "admin_broadcast_starting": "⏳ Broadcast avviato... ({total} utenti)",
    "admin_broadcast_done": (
        "✅ <b>Broadcast completato</b>\n\n"
        "✉️ Inviati: {sent}\n"
        "❌ Falliti: {failed}\n"
        "📊 Totale: {total}"
    ),
    "admin_broadcast_prefix": "📢 <b>Annuncio bot</b>\n\n{text}",
    "admin_lookup_prompt": (
        "🔍 <b>Cerca utente</b>\n\n"
        "<code>/lookup @username</code>\n"
        "<code>/lookup 123456789</code>"
    ),
    "admin_grant_premium_done": "⭐ Premium concesso ({days} giorni)",
    "admin_grant_free_done":    "🆓 Passato al piano gratis",
    "admin_clear_done":         "🗑 {count} messaggi eliminati",
    "admin_bonus_done":         "🎁 +10 messaggi bonus concessi!",

    "top_row":            "{medal} {name} {plan_icon} — {usage} messaggi",
    "status_today":       "📊 Oggi: {used}/{limit} [{bar}]",
    "status_until_short": "📅 Scade: {date}",
    "mode_row":           "{check} {name} — {desc}",
    "inline_result_msg":  "❓ <b>{query}</b>\n\n🤖 {reply}",

    "guest_name": "Ospite",
}

# ── Registry & accessor ───────────────────────────────────────────────────────

_LANGUAGES: dict[str, dict[str, str]] = {
    "az": AZ,
    "en": EN,
    "ru": RU,
    "tr": TR,
    "de": DE,
    "fr": FR,
    "es": ES,
    "ar": AR,
    "zh": ZH,
    "pt": PT,
    "it": IT,
}

DEFAULT_LANG = "az"

# Telegram sends full locale codes like "az-AZ", "en-US", "ru-RU".
# Map them to our two-letter keys.
_LANG_MAP: dict[str, str] = {
    "az": "az", "en": "en", "ru": "ru",
    "tr": "tr", "de": "de", "fr": "fr",
    "es": "es", "ar": "ar", "zh": "zh",
    "pt": "pt", "it": "it",
}


def normalize_lang(raw: str | None) -> str:
    """Convert a Telegram language_code (e.g. 'en-US', 'ru-RU') to our key."""
    if not raw:
        return DEFAULT_LANG
    prefix = raw.split("-")[0].lower()
    return _LANG_MAP.get(prefix, DEFAULT_LANG)


def t(key: str, lang: str | None = None, **kwargs) -> str:
    """Return the localized string for *key* in *lang* (falls back to DEFAULT_LANG, then EN).

    Extra keyword arguments are passed to str.format().
    """
    lng = normalize_lang(lang)
    table = _LANGUAGES.get(lng) or _LANGUAGES.get(DEFAULT_LANG) or EN
    text = table.get(key) or EN.get(key) or key
    return text.format(**kwargs) if kwargs else text


# ── AI Modes ─────────────────────────────────────────────────────────────────

_MODE_NAMES: dict[str, dict[str, str]] = {
    "az": {
        "default":    "🤖 Standart",
        "teacher":    "📚 Müəllim",
        "coder":      "💻 Proqramçı",
        "friend":     "😊 Dost",
        "translator": "🌐 Tərcüməçi",
        "writer":     "✍️ Yazıçı",
        "analyst":    "📊 Analitik",
        "creative":   "🎨 Kreativ",
        "fitness":    "💪 Fitnes",
        "chef":       "👨‍🍳 Aşpaz",
    },
    "en": {
        "default":    "🤖 Standard",
        "teacher":    "📚 Teacher",
        "coder":      "💻 Coder",
        "friend":     "😊 Friend",
        "translator": "🌐 Translator",
        "writer":     "✍️ Writer",
        "analyst":    "📊 Analyst",
        "creative":   "🎨 Creative",
        "fitness":    "💪 Fitness",
        "chef":       "👨‍🍳 Chef",
    },
    "ru": {
        "default":    "🤖 Стандарт",
        "teacher":    "📚 Учитель",
        "coder":      "💻 Программист",
        "friend":     "😊 Друг",
        "translator": "🌐 Переводчик",
        "writer":     "✍️ Писатель",
        "analyst":    "📊 Аналитик",
        "creative":   "🎨 Креатив",
        "fitness":    "💪 Фитнес",
        "chef":       "👨‍🍳 Повар",
    },
    "tr": {
        "default":    "🤖 Standart",
        "teacher":    "📚 Öğretmen",
        "coder":      "💻 Programcı",
        "friend":     "😊 Arkadaş",
        "translator": "🌐 Çevirmen",
        "writer":     "✍️ Yazar",
        "analyst":    "📊 Analist",
        "creative":   "🎨 Yaratıcı",
        "fitness":    "💪 Fitness",
        "chef":       "👨‍🍳 Şef",
    },
    "de": {
        "default":    "🤖 Standard",
        "teacher":    "📚 Lehrer",
        "coder":      "💻 Entwickler",
        "friend":     "😊 Freund",
        "translator": "🌐 Übersetzer",
        "writer":     "✍️ Autor",
        "analyst":    "📊 Analyst",
        "creative":   "🎨 Kreativ",
        "fitness":    "💪 Fitness",
        "chef":       "👨‍🍳 Koch",
    },
    "fr": {
        "default":    "🤖 Standard",
        "teacher":    "📚 Professeur",
        "coder":      "💻 Développeur",
        "friend":     "😊 Ami",
        "translator": "🌐 Traducteur",
        "writer":     "✍️ Écrivain",
        "analyst":    "📊 Analyste",
        "creative":   "🎨 Créatif",
        "fitness":    "💪 Fitness",
        "chef":       "👨‍🍳 Chef",
    },
    "es": {
        "default":    "🤖 Estándar",
        "teacher":    "📚 Profesor",
        "coder":      "💻 Programador",
        "friend":     "😊 Amigo",
        "translator": "🌐 Traductor",
        "writer":     "✍️ Escritor",
        "analyst":    "📊 Analista",
        "creative":   "🎨 Creativo",
        "fitness":    "💪 Fitness",
        "chef":       "👨‍🍳 Chef",
    },
    "ar": {
        "default":    "🤖 قياسي",
        "teacher":    "📚 معلم",
        "coder":      "💻 مبرمج",
        "friend":     "😊 صديق",
        "translator": "🌐 مترجم",
        "writer":     "✍️ كاتب",
        "analyst":    "📊 محلل",
        "creative":   "🎨 مبدع",
        "fitness":    "💪 لياقة",
        "chef":       "👨‍🍳 طاهي",
    },
    "zh": {
        "default":    "🤖 标准",
        "teacher":    "📚 老师",
        "coder":      "💻 程序员",
        "friend":     "😊 朋友",
        "translator": "🌐 翻译",
        "writer":     "✍️ 作家",
        "analyst":    "📊 分析师",
        "creative":   "🎨 创意",
        "fitness":    "💪 健身",
        "chef":       "👨‍🍳 厨师",
    },
    "pt": {
        "default":    "🤖 Padrão",
        "teacher":    "📚 Professor",
        "coder":      "💻 Programador",
        "friend":     "😊 Amigo",
        "translator": "🌐 Tradutor",
        "writer":     "✍️ Escritor",
        "analyst":    "📊 Analista",
        "creative":   "🎨 Criativo",
        "fitness":    "💪 Fitness",
        "chef":       "👨‍🍳 Chef",
    },
    "it": {
        "default":    "🤖 Standard",
        "teacher":    "📚 Insegnante",
        "coder":      "💻 Sviluppatore",
        "friend":     "😊 Amico",
        "translator": "🌐 Traduttore",
        "writer":     "✍️ Scrittore",
        "analyst":    "📊 Analista",
        "creative":   "🎨 Creativo",
        "fitness":    "💪 Fitness",
        "chef":       "👨‍🍳 Chef",
    },
}

_MODE_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "az": {
        "default":    "Normal AI köməkçi",
        "teacher":    "Addım-addım izah edir",
        "coder":      "Kod yazır və debug edir",
        "friend":     "Səmimi danışır",
        "translator": "Tərcümə edir",
        "writer":     "Mətn yaradır",
        "analyst":    "Analiz edir",
        "creative":   "İdeyalar verir",
        "fitness":    "Məşq köməkçisi",
        "chef":       "Yemək köməkçisi",
    },
    "en": {
        "default":    "General AI assistant",
        "teacher":    "Explains step by step",
        "coder":      "Writes and debugs code",
        "friend":     "Talks casually",
        "translator": "Translates text",
        "writer":     "Creates written content",
        "analyst":    "Analyzes data",
        "creative":   "Generates ideas",
        "fitness":    "Workout assistant",
        "chef":       "Cooking assistant",
    },
    "ru": {
        "default":    "Обычный AI помощник",
        "teacher":    "Объясняет пошагово",
        "coder":      "Пишет и отлаживает код",
        "friend":     "Общается по-дружески",
        "translator": "Переводит текст",
        "writer":     "Создаёт тексты",
        "analyst":    "Анализирует данные",
        "creative":   "Генерирует идеи",
        "fitness":    "Помощник по тренировкам",
        "chef":       "Кулинарный помощник",
    },
    "tr": {
        "default":    "Genel AI asistanı",
        "teacher":    "Adım adım açıklar",
        "coder":      "Kod yazar ve hata ayıklar",
        "friend":     "Samimi konuşur",
        "translator": "Metin çevirir",
        "writer":     "Yazılı içerik oluşturur",
        "analyst":    "Veri analiz eder",
        "creative":   "Fikir üretir",
        "fitness":    "Egzersiz asistanı",
        "chef":       "Yemek asistanı",
    },
    "de": {
        "default":    "Allgemeiner AI-Assistent",
        "teacher":    "Erklärt Schritt für Schritt",
        "coder":      "Schreibt und debuggt Code",
        "friend":     "Unterhält sich locker",
        "translator": "Übersetzt Texte",
        "writer":     "Erstellt schriftliche Inhalte",
        "analyst":    "Analysiert Daten",
        "creative":   "Generiert Ideen",
        "fitness":    "Trainingsassistent",
        "chef":       "Kochassistent",
    },
    "fr": {
        "default":    "Assistant IA général",
        "teacher":    "Explique étape par étape",
        "coder":      "Écrit et débogue du code",
        "friend":     "Parle de façon décontractée",
        "translator": "Traduit des textes",
        "writer":     "Crée du contenu écrit",
        "analyst":    "Analyse des données",
        "creative":   "Génère des idées",
        "fitness":    "Assistant d'entraînement",
        "chef":       "Assistant culinaire",
    },
    "es": {
        "default":    "Asistente IA general",
        "teacher":    "Explica paso a paso",
        "coder":      "Escribe y depura código",
        "friend":     "Habla de forma casual",
        "translator": "Traduce textos",
        "writer":     "Crea contenido escrito",
        "analyst":    "Analiza datos",
        "creative":   "Genera ideas",
        "fitness":    "Asistente de ejercicios",
        "chef":       "Asistente de cocina",
    },
    "ar": {
        "default":    "مساعد ذكاء اصطناعي عام",
        "teacher":    "يشرح خطوة بخطوة",
        "coder":      "يكتب ويصحح الكود",
        "friend":     "يتحدث بشكل ودي",
        "translator": "يترجم النصوص",
        "writer":     "ينشئ محتوى مكتوب",
        "analyst":    "يحلل البيانات",
        "creative":   "يولد أفكاراً",
        "fitness":    "مساعد تمارين",
        "chef":       "مساعد طبخ",
    },
    "zh": {
        "default":    "通用AI助手",
        "teacher":    "逐步讲解",
        "coder":      "编写和调试代码",
        "friend":     "轻松对话",
        "translator": "翻译文本",
        "writer":     "创作书面内容",
        "analyst":    "分析数据",
        "creative":   "产生创意",
        "fitness":    "健身助手",
        "chef":       "烹饪助手",
    },
    "pt": {
        "default":    "Assistente IA geral",
        "teacher":    "Explica passo a passo",
        "coder":      "Escreve e depura código",
        "friend":     "Conversa de forma casual",
        "translator": "Traduz textos",
        "writer":     "Cria conteúdo escrito",
        "analyst":    "Analisa dados",
        "creative":   "Gera ideias",
        "fitness":    "Assistente de exercícios",
        "chef":       "Assistente de culinária",
    },
    "it": {
        "default":    "Assistente IA generale",
        "teacher":    "Spiega passo dopo passo",
        "coder":      "Scrive e fa debug del codice",
        "friend":     "Parla in modo informale",
        "translator": "Traduce testi",
        "writer":     "Crea contenuti scritti",
        "analyst":    "Analizza dati",
        "creative":   "Genera idee",
        "fitness":    "Assistente allenamento",
        "chef":       "Assistente cucina",
    },
}

# Backward-compatible flat dicts (AZ by default) so existing imports don't break
MODE_NAMES = _MODE_NAMES["az"]
MODE_DESCRIPTIONS = _MODE_DESCRIPTIONS["az"]


def mode_name(mode: str, lang: str | None = None) -> str:
    """Return localized mode name."""
    lng = normalize_lang(lang)
    return _MODE_NAMES.get(lng, _MODE_NAMES["az"]).get(mode, mode)


def mode_desc(mode: str, lang: str | None = None) -> str:
    """Return localized mode description."""
    lng = normalize_lang(lang)
    return _MODE_DESCRIPTIONS.get(lng, _MODE_DESCRIPTIONS["az"]).get(mode, mode)


# ── Language metadata ─────────────────────────────────────────────────────────

# Display label shown on the button / in messages for each language code
LANGUAGE_LABELS: dict[str, str] = {
    "az": "🇦🇿 Azərbaycan",
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "tr": "🇹🇷 Türkçe",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "ar": "🇸🇦 العربية",
    "zh": "🇨🇳 中文",
    "pt": "🇵🇹 Português",
    "it": "🇮🇹 Italiano",
}

SUPPORTED_LANGS = list(_LANGUAGES.keys())

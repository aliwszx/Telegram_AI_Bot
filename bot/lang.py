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

# ── Registry & accessor ───────────────────────────────────────────────────────

_LANGUAGES: dict[str, dict[str, str]] = {
    "az": AZ,
    "en": EN,
    "ru": RU,
}

DEFAULT_LANG = "az"

# Telegram sends full locale codes like "az-AZ", "en-US", "ru-RU".
# Map them to our two-letter keys.
_LANG_MAP: dict[str, str] = {
    "az": "az", "en": "en", "ru": "ru",
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
}

SUPPORTED_LANGS = list(_LANGUAGES.keys())

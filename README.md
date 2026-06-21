# Telegram AI Chat Bot (Gemini + Supabase + Render)

Production-ready Telegram AI chat bot. Gemini ilə söhbət edir, istifadəçi
məlumatı və mesaj tarixçəsini Supabase-də saxlayır, günlük limit (free/premium)
sistemi var, Render-də 24/7 işləyə bilir.

## Folder structure

```
telegram-ai-bot/
├── bot/
│   ├── __init__.py
│   ├── config.py        # .env-dən bütün config oxunur
│   ├── ai.py             # Gemini API wrapper
│   ├── db.py              # Supabase: users, messages, rate limit
│   ├── handlers.py        # /start, /help, /status, /grant, AI chat
│   └── middlewares.py     # sadə anti-flood middleware
├── supabase/
│   └── schema.sql          # users + messages cədvəlləri
├── main.py                  # polling entrypoint (tövsiyə olunur)
├── main_webhook.py          # webhook entrypoint (alternativ)
├── requirements.txt
├── render.yaml               # Render Background Worker blueprint
├── .env.example
└── .gitignore
```

## 1. Tələblər

- Python 3.11+
- Telegram bot token ([@BotFather](https://t.me/BotFather)-dan)
- Google Gemini API key ([Google AI Studio](https://aistudio.google.com/apikey))
- Supabase layihəsi ([supabase.com](https://supabase.com))

## 2. Supabase qurulumu

1. [supabase.com](https://supabase.com) → New project yarat.
2. Sol menyudan **SQL Editor** → New query.
3. `supabase/schema.sql` faylının içindəkiləri kopyala, yapıştır, **Run**.
   Bu, `users` və `messages` cədvəllərini yaradacaq.
4. **Project Settings → API** bölməsindən götür:
   - `Project URL` → `.env`-də `SUPABASE_URL`
   - `service_role` key (anon deyil!) → `.env`-də `SUPABASE_KEY`

   ⚠️ `service_role` key-i yalnız backend-də (bot serverində) saxla, heç vaxt
   client/frontend kodunda istifadə etmə — bütün RLS-i bypass edir.

### Schema (qısaca)

**users**
| sütun | tip | qeyd |
|---|---|---|
| id | bigint, PK | Telegram user_id |
| username | text | |
| first_name | text | |
| plan | text | `free` / `premium`, default `free` |
| daily_usage | integer | günlük göndərilən mesaj sayı |
| last_usage_date | date | sayğacın sıfırlandığı son tarix |
| created_at | timestamptz | |

**messages**
| sütun | tip | qeyd |
|---|---|---|
| id | uuid, PK | |
| user_id | bigint, FK → users.id | |
| role | text | `user` / `assistant` |
| content | text | mesajın özü |
| created_at | timestamptz | tarixçə sıralaması üçün |

## 3. Lokal işə salma

```bash
git clone <your-repo-url>
cd telegram-ai-bot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# .env faylını aç və BOT_TOKEN, GEMINI_API_KEY, SUPABASE_URL, SUPABASE_KEY-i doldur

python main.py
```

Bot indi polling rejimində işləyəcək — Telegram-da botuna `/start` yaz.

## 4. Konfiqurasiya (.env)

| Dəyişən | Açıqlama | Default |
|---|---|---|
| `BOT_TOKEN` | BotFather-dan aldığın token | — (məcburi) |
| `GEMINI_API_KEY` | Google AI Studio key | — (məcburi) |
| `GEMINI_MODEL` | İstifadə olunan model | `gemini-3.1-flash-lite` |
| `GEMINI_SYSTEM_PROMPT` | AI-ın "şəxsiyyəti" | qısa default mesaj |
| `SUPABASE_URL` | Layihə URL-i | — (məcburi) |
| `SUPABASE_KEY` | service_role key | — (məcburi) |
| `HISTORY_LIMIT` | Gemini-yə göndərilən son neçə mesaj | `10` |
| `FREE_DAILY_LIMIT` | Free user üçün günlük mesaj limiti | `20` |
| `PREMIUM_DAILY_LIMIT` | Premium user üçün günlük limit | `300` |
| `ADMIN_IDS` | `/grant` komandasını işlədə bilən Telegram ID-lər, vergüllə ayrılmış | boş |

## 5. Monetizasiya — Telegram Stars ilə premium

İstifadəçi `/upgrade` yazanda bot Telegram Stars (`XTR`) invoice-u göndərir.
Stars üçün bank/kart provayderi, müqavilə, KYC və s. lazım deyil — Telegram
özü ödənişi idarə edir və hər ölkədə (Azərbaycan daxil) işləyir.

**Necə işləyir:**
1. `/upgrade` → bot `send_invoice(currency="XTR", ...)` göndərir.
2. İstifadəçi Telegram-da Stars ilə ödəyir (Stars-ı yoxdursa, Telegram ona
   almaq imkanı göstərir).
3. Telegram `pre_checkout_query` göndərir → bot avtomatik təsdiqləyir.
4. Ödəniş uğurlu olanda `successful_payment` mesajı gəlir → bot
   `db.activate_premium()` çağırır, istifadəçinin planı `premium` olur,
   `premium_until = indi + PREMIUM_DURATION_DAYS` təyin olunur.
5. `premium_until` keçəndə bot avtomatik olaraq istifadəçini yenidən `free`
   plana qaytarır (`bot/db.py` → `effective_plan()`), heç bir cron lazım deyil.

**Qiyməti dəyişmək:** `.env`-də `STARS_PRICE` (Stars sayı) və
`PREMIUM_DURATION_DAYS` (neçə gün davam etsin) dəyərlərini dəyiş, Render-də
Manual Deploy et.

**Qeyd:** Stars-dan Telegram öz komissiyasını çıxır, qalanını sənə ödəyir
(real pulla çıxarmaq üçün BotFather → Stars balansı → Withdraw). Əgər real
bank kartı ilə ödəniş (Stripe, Click, Payme) istəsən, bu da `send_invoice`-a
fərqli `provider_token` və `currency` verməklə əlavə oluna bilər — sonra
quraşdırmaq istəsən mənə de.

**Admin əl ilə təyinat:** `/grant <user_id> <free|premium>` hələ də qalır —
manual qrant `premium_until`-ı `null` saxlayır, ona görə avtomatik bitmir
(yalnız sən özün `/grant ... free` ilə geri qaytara bilərsən).

## 5.1. Dil problemi (məs. "salam" yazanda Özbəkcə cavab gəlir)

Bot universal işləyir — istifadəçi hansı dildə yazırsa, həmin dildə cavab
verir (Gemini özü dili aşkarlayır). Problem yalnız çox qısa/oxşar mesajlarda
yaranır: "salam" kimi sözlər Azərbaycan, Özbək, Türk dillərində demək olar ki
eynidir, ona görə model bəzən səhv təxmin edə bilir.

Bunun qarşısını almaq üçün bot hər sorğuda istifadəçinin **Telegram tətbiq
dilini** (`message.from_user.language_code`, məs. `az`, `uz`, `tr`, `en`) Gemini-yə
əlavə ipucu kimi göndərir (`bot/ai.py` → `generate_reply(..., language_hint=...)`).
Bu ipucu yalnız qısa/qeyri-müəyyən mesajlarda tie-breaker kimi işləyir —
istifadəçi aydın şəkildə başqa dildə yazırsa, model həmin dili üstün tutur.

Qeyd: bu, istifadəçinin Telegram tətbiqində seçdiyi dilə əsaslanır (Settings
→ Language), real coğrafi məkana yox. Əgər istifadəçi Telegram-ı, məsələn,
İngilis dilində istifadə edirsə, ipucu da "en" olacaq.

## 6. GitHub-a yükləmə

```bash
git init
git add .
git commit -m "Initial commit: Telegram AI bot"
git branch -M main
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

`.env` faylı `.gitignore`-dadır — heç vaxt repo-ya push etmə, secret-lərini
itirmiş olarsan.

## 7. Render-də deploy (24/7)

İki seçim var: **polling** (tövsiyə olunur, sadədir) və **webhook**.

> ⚠️ **Vacib:** Render-in default Python versiyası çox yeni ola bilər (məs.
> 3.14), bu da `pydantic-core` kimi C/Rust əsaslı paketlərin build xətası ilə
> uğursuz olmasına səbəb olur (mənbədən compile etməyə çalışır, Render-in
> read-only fayl sistemi buna icazə vermir). Bunun qarşısını almaq üçün repo-da
> `.python-version` faylı `3.11.9` ilə əlavə olunub. Əgər Render Dashboard-dan
> **manual** (blueprint olmadan) Web Service/Background Worker yaradırsansa,
> Environment bölməsinə əlavə olaraq bunu da əlavə et:
>
> ```
> PYTHON_VERSION=3.11.9
> ```
>
> `render.yaml` blueprint-i istifadə etsən, bu artıq avtomatik təyin olunub.

### A) Polling — Background Worker (tövsiyə olunur)

Polling-də bot Telegram-a özü qoşulub davamlı sorğu göndərir, ona görə açıq
porta ehtiyac yoxdur — Render-in "Web Service" health-check tələbi ilə
toqquşmur.

1. Render Dashboard → **New → Background Worker**.
2. GitHub repo-nu qoş.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python main.py`
5. **Environment** bölməsində `.env.example`-dəki bütün dəyişənləri əlavə et
   (`BOT_TOKEN`, `GEMINI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, və s.)
6. Deploy et. Loglardan `Starting bot in polling mode...` görünməlidir.

İstəsən `render.yaml` faylındakı blueprint-i də birbaşa istifadə edə bilərsən
(Render Dashboard → New → Blueprint → repo seç).

### B) Webhook — Web Service (alternativ)

Webhook rejimində Telegram mesajları birbaşa sənin serverinə HTTP POST kimi
göndərir, ona görə server açıq port saxlamalıdır (Render Web Service buna
uyğundur, üstəlik free/starter planlarda "sleep" probleminə də daha az
məruz qalır).

1. Render Dashboard → **New → Web Service**.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `python main_webhook.py`
4. Environment-ə əlavə et: yuxarıdakılardan başqa, `WEBHOOK_BASE_URL`
   (Render-in sənə verdiyi public URL, məs: `https://telegram-ai-bot.onrender.com`)
5. Deploy. `main_webhook.py` startup-da `bot.set_webhook(...)` çağıraraq
   Telegram-a webhook URL-ni özü qeydiyyatdan keçirir.

> Polling sadəliyinə görə kiçik/orta həcmli botlar üçün adətən kifayətdir.
> Yüksək trafikdə və ya çoxlu instance scale etmək istəsən webhook daha
> effektivdir.

## 8. Genişləndirmə ideyaları

- `/grant` əvəzinə real ödəniş inteqrasiyası (Stripe/Click/Payme webhook → `db.set_plan`)
- Inline keyboard ilə plan seçimi, FAQ, dil seçimi
- Multi-language (i18n) dəstəyi
- Redis əsaslı flood control (çoxlu instance üçün)
- Gemini function calling / tool use ilə əlavə bacarıqlar (hava, axtarış və s.)
- Admin paneli (Supabase + sadə dashboard) — istifadəçi statistikası üçün

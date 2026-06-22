# 🤖 Telegram AI Bot PRO

Gemini AI ilə işləyən tam professional Telegram botu.

---

## ✨ Yeni Funksiyalar (PRO versiya)

### 🎭 10 AI Rejimi
| Rejim | Açıqlama |
|-------|----------|
| 🤖 Standart | Ümumi köməkçi |
| 📚 Müəllim | Addım-addım izahat |
| 💻 Proqramçı | Kod və texnologiya |
| 😊 Dost | Mehriban söhbət |
| 🌐 Tərcüməçi | Dil tərcüməsi |
| ⚖️ Hüquqçu | Hüquqi məsləhət |
| 🏥 Həkim | Tibbi məlumat |
| 🧠 Psixoloq | Psixoloji dəstək |
| 👨‍🍳 Aşpaz | Resept və kulinariya |
| 💪 Fitnes | İdman və sağlamlıq |

### 📎 Media Dəstəyi
- 🖼 **Şəkil analizi** — Gemini Vision ilə
- 📄 **PDF / sənəd oxuma** — PDF, TXT, DOCX, CSV, JSON
- 🎙 **Səsli mesaj** — Audio transcription + cavab
- 😄 **Stiker** — Emosiya analizi

### 🌐 Real-time İnternet Axtarışı
- Google Search inteqrasiyası (Gemini built-in)
- `/search` ilə aç/bağla
- Hər istifadəçi üçün ayrıca ayar

### 💬 Inline Mode
- Hər hansı chatda `@botusername sual` yazaraq istifadə et
- Qrup söhbətlərində AI köməyi

### 🎁 Referral Sistemi
- `/invite` ilə dost dəvət et
- Hər dəvət: **+5 bonus mesaj** (sənə + dostuna)
- `/invite` ilə statistika gör

### 💰 Revenue Tracking
- Bütün ödənişlər loglanır
- Admin paneldə aylıq/total gəlir statistikası
- Stars ilə ödəniş

### ⏰ Premium Expiry Warnings
- Bitmədən **3 gün əvvəl** avtomatik xəbərdarlıq
- Hər 12 saatda bir yoxlanır

### 📊 Admin Panel (`/admin`)
- 📈 Statistika (users, premium, active, messages)
- 💰 Gəlir hesabatı
- 🏆 TOP 10 aktiv istifadəçi
- ⏰ Premium-u bitən istifadəçilər
- 📢 Broadcast (bütün istifadəçilərə mesaj)
- 🔍 User axtarış + plan idarəsi

### 🚀 Performance
- **Tək model**: gemini-3.1-flash-lite (fallback yoxdur)
- **Streaming**: Real-time cavab göstərilməsi
- **Redis cache**: Opsional sürətlənmə
- **PostgreSQL RPC**: Hər AI mesajı üçün 1 DB sorğusu (3 əvəzinə)

### 💌 Feedback Sistemi
- `/feedback` ilə rəy/təklif göndər
- Admin-lərə avtomatik forwarding

---

## 🛠 Quraşdırma

### 1. Supabase
```sql
-- Supabase SQL Editor-də icra et:
supabase/schema.sql
```

### 2. Mühit dəyişənləri
```bash
cp .env.example .env
# .env faylını redaktə et
```

### 3. Asılılıqları quraşdır
```bash
pip install -r requirements.txt
```

### 4. Başlat

**Polling (lokal test üçün):**
```bash
python main.py
```

**Webhook (Render/Railway üçün):**
```bash
python main_webhook.py
```

---

## 📁 Layihə strukturu

```
├── bot/
│   ├── __init__.py
│   ├── ai.py          # Gemini AI wrapper (10 rejim, streaming)
│   ├── cache.py       # Redis cache (opsional)
│   ├── config.py      # Bütün ayarlar
│   ├── db.py          # Supabase DB qatı
│   ├── handlers.py    # Bütün Telegram handlerlər
│   ├── retry.py       # Retry dekorator
│   └── scheduler.py   # Arxa plan tapşırıqları
├── supabase/
│   └── schema.sql     # DB strukturu + RPC
├── main.py            # Polling başlatma
├── main_webhook.py    # Webhook başlatma
├── requirements.txt
└── .env.example
```

---

## 🔧 Əsas Komandalar

| Komanda | Açıqlama |
|---------|----------|
| `/start` | Başla / Əsas menyu |
| `/help` | Kömək |
| `/mode` | AI rejimini dəyiş |
| `/status` | Plan və limit məlumatı |
| `/clear` | Söhbəti sil |
| `/export` | Söhbəti fayl kimi yüklə |
| `/search` | İnternet axtarışını aç/bağla |
| `/invite` | Dost dəvət et |
| `/top` | Ən aktiv istifadəçilər |
| `/feedback` | Rəy/təklif göndər |
| `/upgrade` | Premium al |
| `/admin` | Admin panel (yalnız adminlər) |
| `/broadcast` | Bütün istifadəçilərə mesaj |
| `/lookup` | User məlumatı |
| `/grant` | Plani dəyiş |

---

## 🌐 Render Deployment

1. Yeni **Web Service** yarat
2. Build command: `pip install -r requirements.txt`
3. Start command: `python main_webhook.py`
4. Mühit dəyişənlərini əlavə et (`.env.example`-a bax)
5. `WEBHOOK_BASE_URL` = Render URL-in

---

## 📄 Lisenziya
MIT

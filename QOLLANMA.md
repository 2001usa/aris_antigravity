# 📖 ARIS Bot - Batafsil Qo'llanma

## 📑 Mundarija

1. [Kirish](#kirish)
2. [O'rnatish](#ornatish)
3. [Sozlash](#sozlash)
4. [Foydalanish](#foydalanish)
5. [Admin Panel](#admin-panel)
6. [Deployment](#deployment)
7. [Muammolarni Hal Qilish](#muammolarni-hal-qilish)

---

## 1. Kirish

ARIS - bu Telegram orqali ishlaydigan shaxsiy moliyaviy yordamchi bot. U sizning kirim va chiqimlaringizni kuzatib boradi, statistika tayyorlaydi va maqsadlaringizga erishishda yordam beradi.

### Asosiy Imkoniyatlar

- 🎤 **Ovozli Tahlil** - Ovozli xabarlarni matnга o'girish va tahlil qilish
- 📊 **Statistika** - Kirim, chiqim va balansni ko'rish
- 🎯 **Maqsadlar** - Moliyaviy maqsadlar qo'yish va kuzatish
- 📝 **Kundalik** - Kundalik yozuvlar va AI tahlili (Premium)
- 📈 **Hisobotlar** - Haftalik va oylik hisobotlar
- 📥 **Export** - Excel va PDF formatda export

---

## 2. O'rnatish

### 2.1. Talablar

- **Python**: 3.11 yoki yuqori
- **OS**: Windows, Linux, macOS
- **Internet**: API'lar uchun

### 2.2. Loyihani Yuklab Olish

#### GitHub'dan:
```bash
git clone https://github.com/YOUR_USERNAME/aris-finance-bot.git
cd aris-finance-bot
```

#### ZIP fayl:
1. Loyihani yuklab oling
2. Arxivdan chiqaring
3. Papkaga o'ting

### 2.3. Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2.4. Kutubxonalar

```bash
pip install -r requirements.txt
```

**O'rnatilayotgan kutubxonalar:**
- aiogram 3.15.0 - Telegram bot framework
- groq 1.0.0+ - AI xizmati
- google-generativeai 0.8.3 - Gemini AI
- aiosqlite 0.20.0 - Asinxron SQLite
- openpyxl 3.1.5 - Excel export
- reportlab 4.2.2 - PDF export
- matplotlib 3.9.3 - Grafiklar
- pillow 11.0.0 - Rasmlar

---

## 3. Sozlash

### 3.1. API Kalitlarni Olish

#### Telegram Bot Token

1. [@BotFather](https://t.me/BotFather) ga `/start` yuboring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: "ARIS Finance Bot")
4. Bot username kiriting (masalan: "aris_finance_bot")
5. Token oling va saqlang

#### Groq API Keys (2 ta)

1. [console.groq.com](https://console.groq.com) ga kiring
2. "API Keys" bo'limiga o'ting
3. "Create API Key" tugmasini bosing
4. Nom bering va saqlang
5. Ikkinchi kalit uchun takrorlang

#### Gemini API Key

1. [ai.google.dev](https://ai.google.dev) ga kiring
2. "Get API Key" tugmasini bosing
3. Loyiha yarating
4. API kalitni oling va saqlang

### 3.2. .env Fayl

Loyiha papkasida `.env` fayl yarating:

```env
# Telegram Bot
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Groq API Keys (2 ta - fallback uchun)
GROQ_API_KEY_1=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY_2=gsk_yyyyyyyyyyyyyyyyyyyyyyyy

# Google Gemini API
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

# Database
DATABASE_PATH=database/aris.db
```

### 3.3. Admin Qo'shish

#### User ID ni Topish

1. [@userinfobot](https://t.me/userinfobot) ga `/start` yuboring
2. Sizning user ID ni ko'rsatadi (masalan: 123456789)

#### config.py da Qo'shish

`config.py` faylini oching va `ADMIN_USERS` ro'yxatiga qo'shing:

```python
ADMIN_USERS = [
    123456789,  # Sizning user ID
    987654321,  # Boshqa admin (ixtiyoriy)
]
```

### 3.4. Limitlarni Sozlash

#### Test Rejimi (Limitlar O'chirilgan)

```python
# config.py
ENABLE_LIMITS = False  # Barcha funksiyalar cheksiz
```

#### Ishlab Chiqarish Rejimi

```python
# config.py
ENABLE_LIMITS = True  # Limitlar yoqilgan

SUBSCRIPTION_LIMITS = {
    SubscriptionTier.STANDARD: 1890000,   # 1.89M token/oy
    SubscriptionTier.PREMIUM: 2400000,    # 2.4M token/oy
}
```

---

## 4. Foydalanish

### 4.1. Botni Ishga Tushirish

```bash
# Virtual environment aktivlashtirilgan bo'lishi kerak
python bot.py
```

**Muvaffaqiyatli ishga tushsa:**
```
INFO:aiogram:Bot started
INFO:aiogram:Polling started
```

### 4.2. Botdan Foydalanish

#### Boshlash

1. Telegram'da botni toping
2. `/start` buyrug'ini yuboring
3. Tarif avtomatik belgilanadi:
   - Admin → Premium
   - Oddiy user → Standart

#### Tranzaksiya Qo'shish

**Ovozli xabar:**
```
🎤 "Bugun 50 ming so'm non oldim"
```

Bot javob beradi:
```
✅ Tranzaksiya qo'shildi!

Turi: Chiqim
Summa: 50,000 so'm
Kategoriya: Oziq-ovqat
```

**Matn xabar:**
```
1 million so'm maosh oldim
```

#### Statistika Ko'rish

1. "📊 Statistika" tugmasini bosing
2. Kirim, chiqim va balansni ko'ring

#### Maqsad Qo'yish

1. "🎯 Maqsadlar" tugmasini bosing
2. "➕ Yangi maqsad" ni tanlang
3. Maqsad nomini kiriting
4. Maqsad summasini kiriting

#### Hisobot Olish

1. "📈 Hisobotlar" tugmasini bosing
2. Haftalik yoki oylik tanlang
3. Export uchun "📥 Export" ni bosing
4. Excel yoki PDF tanlang

---

## 5. Admin Panel

### 5.1. Admin Buyruqlari

```
/admin - Admin panel
/settings - Sozlamalar va status
```

### 5.2. Admin Imkoniyatlari

- 👑 Premium tarif (avtomatik)
- 📊 Barcha funksiyalar cheksiz
- 🔧 Tizim sozlamalari (keyinroq)
- 👥 Foydalanuvchilar statistikasi (keyinroq)

### 5.3. Yangi Admin Qo'shish

1. User ID ni oling ([@userinfobot](https://t.me/userinfobot))
2. `config.py` ni oching
3. `ADMIN_USERS` ga qo'shing:
   ```python
   ADMIN_USERS = [
       123456789,  # Birinchi admin
       987654321,  # Yangi admin
   ]
   ```
4. Botni qayta ishga tushiring

---

## 6. Deployment

### 6.1. Railway

#### Tayyorgarlik

1. [railway.app](https://railway.app) ga ro'yxatdan o'ting
2. GitHub repository yarating
3. Kodni GitHub'ga yuklang

#### Deploy Qilish

1. Railway'da "New Project" bosing
2. "Deploy from GitHub repo" tanlang
3. Repository ni tanlang
4. Environment variables qo'shing:
   - `BOT_TOKEN`
   - `GROQ_API_KEY_1`
   - `GROQ_API_KEY_2`
   - `GEMINI_API_KEY`
5. Deploy tugmasini bosing

#### Sozlamalar

**Start Command:**
```
python bot.py
```

**Build Command:**
```
pip install -r requirements.txt
```

### 6.2. Render

1. [render.com](https://render.com) ga kiring
2. "New Web Service" yarating
3. GitHub repository ulang
4. Environment variables qo'shing
5. Deploy qiling

### 6.3. VPS (Ubuntu)

```bash
# Serverni yangilash
sudo apt update && sudo apt upgrade -y

# Python o'rnatish
sudo apt install python3.11 python3.11-venv -y

# Loyihani yuklab olish
git clone https://github.com/YOUR_USERNAME/aris-finance-bot.git
cd aris-finance-bot

# Virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Kutubxonalar
pip install -r requirements.txt

# .env yaratish
nano .env
# API kalitlarni kiriting

# Systemd service yaratish
sudo nano /etc/systemd/system/aris-bot.service
```

**Service fayl:**
```ini
[Unit]
Description=ARIS Finance Bot
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/aris-finance-bot
Environment="PATH=/path/to/aris-finance-bot/venv/bin"
ExecStart=/path/to/aris-finance-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Ishga tushirish:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable aris-bot
sudo systemctl start aris-bot
sudo systemctl status aris-bot
```

---

## 7. Muammolarni Hal Qilish

### 7.1. Bot Ishga Tushmayapti

**Xato:** `Invalid token`
- ✅ `.env` fayldagi `BOT_TOKEN` ni tekshiring
- ✅ @BotFather dan yangi token oling

**Xato:** `Module not found`
- ✅ Virtual environment aktivlashtirilganini tekshiring
- ✅ `pip install -r requirements.txt` qayta ishga tushiring

### 7.2. AI Ishlamayapti

**Xato:** `API key invalid`
- ✅ Groq va Gemini API kalitlarni tekshiring
- ✅ API limitlar tugaganini tekshiring

**Xato:** `Rate limit exceeded`
- ✅ Fallback tizimi avtomatik ishlaydi
- ✅ Ikkinchi Groq kalit yoki Gemini ishlatiladi

### 7.3. Database Xatolari

**Xato:** `Database locked`
- ✅ Faqat bitta bot instance ishlayotganini tekshiring
- ✅ Database faylni o'chiring va qayta yarating

**Database tozalash:**
```bash
rm database/aris.db
python bot.py  # Yangi database yaratiladi
```

### 7.4. Export Ishlamayapti

**Xato:** `File not found`
- ✅ `exports/` papka mavjudligini tekshiring
- ✅ Yozish huquqlari borligini tekshiring

**Excel ochilmayapti:**
- ✅ Microsoft Excel yoki LibreOffice o'rnatilgan bo'lishi kerak
- ✅ Fayl buzilmagan bo'lishi kerak

### 7.5. Loglarni Ko'rish

```bash
# Terminal'da
python bot.py

# Loglar konsolda ko'rinadi
INFO:aiogram:Update received
INFO:database:Transaction added
ERROR:ai_service:API error
```

---

## 📞 Yordam

### Tez-tez So'raladigan Savollar

**Q: User ID ni qayerdan topaman?**  
A: [@userinfobot](https://t.me/userinfobot) ga `/start` yuboring

**Q: Limitlarni qanday o'zgartiraman?**  
A: `config.py` da `SUBSCRIPTION_LIMITS` ni o'zgartiring

**Q: Database qayerda saqlanadi?**  
A: `database/aris.db` faylida (SQLite)

**Q: Export fayllari qayerda?**  
A: `exports/` papkada

**Q: Necha foydalanuvchi ishlata oladi?**  
A: Cheklovsiz, lekin API limitlariga bog'liq

### Murojaat

- 📧 Email: support@example.com
- 💬 Telegram: @support_username
- 🐛 Issues: GitHub Issues

---

**Versiya:** 2.0  
**Yangilangan:** 2026-02-09  
**Muallif:** ARIS Development Team

# ARIS Finance Bot

Shaxsiy moliyaviy yordamchi Telegram bot

## ✨ Imkoniyatlar

- 🎤 Ovozli moliyaviy tahlil
- 📊 Kirim/chiqim statistikasi
- 🎯 Moliyaviy maqsadlar
- 📝 Kundalik va AI tahlili
- 📈 Haftalik/oylik hisobotlar
- 📥 Excel/PDF export

## 🚀 Tezkor Boshlash

### O'rnatish

```bash
# Loyihani klonlash
git clone https://github.com/YOUR_USERNAME/aris-finance-bot.git
cd aris-finance-bot

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Kutubxonalar
pip install -r requirements.txt
```

### Sozlash

1. `.env` fayl yarating:
```env
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY_1=your_groq_key_1
GROQ_API_KEY_2=your_groq_key_2
GEMINI_API_KEY=your_gemini_key
```

2. `config.py` da admin qo'shing:
```python
ADMIN_USERS = [123456789]  # Sizning user ID
```

3. Botni ishga tushiring:
```bash
python bot.py
```

## 📖 Dokumentatsiya

- [Batafsil Qo'llanma](QOLLANMA.md)
- [O'zgarishlar](changelog.md)

## 🌐 Deployment

### Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Repository'ni fork qiling
2. Railway'da "Deploy from GitHub" tanlang
3. Environment variables qo'shing
4. Deploy qiling

### Render

1. [render.com](https://render.com) ga kiring
2. "New Web Service" yarating
3. GitHub repository ulang
4. Environment variables sozlang

## 🛠️ Texnologiyalar

- Python 3.11+
- Aiogram 3.15.0
- SQLite (aiosqlite)
- Groq AI (Whisper, LLaMA)
- Google Gemini
- OpenPyXL, ReportLab

## 📝 Litsenziya

MIT License

## 👨‍💻 Muallif

ARIS Development Team

---

**Versiya:** 2.0  
**Yangilangan:** 2026-02-09

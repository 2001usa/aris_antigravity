"""
ARIS Bot Configuration
Barcha sozlamalar va konstantalar
"""
import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

# AI Service API Keys
GROQ_API_KEY_1 = os.getenv("GROQ_API_KEY_1")
GROQ_API_KEY_2 = os.getenv("GROQ_API_KEY_2")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "database/aris.db")

# Admin Users (user_id ro'yxati)
ADMIN_USERS = [7586510077
    # Admin user ID'larini bu yerga qo'shing
    # Misol: 123456789, 987654321
]

# Subscription Tiers
class SubscriptionTier:
    STANDARD = "standard"
    PREMIUM = "premium"

# Tarif limitleri (HOZIRCHA O'CHIRILGAN - TEST UCHUN)
ENABLE_LIMITS = False  # True qilsangiz limitlar ishlaydi

SUBSCRIPTION_LIMITS = {
    SubscriptionTier.STANDARD: int(os.getenv("STANDARD_LIMIT", 1890000)),
    SubscriptionTier.PREMIUM: int(os.getenv("PREMIUM_LIMIT", 2400000)),
}

# Tarif funksiyalari
SUBSCRIPTION_FEATURES = {
    SubscriptionTier.STANDARD: {
        "voice_analysis": True,
        "statistics": True,
        "goals": True,
        "diary": True,
        "weekly_report": True,
        "monthly_report": False,
        "excel_export": True,
        "pdf_export": True,
    },
    SubscriptionTier.PREMIUM: {
        "voice_analysis": True,
        "statistics": True,
        "goals": True,
        "diary": True,
        "diary_ai_analysis": True,
        "weekly_report": True,
        "monthly_report": True,
        "excel_export": True,
        "pdf_export": True,
    },
}

# Tarif nomlari (o'zbekcha)
SUBSCRIPTION_NAMES = {
    SubscriptionTier.STANDARD: "💙 Standart",
    SubscriptionTier.PREMIUM: "💎 Premium (Admin)",
}

# Kategoriyalar
EXPENSE_CATEGORIES = [
    "🍔 Oziq-ovqat",
    "🚗 Transport",
    "🏠 Uy-joy",
    "💊 Sog'liq",
    "🎓 Ta'lim",
    "🎮 O'yin-kulgi",
    "👕 Kiyim",
    "📱 Aloqa",
    "🔧 Boshqa",
]

INCOME_CATEGORIES = [
    "💰 Maosh",
    "💼 Biznes",
    "🎁 Sovg'a",
    "📈 Investitsiya",
    "🔧 Boshqa",
]

# AI Model sozlamalari
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_WHISPER_MODEL = "whisper-large-v3"
GEMINI_MODEL = "gemini-2.0-flash-exp"

# Prompt shablonlari
TRANSACTION_ANALYSIS_PROMPT = """
Siz moliyaviy yordamchisiz. Foydalanuvchi ovozli xabar yubordi va u matnga o'girildi.
Sizning vazifangiz: matndan moliyaviy ma'lumotlarni ajratib olish.

Matn: {text}

Quyidagi formatda JSON qaytaring:
{{
    "type": "income" yoki "expense",
    "amount": raqam (faqat raqam, so'm belgisisiz),
    "category": kategoriya nomi,
    "description": qisqa tavsif
}}

Kategoriyalar:
Chiqim: Oziq-ovqat, Transport, Uy-joy, Sog'liq, Ta'lim, O'yin-kulgi, Kiyim, Aloqa, Boshqa
Kirim: Maosh, Biznes, Sovg'a, Investitsiya, Boshqa

Faqat JSON qaytaring, boshqa hech narsa yozmaslik kerak.
"""

DIARY_ANALYSIS_PROMPT = """
Siz psixolog yordamchisiz. Foydalanuvchi kundalik yozdi.

Kundalik: {text}

Qisqa tahlil bering (3-4 jumla):
1. Asosiy kayfiyat
2. Muhim voqealar
3. Qisqa maslahat

O'zbekcha javob bering.
"""

WEEKLY_REPORT_PROMPT = """
Siz moliyaviy tahlilchisiz. Haftalik hisobot tayyorlang.

Ma'lumotlar:
- Jami kirim: {total_income} so'm
- Jami chiqim: {total_expense} so'm
- Balans: {balance} so'm
- Eng ko'p chiqim: {top_category}

Qisqa tahlil va maslahat bering (5-6 jumla). O'zbekcha yozing.
"""

MONTHLY_REPORT_PROMPT = """
Siz moliyaviy tahlilchisiz. Oylik hisobot tayyorlang.

Ma'lumotlar:
- Jami kirim: {total_income} so'm
- Jami chiqim: {total_expense} so'm
- Balans: {balance} so'm
- Maqsadlar: {goals_progress}

Batafsil tahlil va strategik maslahatlar bering (10-12 jumla). O'zbekcha yozing.
"""

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
ADMIN_USERS = [
    7586510077,  # @Aslbek_1203
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
TRANSACTION_ANALYSIS_PROMPT = """Matndan moliyaviy ma'lumot ajratib, JSON qaytaring:

Matn: {text}

Format:
{{"type": "income/expense", "amount": raqam, "category": "kategoriya", "description": "tavsif"}}

Kategoriyalar - Chiqim: Oziq-ovqat, Transport, Uy-joy, Sog'liq, Ta'lim, O'yin-kulgi, Kiyim, Aloqa, Boshqa
Kirim: Maosh, Biznes, Sovg'a, Investitsiya, Boshqa

Faqat JSON, boshqa hech narsa."""

DIARY_ANALYSIS_PROMPT = """Kundalik tahlil (3-4 jumla):

{text}

1. Kayfiyat 2. Muhim voqea 3. Maslahat"""

WEEKLY_REPORT_PROMPT = """Haftalik tahlil (5 jumla):

Kirim: {total_income} | Chiqim: {total_expense} | Balans: {balance}
Eng ko'p: {top_category}

Tahlil va maslahat bering."""

MONTHLY_REPORT_PROMPT = """Oylik hisobot (8-10 jumla):

Kirim: {total_income} | Chiqim: {total_expense} | Balans: {balance}
Maqsadlar: {goals_progress}

Batafsil tahlil va strategiya."""


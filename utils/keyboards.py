"""
Telegram Keyboards
Barcha inline va reply klaviaturalar
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import config

def get_main_menu() -> ReplyKeyboardMarkup:
    """Asosiy menyu"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="💰 Moliya"),
        KeyboardButton(text="📊 Statistika")
    )
    builder.row(
        KeyboardButton(text="🎯 Maqsadlar"),
        KeyboardButton(text="📝 Kundalik")
    )
    builder.row(
        KeyboardButton(text="📈 Hisobotlar"),
        KeyboardButton(text="⚙️ Sozlamalar")
    )
    return builder.as_markup(resize_keyboard=True)

def get_subscription_menu() -> InlineKeyboardMarkup:
    """Tarif tanlash menyu"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=config.SUBSCRIPTION_NAMES[config.SubscriptionTier.MINIMAL],
            callback_data=f"sub_{config.SubscriptionTier.MINIMAL}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=config.SUBSCRIPTION_NAMES[config.SubscriptionTier.STANDARD],
            callback_data=f"sub_{config.SubscriptionTier.STANDARD}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=config.SUBSCRIPTION_NAMES[config.SubscriptionTier.PREMIUM],
            callback_data=f"sub_{config.SubscriptionTier.PREMIUM}"
        )
    )
    return builder.as_markup()

def get_transaction_type_menu() -> InlineKeyboardMarkup:
    """Tranzaksiya turi tanlash"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💵 Kirim", callback_data="trans_type_income"),
        InlineKeyboardButton(text="💸 Chiqim", callback_data="trans_type_expense")
    )
    return builder.as_markup()

def get_category_menu(trans_type: str) -> InlineKeyboardMarkup:
    """Kategoriya tanlash"""
    builder = InlineKeyboardBuilder()
    
    categories = config.INCOME_CATEGORIES if trans_type == "income" else config.EXPENSE_CATEGORIES
    
    for category in categories:
        builder.row(
            InlineKeyboardButton(
                text=category,
                callback_data=f"cat_{trans_type}_{category}"
            )
        )
    
    return builder.as_markup()

def get_export_menu() -> InlineKeyboardMarkup:
    """Export opsiyalari"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Excel", callback_data="export_excel"),
        InlineKeyboardButton(text="📄 PDF", callback_data="export_pdf")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_main")
    )
    return builder.as_markup()

def get_report_menu() -> InlineKeyboardMarkup:
    """Hisobot menyu"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📅 Haftalik", callback_data="report_weekly")
    )
    builder.row(
        InlineKeyboardButton(text="📆 Oylik", callback_data="report_monthly")
    )
    builder.row(
        InlineKeyboardButton(text="📤 Export", callback_data="show_export")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_main")
    )
    return builder.as_markup()

def get_goals_menu() -> InlineKeyboardMarkup:
    """Maqsadlar menyu"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="➕ Yangi maqsad", callback_data="goal_new")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Maqsadlarim", callback_data="goal_list")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_main")
    )
    return builder.as_markup()

def get_back_button() -> InlineKeyboardMarkup:
    """Orqaga tugmasi"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_main")
    )
    return builder.as_markup()

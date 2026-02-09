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

def get_goal_actions_keyboard(goal_id: int) -> InlineKeyboardMarkup:
    """Maqsad uchun action tugmalari"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💰 Pul qo'shish", callback_data=f"goal_add_money_{goal_id}")
    )
    builder.row(
        InlineKeyboardButton(text="✏️ Tahrirlash", callback_data=f"goal_edit_{goal_id}"),
        InlineKeyboardButton(text="🗑️ O'chirish", callback_data=f"goal_delete_{goal_id}")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="goal_list")
    )
    return builder.as_markup()

def get_goal_edit_menu(goal_id: int) -> InlineKeyboardMarkup:
    """Maqsad tahrirlash menyusi"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📝 Nomini o'zgartirish", callback_data=f"goal_edit_title_{goal_id}")
    )
    builder.row(
        InlineKeyboardButton(text="💰 Summasini o'zgartirish", callback_data=f"goal_edit_amount_{goal_id}")
    )
    builder.row(
        InlineKeyboardButton(text="📅 Muddatni o'zgartirish", callback_data=f"goal_edit_deadline_{goal_id}")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data=f"goal_view_{goal_id}")
    )
    return builder.as_markup()

def get_confirmation_keyboard(action: str, item_id: int) -> InlineKeyboardMarkup:
    """Tasdiqlash dialogi"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Ha", callback_data=f"confirm_{action}_{item_id}"),
        InlineKeyboardButton(text="❌ Yo'q", callback_data=f"cancel_{action}_{item_id}")
    )
    return builder.as_markup()

def get_settings_menu() -> InlineKeyboardMarkup:
    """Sozlamalar menyusi"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💱 Valyuta", callback_data="settings_currency")
    )
    builder.row(
        InlineKeyboardButton(text="🎨 Mavzu", callback_data="settings_theme")
    )
    builder.row(
        InlineKeyboardButton(text="📧 Profil", callback_data="settings_profile")
    )
    builder.row(
        InlineKeyboardButton(text="🔔 Bildirishnomalar", callback_data="settings_notifications")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_main")
    )
    return builder.as_markup()

def get_currency_menu(current: str = "UZS") -> InlineKeyboardMarkup:
    """Valyuta tanlash menyusi"""
    builder = InlineKeyboardBuilder()
    
    currencies = [
        ("🇺🇿 O'zbek so'mi (UZS)", "UZS"),
        ("🇺🇸 Dollar (USD)", "USD"),
        ("🇷🇺 Rubl (RUB)", "RUB")
    ]
    
    for name, code in currencies:
        mark = "✅ " if code == current else ""
        builder.row(
            InlineKeyboardButton(text=f"{mark}{name}", callback_data=f"set_currency_{code}")
        )
    
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_settings")
    )
    return builder.as_markup()

def get_theme_menu(current: str = "auto") -> InlineKeyboardMarkup:
    """Mavzu tanlash menyusi"""
    builder = InlineKeyboardBuilder()
    
    themes = [
        ("☀️ Yorug'", "light"),
        ("🌙 Qorong'i", "dark"),
        ("🔄 Avtomatik", "auto")
    ]
    
    for name, code in themes:
        mark = "✅ " if code == current else ""
        builder.row(
            InlineKeyboardButton(text=f"{mark}{name}", callback_data=f"set_theme_{code}")
        )
    
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_settings")
    )
    return builder.as_markup()

def get_notifications_menu(enabled: bool = True) -> InlineKeyboardMarkup:
    """Bildirishnomalar menyusi"""
    builder = InlineKeyboardBuilder()
    
    status = "🔔 Yoqilgan" if enabled else "🔕 O'chirilgan"
    action = "off" if enabled else "on"
    button_text = "🔕 O'chirish" if enabled else "🔔 Yoqish"
    
    builder.row(
        InlineKeyboardButton(text=f"Hozirgi holat: {status}", callback_data="noop")
    )
    builder.row(
        InlineKeyboardButton(
            text=button_text, 
            callback_data=f"set_notifications_{action}"
        )
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_settings")
    )
    return builder.as_markup()

def get_profile_menu() -> InlineKeyboardMarkup:
    """Profil tahrirlash menyusi"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📱 Telefon raqam", callback_data="profile_edit_phone")
    )
    builder.row(
        InlineKeyboardButton(text="📧 Email", callback_data="profile_edit_email")
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_settings")
    )
    return builder.as_markup()

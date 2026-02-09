"""
Settings Handler
Sozlamalar boshqaruvi
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import Database
from utils.keyboards import (
    get_settings_menu, get_currency_menu, get_theme_menu,
    get_notifications_menu, get_profile_menu
)
from utils.subscription import SubscriptionManager

router = Router()
db = Database()
sub_manager = SubscriptionManager()

class SettingsStates(StatesGroup):
    """Sozlamalar holatlari"""
    editing_phone = State()
    editing_email = State()

@router.message(F.text == "⚙️ Sozlamalar")
async def settings_menu(message: Message):
    """Sozlamalar menyusi"""
    user_id = message.from_user.id
    
    # Tarif ma'lumotlari
    status = await sub_manager.format_subscription_status(user_id)
    
    await message.answer(
        f"⚙️ <b>Sozlamalar</b>\n\n"
        f"{status}\n\n"
        f"Quyidagi sozlamalarni o'zgartirishingiz mumkin:",
        parse_mode="HTML",
        reply_markup=get_settings_menu()
    )

# Valyuta
@router.callback_query(F.data == "settings_currency")
async def currency_settings(callback: CallbackQuery):
    """Valyuta sozlamalari"""
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    current_currency = user.get("currency", "UZS") if user else "UZS"
    
    await callback.message.edit_text(
        "💱 <b>Valyuta tanlash</b>\n\n"
        "Qaysi valyutada ishlashni xohlaysiz?",
        parse_mode="HTML",
        reply_markup=get_currency_menu(current_currency)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("set_currency_"))
async def set_currency(callback: CallbackQuery):
    """Valyutani o'rnatish"""
    currency = callback.data.split("_")[2]
    user_id = callback.from_user.id
    
    success = await db.update_user_settings(user_id, currency=currency)
    
    if success:
        currency_names = {
            "UZS": "O'zbek so'mi",
            "USD": "Dollar",
            "RUB": "Rubl"
        }
        await callback.answer(
            f"✅ Valyuta o'zgartirildi: {currency_names.get(currency, currency)}",
            show_alert=True
        )
        # Menyuni yangilash
        await currency_settings(callback)
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

# Mavzu
@router.callback_query(F.data == "settings_theme")
async def theme_settings(callback: CallbackQuery):
    """Mavzu sozlamalari"""
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    current_theme = user.get("theme", "auto") if user else "auto"
    
    await callback.message.edit_text(
        "🎨 <b>Mavzu tanlash</b>\n\n"
        "Qaysi mavzuni afzal ko'rasiz?\n\n"
        "<i>💡 Eslatma: Bu sozlama hozircha faqat saqlanadi, interfeys o'zgarishi keyingi versiyalarda qo'shiladi.</i>",
        parse_mode="HTML",
        reply_markup=get_theme_menu(current_theme)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("set_theme_"))
async def set_theme(callback: CallbackQuery):
    """Mavzuni o'rnatish"""
    theme = callback.data.split("_")[2]
    user_id = callback.from_user.id
    
    success = await db.update_user_settings(user_id, theme=theme)
    
    if success:
        theme_names = {
            "light": "Yorug'",
            "dark": "Qorong'i",
            "auto": "Avtomatik"
        }
        await callback.answer(
            f"✅ Mavzu o'zgartirildi: {theme_names.get(theme, theme)}",
            show_alert=True
        )
        # Menyuni yangilash
        await theme_settings(callback)
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

# Bildirishnomalar
@router.callback_query(F.data == "settings_notifications")
async def notifications_settings(callback: CallbackQuery):
    """Bildirishnomalar sozlamalari"""
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    enabled = bool(user.get("notifications_enabled", 1)) if user else True
    
    await callback.message.edit_text(
        "🔔 <b>Bildirishnomalar</b>\n\n"
        "Bildirishnomalarni yoqish yoki o'chirish:\n\n"
        "<i>💡 Eslatma: Bu sozlama kelajakda haftalik/oylik hisobotlar uchun ishlatiladi.</i>",
        parse_mode="HTML",
        reply_markup=get_notifications_menu(enabled)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("set_notifications_"))
async def set_notifications(callback: CallbackQuery):
    """Bildirishnomalarni o'rnatish"""
    action = callback.data.split("_")[2]
    user_id = callback.from_user.id
    enabled = (action == "on")
    
    success = await db.update_user_settings(user_id, notifications_enabled=enabled)
    
    if success:
        status = "yoqildi" if enabled else "o'chirildi"
        await callback.answer(f"✅ Bildirishnomalar {status}", show_alert=True)
        # Menyuni yangilash
        await notifications_settings(callback)
    else:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

# Profil
@router.callback_query(F.data == "settings_profile")
async def profile_settings(callback: CallbackQuery):
    """Profil sozlamalari"""
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    
    phone = user.get("phone", "Kiritilmagan") if user else "Kiritilmagan"
    email = user.get("email", "Kiritilmagan") if user else "Kiritilmagan"
    
    await callback.message.edit_text(
        f"📧 <b>Profil ma'lumotlari</b>\n\n"
        f"📱 Telefon: {phone}\n"
        f"📧 Email: {email}\n\n"
        f"O'zgartirish uchun tugmani bosing:",
        parse_mode="HTML",
        reply_markup=get_profile_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "profile_edit_phone")
async def edit_phone_start(callback: CallbackQuery, state: FSMContext):
    """Telefon tahrirlash boshlash"""
    await callback.message.edit_text(
        "📱 <b>Telefon raqam</b>\n\n"
        "Telefon raqamingizni kiriting (masalan: +998901234567):",
        parse_mode="HTML"
    )
    await state.set_state(SettingsStates.editing_phone)
    await callback.answer()

@router.message(SettingsStates.editing_phone)
async def edit_phone_received(message: Message, state: FSMContext):
    """Telefon qabul qilindi"""
    user_id = message.from_user.id
    phone = message.text.strip()
    
    success = await db.update_user_settings(user_id, phone=phone)
    
    if success:
        await message.answer(f"✅ Telefon raqam saqlandi: {phone}")
    else:
        await message.answer("❌ Xatolik yuz berdi.")
    
    await state.clear()

@router.callback_query(F.data == "profile_edit_email")
async def edit_email_start(callback: CallbackQuery, state: FSMContext):
    """Email tahrirlash boshlash"""
    await callback.message.edit_text(
        "📧 <b>Email manzil</b>\n\n"
        "Email manzilingizni kiriting:",
        parse_mode="HTML"
    )
    await state.set_state(SettingsStates.editing_email)
    await callback.answer()

@router.message(SettingsStates.editing_email)
async def edit_email_received(message: Message, state: FSMContext):
    """Email qabul qilindi"""
    user_id = message.from_user.id
    email = message.text.strip()
    
    # Oddiy email validatsiya
    if "@" not in email or "." not in email:
        await message.answer("❌ Noto'g'ri email format. Iltimos, qaytadan kiriting.")
        return
    
    success = await db.update_user_settings(user_id, email=email)
    
    if success:
        await message.answer(f"✅ Email saqlandi: {email}")
    else:
        await message.answer("❌ Xatolik yuz berdi.")
    
    await state.clear()

# Orqaga qaytish
@router.callback_query(F.data == "back_settings")
async def back_to_settings(callback: CallbackQuery):
    """Sozlamalarga qaytish"""
    user_id = callback.from_user.id
    status = await sub_manager.format_subscription_status(user_id)
    
    await callback.message.edit_text(
        f"⚙️ <b>Sozlamalar</b>\n\n"
        f"{status}\n\n"
        f"Quyidagi sozlamalarni o'zgartirishingiz mumkin:",
        parse_mode="HTML",
        reply_markup=get_settings_menu()
    )
    await callback.answer()

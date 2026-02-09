"""
Start Handler
/start va /help buyruqlari, tarif tanlash
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.db import Database
from utils.keyboards import get_main_menu, get_subscription_menu
from utils.subscription import SubscriptionManager
import config

router = Router()
db = Database()
sub_manager = SubscriptionManager()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Bot boshlash"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Foydalanuvchini qo'shish
    await db.add_user(user_id, username, first_name)
    
    # Tarifni avtomatik belgilash
    if sub_manager.is_admin(user_id):
        tier = config.SubscriptionTier.PREMIUM
        await db.update_subscription(user_id, tier)
        admin_msg = "\n\n👑 <b>Siz Admin sifatida Premium tarifga egasiz!</b>"
    else:
        tier = config.SubscriptionTier.STANDARD
        await db.update_subscription(user_id, tier)
        admin_msg = ""
    
    tier_name = config.SUBSCRIPTION_NAMES.get(tier)
    tier_desc = sub_manager.get_tier_description(tier)
    
    await message.answer(
        f"👋 Xush kelibsiz, {first_name}!\n\n"
        f"🤖 <b>ARIS</b> - Shaxsiy moliyaviy yordamchingiz\n\n"
        f"Ovozli xabar yuboring, men sizning kirim va chiqimlaringizni "
        f"avtomatik tahlil qilaman va statistika tayyorlayman.\n\n"
        f"📊 <b>Sizning tarifingiz:</b> {tier_name}{admin_msg}\n\n"
        f"{tier_desc}",
        parse_mode="HTML",
        reply_markup=get_main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam"""
    help_text = (
        "🤖 <b>ARIS Bot - Yordam</b>\n\n"
        
        "<b>💰 Moliya:</b>\n"
        "• Ovozli xabar yuboring: 'Bugun non uchun 5000 so'm sarfladim'\n"
        "• Bot avtomatik tahlil qiladi va saqlaydi\n\n"
        
        "<b>📊 Statistika:</b>\n"
        "• Jami kirim va chiqimlaringizni ko'ring\n"
        "• Kategoriya bo'yicha taqsimot\n\n"
        
        "<b>🎯 Maqsadlar:</b>\n"
        "• Moliyaviy maqsadlar qo'ying\n"
        "• Progress kuzating\n\n"
        
        "<b>📝 Kundalik:</b> (Standart+ tarif)\n"
        "• Kundalik yozing\n"
        "• AI tahlil oling (Premium)\n\n"
        
        "<b>📈 Hisobotlar:</b> (Standart+ tarif)\n"
        "• Haftalik/Oylik hisobotlar\n"
        "• Excel/PDF export\n\n"
        
        "<b>Buyruqlar:</b>\n"
        "/start - Botni boshlash\n"
        "/help - Yordam\n"
        "/settings - Sozlamalar"
    )
    
    await message.answer(help_text, parse_mode="HTML")

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """Sozlamalar"""
    user_id = message.from_user.id
    
    # Tarif ma'lumotlari
    status = await sub_manager.format_subscription_status(user_id)
    
    await message.answer(
        f"⚙️ <b>Sozlamalar</b>\n\n"
        f"{status}",
        parse_mode="HTML"
    )

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Admin panel (faqat adminlar uchun)"""
    user_id = message.from_user.id
    
    if not sub_manager.is_admin(user_id):
        await message.answer("❌ Bu buyruq faqat adminlar uchun!")
        return
    
    await message.answer(
        "👑 <b>Admin Panel</b>\n\n"
        "Mavjud buyruqlar:\n"
        "/admin - Admin panel\n"
        "/stats - Umumiy statistika\n"
        "/users - Foydalanuvchilar ro'yxati\n\n"
        "📝 <b>Admin qo'shish:</b>\n"
        "config.py faylida ADMIN_USERS ro'yxatiga user_id qo'shing",
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    """Asosiy menyuga qaytish"""
    await callback.message.delete()
    await callback.message.answer(
        "Asosiy menyu:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

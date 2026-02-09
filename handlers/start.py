"""
Start Handler
/start va /help buyruqlari, tarif tanlash
"""
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Admin panel (faqat adminlar uchun)"""
    user_id = message.from_user.id
    
    if not sub_manager.is_admin(user_id):
        await message.answer("❌ Bu buyruq faqat adminlar uchun!")
        return
    
    # Umumiy statistika
    total_users = await db.get_total_users()
    active_today = await db.get_active_users_today()
    total_transactions = await db.get_total_transactions()
    
    await message.answer(
        "👑 <b>Admin Panel</b>\n\n"
        f"👥 Jami foydalanuvchilar: {total_users}\n"
        f"✅ Bugun aktiv: {active_today}\n"
        f"💰 Jami tranzaksiyalar: {total_transactions}\n\n"
        "<b>Buyruqlar:</b>\n"
        "/stats - Batafsil statistika\n"
        "/users - Foydalanuvchilar ro'yxati\n"
        "/broadcast - Xabar yuborish (tez orada)\n\n"
        "📝 <b>Admin qo'shish:</b>\n"
        "config.py → ADMIN_USERS",
        parse_mode="HTML"
    )

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Umumiy statistika (adminlar uchun)"""
    user_id = message.from_user.id
    
    if not sub_manager.is_admin(user_id):
        await message.answer("❌ Bu buyruq faqat adminlar uchun!")
        return
    
    # Statistika to'plash
    stats = await db.get_admin_statistics()
    
    await message.answer(
        "📊 <b>Tizim Statistikasi</b>\n\n"
        f"👥 <b>Foydalanuvchilar:</b>\n"
        f"  • Jami: {stats['total_users']}\n"
        f"  • Bugun: {stats['new_users_today']}\n"
        f"  • Aktiv (7 kun): {stats['active_week']}\n\n"
        f"💰 <b>Tranzaksiyalar:</b>\n"
        f"  • Jami: {stats['total_transactions']}\n"
        f"  • Bugun: {stats['transactions_today']}\n"
        f"  • Shu hafta: {stats['transactions_week']}\n\n"
        f"📈 <b>Moliyaviy:</b>\n"
        f"  • Jami kirim: {stats['total_income']:,.0f} so'm\n"
        f"  • Jami chiqim: {stats['total_expense']:,.0f} so'm\n\n"
        f"🎯 <b>Maqsadlar:</b>\n"
        f"  • Jami: {stats['total_goals']}\n"
        f"  • Bajarilgan: {stats['completed_goals']}\n\n"
        f"🤖 <b>AI Ishlatilishi:</b>\n"
        f"  • Groq: {stats['groq_usage']:,} token\n"
        f"  • Gemini: {stats['gemini_usage']:,} token",
        parse_mode="HTML"
    )

@router.message(Command("users"))
async def cmd_users(message: Message):
    """Foydalanuvchilar ro'yxati (adminlar uchun)"""
    user_id = message.from_user.id
    
    if not sub_manager.is_admin(user_id):
        await message.answer("❌ Bu buyruq faqat adminlar uchun!")
        return
    
    # Foydalanuvchilar ro'yxati
    users = await db.get_all_users(limit=20)
    
    if not users:
        await message.answer("📭 Foydalanuvchilar yo'q")
        return
    
    text = "👥 <b>Foydalanuvchilar Ro'yxati</b>\n\n"
    
    for i, user in enumerate(users, 1):
        tier_emoji = "💎" if user['subscription_tier'] == 'premium' else "💙"
        text += (
            f"{i}. {tier_emoji} <b>{user['first_name']}</b>\n"
            f"   ID: <code>{user['user_id']}</code>\n"
            f"   @{user['username'] or 'username_yoq'}\n"
            f"   Tarif: {config.SUBSCRIPTION_NAMES.get(user['subscription_tier'])}\n"
            f"   Tokenlar: {user['tokens_used']:,}\n\n"
        )
    
    text += f"\n📊 Ko'rsatildi: {len(users)} ta"
    
    await message.answer(text, parse_mode="HTML")

@router.message(Command("token"))
async def cmd_token(message: Message, state: FSMContext):
    """Token hisoblash buyrug'i"""
    from utils.token_counter import format_token_info
    
    await message.answer(
        "📊 <b>Token Hisoblash</b>\n\n"
        "Matn yuboring, men sizga taxminiy token sonini ko'rsataman:",
        parse_mode="HTML"
    )
    await state.set_state("waiting_for_token_text")

@router.message(F.text, StateFilter("waiting_for_token_text"))
async def token_text_received(message: Message, state: FSMContext):
    """Token hisoblash uchun matn qabul qilindi"""
    from utils.token_counter import format_token_info
    
    text = message.text
    result = format_token_info(text, language="uzbek")
    
    await message.answer(result, parse_mode="HTML")
    await state.clear()

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    """Asosiy menyuga qaytish"""
    await callback.message.delete()
    await callback.message.answer(
        "Asosiy menyu:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

"""
Diary Handler
Kundalik yozish va AI tahlil (Standart+ tarif)
"""
from datetime import date
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import Database
from services.ai_service import AIService
from utils.subscription import SubscriptionManager

router = Router()
db = Database()
ai_service = AIService()
sub_manager = SubscriptionManager()

class DiaryStates(StatesGroup):
    """Kundalik holatlari"""
    waiting_for_entry = State()

@router.message(F.text == "📝 Kundalik")
async def diary_menu(message: Message, state: FSMContext):
    """Kundalik menyusi"""
    user_id = message.from_user.id
    
    # Ruxsatni tekshirish
    has_access = await sub_manager.check_feature_access(user_id, "diary")
    
    if not has_access:
        await message.answer(
            "🔒 <b>Kundalik funksiyasi</b>\n\n"
            "Bu funksiya faqat Standart va Premium tariflarda mavjud.\n\n"
            "Tarifni oshirish uchun /settings buyrug'ini yuboring.",
            parse_mode="HTML"
        )
        return
    
    # Oxirgi yozuvlarni ko'rsatish
    entries = await db.get_diary(user_id, limit=3)
    
    if entries:
        text = "📝 <b>Oxirgi yozuvlar:</b>\n\n"
        for entry in entries:
            text += f"📅 {entry['date']}\n{entry['content'][:100]}...\n\n"
        text += "\n💭 Bugun nima bo'ldi? Yozing:"
    else:
        text = "📝 <b>Kundalik</b>\n\n💭 Bugun nima bo'ldi? Yozing:"
    
    await message.answer(text, parse_mode="HTML")
    await state.set_state(DiaryStates.waiting_for_entry)

@router.message(DiaryStates.waiting_for_entry)
async def process_diary_entry(message: Message, state: FSMContext):
    """Kundalik yozuvini qayta ishlash"""
    user_id = message.from_user.id
    content = message.text
    
    # Premium tarif uchun AI tahlil
    has_ai = await sub_manager.check_feature_access(user_id, "diary_ai_analysis")
    
    ai_analysis = None
    
    if has_ai:
        # Token limitini tekshirish
        can_use, used, limit = await sub_manager.check_token_limit(user_id)
        
        if can_use:
            processing_msg = await message.answer("⏳ AI tahlil qilmoqdaman...")
            
            analysis, tokens = await ai_service.analyze_diary(content)
            
            if analysis:
                ai_analysis = analysis
                await db.track_ai_usage(user_id, "diary_analysis", tokens)
                await processing_msg.delete()
    
    # Kundalikni saqlash
    success = await db.add_diary(
        user_id=user_id,
        content=content,
        ai_analysis=ai_analysis
    )
    
    if success:
        response = "✅ <b>Kundalik saqlandi!</b>\n\n"
        
        if ai_analysis:
            response += f"🧠 <b>AI Tahlil:</b>\n{ai_analysis}"
        else:
            response += "📝 Yozuvingiz saqlandi."
        
        await message.answer(response, parse_mode="HTML")
    else:
        await message.answer("❌ Xatolik yuz berdi.")
    
    await state.clear()

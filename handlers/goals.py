"""
Goals Handler
Maqsadlar boshqaruvi
"""
from datetime import datetime, date
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import Database
from utils.keyboards import get_goals_menu, get_back_button

router = Router()
db = Database()

class GoalStates(StatesGroup):
    """Maqsad holatlari"""
    waiting_for_title = State()
    waiting_for_amount = State()
    waiting_for_deadline = State()

@router.message(F.text == "🎯 Maqsadlar")
async def goals_menu(message: Message):
    """Maqsadlar menyusi"""
    await message.answer(
        "🎯 <b>Maqsadlar</b>\n\n"
        "Moliyaviy maqsadlaringizni qo'ying va progress kuzating!",
        parse_mode="HTML",
        reply_markup=get_goals_menu()
    )

@router.callback_query(F.data == "goal_new")
async def new_goal_start(callback: CallbackQuery, state: FSMContext):
    """Yangi maqsad qo'shish boshlash"""
    await callback.message.edit_text(
        "🎯 <b>Yangi maqsad</b>\n\n"
        "Maqsad nomini yozing:",
        parse_mode="HTML"
    )
    await state.set_state(GoalStates.waiting_for_title)
    await callback.answer()

@router.message(GoalStates.waiting_for_title)
async def goal_title_received(message: Message, state: FSMContext):
    """Maqsad nomi qabul qilindi"""
    await state.update_data(title=message.text)
    await message.answer(
        "💰 Maqsad summasini yozing (so'mda):",
        parse_mode="HTML"
    )
    await state.set_state(GoalStates.waiting_for_amount)

@router.message(GoalStates.waiting_for_amount)
async def goal_amount_received(message: Message, state: FSMContext):
    """Maqsad summasi qabul qilindi"""
    try:
        amount = float(message.text.replace(",", "").replace(" ", ""))
        await state.update_data(target_amount=amount)
        
        data = await state.get_data()
        user_id = message.from_user.id
        
        # Maqsadni saqlash (deadline'siz)
        success = await db.add_goal(
            user_id=user_id,
            title=data["title"],
            target_amount=amount
        )
        
        if success:
            await message.answer(
                f"✅ <b>Maqsad qo'shildi!</b>\n\n"
                f"🎯 {data['title']}\n"
                f"💰 Maqsad: {amount:,} so'm",
                parse_mode="HTML"
            )
        else:
            await message.answer("❌ Xatolik yuz berdi.")
        
        await state.clear()
    
    except ValueError:
        await message.answer("❌ Noto'g'ri summa. Iltimos, faqat raqam kiriting.")

@router.callback_query(F.data == "goal_list")
async def show_goals(callback: CallbackQuery):
    """Maqsadlar ro'yxati"""
    user_id = callback.from_user.id
    goals = await db.get_goals(user_id)
    
    if not goals:
        await callback.message.edit_text(
            "📝 Hozircha maqsadlaringiz yo'q.\n\n"
            "Yangi maqsad qo'shish uchun 'Yangi maqsad' tugmasini bosing.",
            reply_markup=get_goals_menu()
        )
        await callback.answer()
        return
    
    text = "🎯 <b>Maqsadlarim:</b>\n\n"
    
    for goal in goals:
        progress = (goal["current_amount"] / goal["target_amount"] * 100) if goal["target_amount"] > 0 else 0
        filled = int(progress / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        text += (
            f"<b>{goal['title']}</b>\n"
            f"💰 {goal['current_amount']:,} / {goal['target_amount']:,} so'm\n"
            f"[{bar}] {progress:.1f}%\n\n"
        )
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_back_button()
    )
    await callback.answer()

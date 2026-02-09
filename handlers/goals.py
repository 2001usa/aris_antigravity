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
from utils.keyboards import (
    get_goals_menu, get_back_button, get_goal_actions_keyboard,
    get_goal_edit_menu, get_confirmation_keyboard
)
from utils.formatters import format_currency, format_deadline, format_progress_bar

router = Router()
db = Database()

class GoalStates(StatesGroup):
    """Maqsad holatlari"""
    waiting_for_title = State()
    waiting_for_amount = State()
    waiting_for_deadline = State()
    waiting_for_add_money = State()
    editing_title = State()
    editing_amount = State()
    editing_deadline = State()

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
        
        await message.answer(
            "📅 Muddatni kiriting (masalan: 2026-12-31)\n\n"
            "Yoki /skip yozing muddatsiz maqsad uchun:",
            parse_mode="HTML"
        )
        await state.set_state(GoalStates.waiting_for_deadline)
    
    except ValueError:
        await message.answer("❌ Noto'g'ri summa. Iltimos, faqat raqam kiriting.")

@router.message(GoalStates.waiting_for_deadline)
async def goal_deadline_received(message: Message, state: FSMContext):
    """Muddat qabul qilindi"""
    data = await state.get_data()
    user_id = message.from_user.id
    deadline = None
    
    if message.text.strip() != "/skip":
        try:
            deadline = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
        except ValueError:
            await message.answer(
                "❌ Noto'g'ri format. Iltimos, YYYY-MM-DD formatida kiriting\n"
                "Yoki /skip yozing."
            )
            return
    
    # Maqsadni saqlash
    success = await db.add_goal(
        user_id=user_id,
        title=data["title"],
        target_amount=data["target_amount"],
        deadline=deadline
    )
    
    if success:
        deadline_text = format_deadline(deadline) if deadline else "⏳ Muddatsiz"
        await message.answer(
            f"✅ <b>Maqsad qo'shildi!</b>\n\n"
            f"🎯 {data['title']}\n"
            f"💰 Maqsad: {data['target_amount']:,} so'm\n"
            f"{deadline_text}",
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Xatolik yuz berdi.")
    
    await state.clear()

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
    
    builder = InlineKeyboardBuilder()
    for goal in goals:
        progress = (goal["current_amount"] / goal["target_amount"] * 100) if goal["target_amount"] > 0 else 0
        
        # Har bir maqsad uchun tugma
        from aiogram.utils.keyboard import InlineKeyboardBuilder
        builder.row(
            InlineKeyboardButton(
                text=f"🎯 {goal['title']} ({progress:.0f}%)",
                callback_data=f"goal_view_{goal['id']}"
            )
        )
    
    builder.row(InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_main"))
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(F.data.startswith("goal_view_"))
async def view_goal(callback: CallbackQuery):
    """Maqsadni batafsil ko'rish"""
    goal_id = int(callback.data.split("_")[2])
    goal = await db.get_goal_by_id(goal_id)
    
    if not goal:
        await callback.answer("❌ Maqsad topilmadi", show_alert=True)
        return
    
    progress = (goal["current_amount"] / goal["target_amount"] * 100) if goal["target_amount"] > 0 else 0
    bar = format_progress_bar(goal["current_amount"], goal["target_amount"])
    deadline_text = format_deadline(goal.get("deadline"))
    
    text = (
        f"🎯 <b>{goal['title']}</b>\n\n"
        f"💰 Progress: {goal['current_amount']:,} / {goal['target_amount']:,} so'm\n"
        f"[{bar}] {progress:.1f}%\n\n"
        f"{deadline_text}"
    )
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_goal_actions_keyboard(goal_id)
    )
    await callback.answer()

# Pul qo'shish
@router.callback_query(F.data.startswith("goal_add_money_"))
async def add_money_start(callback: CallbackQuery, state: FSMContext):
    """Maqsadga pul qo'shish boshlash"""
    goal_id = int(callback.data.split("_")[3])
    await state.update_data(goal_id=goal_id)
    
    await callback.message.edit_text(
        "💰 <b>Pul qo'shish</b>\n\n"
        "Qancha pul qo'shmoqchisiz?",
        parse_mode="HTML"
    )
    await state.set_state(GoalStates.waiting_for_add_money)
    await callback.answer()

@router.message(GoalStates.waiting_for_add_money)
async def add_money_received(message: Message, state: FSMContext):
    """Qo'shiladigan pul qabul qilindi"""
    try:
        amount = float(message.text.replace(",", "").replace(" ", ""))
        data = await state.get_data()
        goal_id = data["goal_id"]
        
        success = await db.update_goal_progress(goal_id, amount)
        
        if success:
            goal = await db.get_goal_by_id(goal_id)
            progress = (goal["current_amount"] / goal["target_amount"] * 100) if goal["target_amount"] > 0 else 0
            
            await message.answer(
                f"✅ <b>Pul qo'shildi!</b>\n\n"
                f"💰 Qo'shildi: {amount:,} so'm\n"
                f"📊 Yangi progress: {progress:.1f}%",
                parse_mode="HTML"
            )
        else:
            await message.answer("❌ Xatolik yuz berdi.")
        
        await state.clear()
    
    except ValueError:
        await message.answer("❌ Noto'g'ri summa. Iltimos, faqat raqam kiriting.")

# Tahrirlash
@router.callback_query(F.data.startswith("goal_edit_"))
async def edit_goal_menu(callback: CallbackQuery):
    """Tahrirlash menyusi"""
    # Boshqa edit handlerlariga yo'naltirmaslik uchun tekshirish
    if callback.data.startswith("goal_edit_title_") or \
       callback.data.startswith("goal_edit_amount_") or \
       callback.data.startswith("goal_edit_deadline_"):
        return
    
    goal_id = int(callback.data.split("_")[2])
    
    await callback.message.edit_text(
        "✏️ <b>Maqsadni tahrirlash</b>\n\n"
        "Nimani o'zgartirmoqchisiz?",
        parse_mode="HTML",
        reply_markup=get_goal_edit_menu(goal_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("goal_edit_title_"))
async def edit_title_start(callback: CallbackQuery, state: FSMContext):
    """Nom tahrirlash boshlash"""
    goal_id = int(callback.data.split("_")[3])
    await state.update_data(goal_id=goal_id)
    
    await callback.message.edit_text(
        "📝 <b>Yangi nom</b>\n\n"
        "Maqsadning yangi nomini yozing:",
        parse_mode="HTML"
    )
    await state.set_state(GoalStates.editing_title)
    await callback.answer()

@router.message(GoalStates.editing_title)
async def edit_title_received(message: Message, state: FSMContext):
    """Yangi nom qabul qilindi"""
    data = await state.get_data()
    goal_id = data["goal_id"]
    
    success = await db.update_goal(goal_id, title=message.text)
    
    if success:
        await message.answer("✅ Nom o'zgartirildi!")
    else:
        await message.answer("❌ Xatolik yuz berdi.")
    
    await state.clear()

@router.callback_query(F.data.startswith("goal_edit_amount_"))
async def edit_amount_start(callback: CallbackQuery, state: FSMContext):
    """Summa tahrirlash boshlash"""
    goal_id = int(callback.data.split("_")[3])
    await state.update_data(goal_id=goal_id)
    
    await callback.message.edit_text(
        "💰 <b>Yangi summa</b>\n\n"
        "Maqsadning yangi summasini yozing:",
        parse_mode="HTML"
    )
    await state.set_state(GoalStates.editing_amount)
    await callback.answer()

@router.message(GoalStates.editing_amount)
async def edit_amount_received(message: Message, state: FSMContext):
    """Yangi summa qabul qilindi"""
    try:
        amount = float(message.text.replace(",", "").replace(" ", ""))
        data = await state.get_data()
        goal_id = data["goal_id"]
        
        success = await db.update_goal(goal_id, target_amount=amount)
        
        if success:
            await message.answer(f"✅ Summa o'zgartirildi: {amount:,} so'm")
        else:
            await message.answer("❌ Xatolik yuz berdi.")
        
        await state.clear()
    
    except ValueError:
        await message.answer("❌ Noto'g'ri summa. Iltimos, faqat raqam kiriting.")

@router.callback_query(F.data.startswith("goal_edit_deadline_"))
async def edit_deadline_start(callback: CallbackQuery, state: FSMContext):
    """Muddat tahrirlash boshlash"""
    goal_id = int(callback.data.split("_")[3])
    await state.update_data(goal_id=goal_id)
    
    await callback.message.edit_text(
        "📅 <b>Yangi muddat</b>\n\n"
        "Yangi muddatni kiriting (YYYY-MM-DD):\n"
        "Yoki /skip yozing muddatni olib tashlash uchun:",
        parse_mode="HTML"
    )
    await state.set_state(GoalStates.editing_deadline)
    await callback.answer()

@router.message(GoalStates.editing_deadline)
async def edit_deadline_received(message: Message, state: FSMContext):
    """Yangi muddat qabul qilindi"""
    data = await state.get_data()
    goal_id = data["goal_id"]
    deadline = None
    
    if message.text.strip() != "/skip":
        try:
            deadline = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
        except ValueError:
            await message.answer(
                "❌ Noto'g'ri format. Iltimos, YYYY-MM-DD formatida kiriting\n"
                "Yoki /skip yozing."
            )
            return
    
    success = await db.update_goal(goal_id, deadline=deadline)
    
    if success:
        deadline_text = format_deadline(deadline) if deadline else "⏳ Muddatsiz"
        await message.answer(f"✅ Muddat o'zgartirildi: {deadline_text}", parse_mode="HTML")
    else:
        await message.answer("❌ Xatolik yuz berdi.")
    
    await state.clear()

# O'chirish
@router.callback_query(F.data.startswith("goal_delete_"))
async def delete_goal_confirm(callback: CallbackQuery):
    """Maqsadni o'chirish tasdiqlanishi"""
    goal_id = int(callback.data.split("_")[2])
    goal = await db.get_goal_by_id(goal_id)
    
    if not goal:
        await callback.answer("❌ Maqsad topilmadi", show_alert=True)
        return
    
    await callback.message.edit_text(
        f"🗑️ <b>Maqsadni o'chirish</b>\n\n"
        f"Haqiqatan ham '{goal['title']}' maqsadini o'chirmoqchimisiz?",
        parse_mode="HTML",
        reply_markup=get_confirmation_keyboard("goal_delete", goal_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_goal_delete_"))
async def delete_goal_confirmed(callback: CallbackQuery):
    """Maqsadni o'chirish tasdiqlandi"""
    goal_id = int(callback.data.split("_")[3])
    
    success = await db.delete_goal(goal_id)
    
    if success:
        await callback.message.edit_text("✅ Maqsad o'chirildi!")
    else:
        await callback.message.edit_text("❌ Xatolik yuz berdi.")
    
    await callback.answer()

@router.callback_query(F.data.startswith("cancel_goal_delete_"))
async def delete_goal_cancelled(callback: CallbackQuery):
    """Maqsadni o'chirish bekor qilindi"""
    goal_id = int(callback.data.split("_")[3])
    
    # Maqsad ko'rinishiga qaytish
    await view_goal(callback)

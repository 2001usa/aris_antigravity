"""
Finance Handler
Moliyaviy operatsiyalar: ovozli xabar tahlili, statistika
"""
import os
from datetime import datetime, date, timedelta
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, Voice
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import Database
from services.ai_service import AIService
from utils.subscription import SubscriptionManager
import config

router = Router()
db = Database()
ai_service = AIService()
sub_manager = SubscriptionManager()

class FinanceStates(StatesGroup):
    """Moliyaviy operatsiya holatlari"""
    waiting_for_voice = State()

@router.message(F.text == "💰 Moliya")
async def finance_menu(message: Message):
    """Moliya menyusi"""
    await message.answer(
        "💰 <b>Moliyaviy Tahlil</b>\n\n"
        "🎤 Ovozli xabar yuboring, men uni tahlil qilaman.\n\n"
        "<b>Misol:</b>\n"
        "• 'Bugun non uchun 5000 so'm sarfladim'\n"
        "• 'Maosh oldim 3 million'\n"
        "• 'Taxi uchun 15000 to'ladim'\n\n"
        "Yoki matn shaklida ham yozishingiz mumkin.",
        parse_mode="HTML"
    )

@router.message(F.voice)
async def process_voice(message: Message):
    """Ovozli xabarni qayta ishlash"""
    user_id = message.from_user.id
    
    # Token limitini tekshirish
    can_use, used, limit = await sub_manager.check_token_limit(user_id)
    if not can_use:
        await message.answer(
            f"❌ Oylik limitingiz tugadi!\n\n"
            f"Ishlatilgan: {used:,} / {limit:,} token\n\n"
            f"Tarifni oshiring yoki keyingi oyni kuting."
        )
        return
    
    # Ovozni yuklab olish
    processing_msg = await message.answer("🎤 Ovozni qayta ishlamoqdaman...")
    
    try:
        # Ovoz faylini yuklab olish
        voice: Voice = message.voice
        file = await message.bot.get_file(voice.file_id)
        
        # Vaqtinchalik fayl nomi
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, f"{user_id}_{datetime.now().timestamp()}.ogg")
        
        # Faylni saqlash
        await message.bot.download_file(file.file_path, file_path)
        
        # Ovozni matnga o'girish
        text, whisper_tokens = await ai_service.transcribe_voice(file_path)
        
        # Faylni o'chirish
        if os.path.exists(file_path):
            os.remove(file_path)
        
        if not text:
            await processing_msg.edit_text("❌ Ovozni taniy olmadim. Iltimos, qaytadan urinib ko'ring.")
            return
        
        # DEBUG: Whisper natijasi
        print(f"🎤 DEBUG - Whisper transcription: '{text}'")
        
        await processing_msg.edit_text(f"✅ Tanildi: <i>{text}</i>\n\n⏳ Tahlil qilmoqdaman...", parse_mode="HTML")
        
        # AI tahlil
        analysis_list, analysis_tokens = await ai_service.analyze_transaction(text)
        
        # DEBUG: AI tahlil natijasi
        print(f"🤖 DEBUG - AI analysis result: {analysis_list}")
        
        if not analysis_list:
            await processing_msg.edit_text(
                f"✅ Tanildi: <i>{text}</i>\n\n"
                f"❌ Tahlil qilib bo'lmadi. Iltimos, aniqroq aytib bering.",
                parse_mode="HTML"
            )
            return
        
        # Token tracking
        total_tokens = whisper_tokens + analysis_tokens
        await db.track_ai_usage(user_id, "groq", total_tokens)
        
        # Har bir tranzaksiyani saqlash
        saved_count = 0
        results_text = ""
        
        for analysis in analysis_list:
            success = await db.add_transaction(
                user_id=user_id,
                trans_type=analysis.get("type", "expense"),
                amount=float(analysis.get("amount", 0)),
                category=analysis.get("category", "Boshqa"),
                description=analysis.get("description", "")
            )
            
            if success:
                saved_count += 1
                trans_type_emoji = "💵" if analysis["type"] == "income" else "💸"
                results_text += (
                    f"{trans_type_emoji} {analysis.get('type', 'expense')}: "
                    f"{analysis['amount']:,} so'm - {analysis['category']}\n"
                )
        
        if saved_count > 0:
            await processing_msg.edit_text(
                f"✅ <b>{saved_count} ta tranzaksiya saqlandi!</b>\n\n"
                f"{results_text}\n"
                f"🔢 Ishlatilgan: {total_tokens} token",
                parse_mode="HTML"
            )
        else:
            await processing_msg.edit_text("❌ Saqlashda xatolik yuz berdi.")
    
    except Exception as e:
        print(f"❌ Voice processing xato: {e}")
        await processing_msg.edit_text("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

# Menu tugmalari ro'yxati
MENU_BUTTONS = [
    "💰 Moliya", "📊 Statistika", "🎯 Maqsadlar", 
    "📝 Kundalik", "📈 Hisobotlar", "⚙️ Sozlamalar"
]

@router.message(
    F.text & 
    ~F.text.startswith("/") & 
    ~F.text.in_(MENU_BUTTONS) &
    (F.text.contains("*") | F.text.contains("so'm") | F.text.contains("som") | 
     F.text.contains("ming") | F.text.contains("million") | F.text.contains("k"))
)
async def process_text_transaction(message: Message):
    """Matnli moliyaviy xabarni qayta ishlash"""
    user_id = message.from_user.id
    text = message.text
    
    # Token limitini tekshirish
    can_use, used, limit = await sub_manager.check_token_limit(user_id)
    if not can_use:
        await message.answer(
            f"❌ Oylik limitingiz tugadi!\n\n"
            f"Ishlatilgan: {used:,} / {limit:,} token"
        )
        return
    
    processing_msg = await message.answer("⏳ Tahlil qilmoqdaman...")
    
    try:
        # AI tahlil
        analysis_list, tokens = await ai_service.analyze_transaction(text)
        
        if not analysis_list:
            await processing_msg.edit_text("❌ Tahlil qilib bo'lmadi. Iltimos, aniqroq yozing.")
            return
        
        # Token tracking
        await db.track_ai_usage(user_id, "groq", tokens)
        
        # Har bir tranzaksiyani saqlash
        saved_count = 0
        results_text = ""
        
        for analysis in analysis_list:
            success = await db.add_transaction(
                user_id=user_id,
                trans_type=analysis.get("type", "expense"),
                amount=float(analysis.get("amount", 0)),
                category=analysis.get("category", "Boshqa"),
                description=analysis.get("description", "")
            )
            
            if success:
                saved_count += 1
                trans_type_emoji = "💵" if analysis["type"] == "income" else "💸"
                results_text += (
                    f"{trans_type_emoji} {analysis.get('type', 'expense')}: "
                    f"{analysis['amount']:,} so'm - {analysis['category']}\n"
                )
        
        if saved_count > 0:
            await processing_msg.edit_text(
                f"✅ <b>{saved_count} ta tranzaksiya saqlandi!</b>\n\n"
                f"{results_text}",
                parse_mode="HTML"
            )
        else:
            await processing_msg.edit_text("❌ Saqlashda xatolik yuz berdi.")
    
    except Exception as e:
        print(f"❌ Text processing xato: {e}")
        await processing_msg.edit_text("❌ Xatolik yuz berdi.")

@router.message(F.text == "📊 Statistika")
async def show_statistics(message: Message):
    """Statistika ko'rsatish"""
    user_id = message.from_user.id
    
    # Joriy oy statistikasi
    stats = await db.get_statistics(user_id)
    
    if not stats:
        await message.answer("📊 Hozircha ma'lumot yo'q.")
        return
    
    # Kategoriya bo'yicha top 5
    top_categories = stats.get("expenses_by_category", [])[:5]
    categories_text = "\n".join([
        f"  • {cat['category']}: {cat['total']:,} so'm"
        for cat in top_categories
    ]) if top_categories else "  Ma'lumot yo'q"
    
    # Oxirgi 5 ta tranzaksiya
    recent = await db.get_transactions(user_id, limit=5)
    recent_text = ""
    for trans in recent:
        emoji = "💵" if trans["type"] == "income" else "💸"
        description = trans.get('description', '')
        desc_text = f" - {description}" if description else ""
        recent_text += f"{emoji} {trans['amount']:,} so'm ({trans['category']}){desc_text}\n"
    
    if not recent_text:
        recent_text = "Ma'lumot yo'q"
    
    await message.answer(
        f"📊 <b>Statistika</b> ({stats['period']['start']} - {stats['period']['end']})\n\n"
        f"💵 <b>Jami kirim:</b> {stats['total_income']:,} so'm\n"
        f"💸 <b>Jami chiqim:</b> {stats['total_expense']:,} so'm\n"
        f"💰 <b>Balans:</b> {stats['balance']:,} so'm\n\n"
        f"📁 <b>Top kategoriyalar:</b>\n{categories_text}\n\n"
        f"📝 <b>Oxirgi operatsiyalar:</b>\n{recent_text}",
        parse_mode="HTML"
    )

@router.message(Command("export"))
async def export_transactions(message: Message):
    """Tranzaksiyalarni CSV formatida export qilish"""
    from aiogram.types import BufferedInputFile
    from utils.export import export_transactions_to_csv, format_export_filename
    
    user_id = message.from_user.id
    
    processing_msg = await message.answer("📊 Tranzaksiyalarni tayyorlamoqdaman...")
    
    try:
        # Barcha tranzaksiyalarni olish (oxirgi 100 ta)
        transactions = await db.get_transactions(user_id, limit=100)
        
        if not transactions:
            await processing_msg.edit_text("📭 Hozircha tranzaksiyalar yo'q.")
            return
        
        # CSV yaratish
        csv_file = export_transactions_to_csv(transactions, message.from_user.first_name)
        filename = format_export_filename(user_id)
        
        # Faylni yuborish
        file = BufferedInputFile(csv_file.read(), filename=filename)
        
        await message.answer_document(
            file,
            caption=f"📊 <b>Tranzaksiyalar eksporti</b>\n\n"
                    f"📝 Jami: {len(transactions)} ta tranzaksiya\n"
                    f"📅 Sana: {date.today()}\n\n"
                    f"<i>Excel'da ochishingiz mumkin</i>",
            parse_mode="HTML"
        )
        
        await processing_msg.delete()
    
    except Exception as e:
        print(f"❌ Export xato: {e}")
        await processing_msg.edit_text("❌ Export qilishda xatolik yuz berdi.")

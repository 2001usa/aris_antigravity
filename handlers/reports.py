"""
Reports Handler
Hisobotlar va export (Standart+ tarif)
"""
from datetime import date, timedelta
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from database.db import Database
from services.ai_service import AIService
from services.export_service import ExportService
from utils.subscription import SubscriptionManager
from utils.keyboards import get_report_menu, get_export_menu, get_back_button

router = Router()
db = Database()
ai_service = AIService()
export_service = ExportService()
sub_manager = SubscriptionManager()

@router.message(F.text == "📈 Hisobotlar")
async def reports_menu(message: Message):
    """Hisobotlar menyusi"""
    user_id = message.from_user.id
    
    # Ruxsatni tekshirish
    has_access = await sub_manager.check_feature_access(user_id, "weekly_report")
    
    if not has_access:
        await message.answer(
            "🔒 <b>Hisobotlar funksiyasi</b>\n\n"
            "Bu funksiya faqat Standart va Premium tariflarda mavjud.\n\n"
            "Tarifni oshirish uchun /settings buyrug'ini yuboring.",
            parse_mode="HTML"
        )
        return
    
    await message.answer(
        "📈 <b>Hisobotlar</b>\n\n"
        "Qaysi hisobotni ko'rmoqchisiz?",
        parse_mode="HTML",
        reply_markup=get_report_menu()
    )

@router.callback_query(F.data == "report_weekly")
async def weekly_report(callback: CallbackQuery):
    """Haftalik hisobot"""
    user_id = callback.from_user.id
    
    # Oxirgi 7 kun
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    stats = await db.get_statistics(user_id, start_date, end_date)
    
    if not stats:
        await callback.answer("Ma'lumot topilmadi", show_alert=True)
        return
    
    # AI hisobot (agar token yetsa)
    can_use, used, limit = await sub_manager.check_token_limit(user_id)
    
    ai_report = ""
    if can_use:
        top_category = stats["expenses_by_category"][0]["category"] if stats["expenses_by_category"] else "Yo'q"
        
        report_data = {
            "total_income": stats["total_income"],
            "total_expense": stats["total_expense"],
            "balance": stats["balance"],
            "top_category": top_category
        }
        
        analysis, tokens = await ai_service.generate_report("weekly", report_data)
        
        if analysis:
            ai_report = f"\n\n🧠 <b>AI Tahlil:</b>\n{analysis}"
            await db.track_ai_usage(user_id, "weekly_report", tokens)
    
    # Kategoriyalar
    categories_text = "\n".join([
        f"  • {cat['category']}: {cat['total']:,} so'm"
        for cat in stats["expenses_by_category"][:5]
    ]) if stats["expenses_by_category"] else "  Ma'lumot yo'q"
    
    await callback.message.edit_text(
        f"📅 <b>Haftalik Hisobot</b>\n"
        f"({start_date} - {end_date})\n\n"
        f"💵 Jami kirim: {stats['total_income']:,} so'm\n"
        f"💸 Jami chiqim: {stats['total_expense']:,} so'm\n"
        f"💰 Balans: {stats['balance']:,} so'm\n\n"
        f"📁 <b>Top kategoriyalar:</b>\n{categories_text}"
        f"{ai_report}",
        parse_mode="HTML",
        reply_markup=get_back_button()
    )
    await callback.answer()

@router.callback_query(F.data == "report_monthly")
async def monthly_report(callback: CallbackQuery):
    """Oylik hisobot"""
    user_id = callback.from_user.id
    
    # Ruxsatni tekshirish
    has_access = await sub_manager.check_feature_access(user_id, "monthly_report")
    
    if not has_access:
        await callback.answer(
            "🔒 Oylik hisobot faqat Premium tarifda mavjud!",
            show_alert=True
        )
        return
    
    # Joriy oy
    stats = await db.get_statistics(user_id)
    
    if not stats:
        await callback.answer("Ma'lumot topilmadi", show_alert=True)
        return
    
    # AI hisobot
    can_use, used, limit = await sub_manager.check_token_limit(user_id)
    
    ai_report = ""
    if can_use:
        # Maqsadlar progressi
        goals = await db.get_goals(user_id)
        goals_progress = f"{len(goals)} ta maqsad" if goals else "Maqsad yo'q"
        
        report_data = {
            "total_income": stats["total_income"],
            "total_expense": stats["total_expense"],
            "balance": stats["balance"],
            "goals_progress": goals_progress
        }
        
        analysis, tokens = await ai_service.generate_report("monthly", report_data)
        
        if analysis:
            ai_report = f"\n\n🧠 <b>AI Tahlil:</b>\n{analysis}"
            await db.track_ai_usage(user_id, "monthly_report", tokens)
    
    # Kategoriyalar
    categories_text = "\n".join([
        f"  • {cat['category']}: {cat['total']:,} so'm"
        for cat in stats["expenses_by_category"][:5]
    ]) if stats["expenses_by_category"] else "  Ma'lumot yo'q"
    
    await callback.message.edit_text(
        f"📆 <b>Oylik Hisobot</b>\n"
        f"({stats['period']['start']} - {stats['period']['end']})\n\n"
        f"💵 Jami kirim: {stats['total_income']:,} so'm\n"
        f"💸 Jami chiqim: {stats['total_expense']:,} so'm\n"
        f"💰 Balans: {stats['balance']:,} so'm\n\n"
        f"📁 <b>Top kategoriyalar:</b>\n{categories_text}"
        f"{ai_report}",
        parse_mode="HTML",
        reply_markup=get_back_button()
    )
    await callback.answer()

@router.callback_query(F.data == "show_export")
async def show_export_menu(callback: CallbackQuery):
    """Export menyusini ko'rsatish"""
    user_id = callback.from_user.id
    
    # Ruxsatni tekshirish
    has_access = await sub_manager.check_feature_access(user_id, "excel_export")
    
    if not has_access:
        await callback.answer(
            "🔒 Export funksiyasi faqat Standart va Premium tariflarda mavjud!",
            show_alert=True
        )
        return
    
    await callback.message.edit_text(
        "📤 <b>Export</b>\n\n"
        "Qaysi formatda export qilmoqchisiz?",
        parse_mode="HTML",
        reply_markup=get_export_menu()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("export_"))
async def process_export(callback: CallbackQuery):
    """Export qilish"""
    export_type = callback.data.replace("export_", "")
    user_id = callback.from_user.id
    
    await callback.message.edit_text("⏳ Export qilmoqdaman...")
    
    try:
        # Ma'lumotlarni olish
        stats = await db.get_statistics(user_id)
        transactions = await db.get_transactions(user_id, limit=1000)
        
        month = date.today().strftime("%Y-%m")
        
        if export_type == "excel":
            # Excel export
            filepath = await export_service.export_to_excel(
                user_id, transactions, stats, month
            )
            
            # Faylni yuborish
            file = FSInputFile(filepath)
            await callback.message.answer_document(
                file,
                caption=f"📊 Excel hisobot ({month})"
            )
            
            await callback.message.edit_text(
                "✅ Excel hisobot tayyor!",
                reply_markup=get_back_button()
            )
        
        elif export_type == "pdf":
            # PDF export (hozircha text)
            filepath = await export_service.export_to_pdf(
                user_id, transactions, stats, month
            )
            
            # Faylni yuborish
            file = FSInputFile(filepath)
            await callback.message.answer_document(
                file,
                caption=f"📄 Hisobot ({month})\n\n⚠️ PDF versiya tez orada qo'shiladi"
            )
            
            await callback.message.edit_text(
                "✅ Hisobot tayyor!",
                reply_markup=get_back_button()
            )
    
    except Exception as e:
        print(f"❌ Export xato: {e}")
        await callback.message.edit_text(
            f"❌ Export qilishda xatolik: {str(e)}",
            reply_markup=get_back_button()
        )
    
    await callback.answer()

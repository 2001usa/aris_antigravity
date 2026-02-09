"""
ARIS Finance Bot
Shaxsiy moliyaviy yordamchi bot

Author: ARIS Team
Version: 1.0.0
"""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database.models import DatabaseModels
from handlers import start, finance, goals, diary, reports, settings

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Asosiy funksiya"""
    
    # API kalitlarni tekshirish
    if not config.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN topilmadi! .env faylni tekshiring.")
        return
    
    if not config.GROQ_API_KEY_1 and not config.GEMINI_API_KEY:
        logger.error("❌ AI API kalitlari topilmadi! Kamida bitta API key kerak.")
        return
    
    logger.info("🚀 ARIS Bot ishga tushmoqda...")
    
    # Database yaratish
    try:
        await DatabaseModels.create_tables(config.DATABASE_PATH)
        logger.info("✅ Database tayyor")
    except Exception as e:
        logger.error(f"❌ Database xato: {e}")
        return
    
    # Bot va Dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Routerlarni ro'yxatdan o'tkazish
    dp.include_router(start.router)
    dp.include_router(finance.router)
    dp.include_router(goals.router)
    dp.include_router(settings.router)
    dp.include_router(diary.router)
    dp.include_router(reports.router)
    
    logger.info("✅ Handlerlar yuklandi")
    
    # Botni ishga tushirish
    try:
        logger.info("✅ Bot ishga tushdi!")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Bot xato: {e}")
    finally:
        await bot.session.close()
        logger.info("👋 Bot to'xtatildi")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot to'xtatildi (Ctrl+C)")

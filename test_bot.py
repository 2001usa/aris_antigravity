"""
Test Script - ARIS Bot
Bot funksiyalarini test qilish
"""
import asyncio
from database.models import DatabaseModels
from database.db import Database
import config

async def test_database():
    """Database test"""
    print("Database test boshlandi...")
    
    # Database yaratish
    await DatabaseModels.create_tables(config.DATABASE_PATH)
    print("[OK] Database yaratildi")
    
    # Database operatsiyalari
    db = Database()
    
    # Test user qo'shish
    await db.add_user(12345, "test_user", "Test")
    print("[OK] Test user qo'shildi")
    
    # User olish
    user = await db.get_user(12345)
    print(f"[OK] User topildi: {user['username']}")
    
    # Tarif o'zgartirish
    await db.update_subscription(12345, "premium")
    user = await db.get_user(12345)
    print(f"[OK] Tarif o'zgartirildi: {user['subscription_tier']}")
    
    # Tranzaksiya qo'shish
    await db.add_transaction(12345, "expense", 50000, "Oziq-ovqat", "Test chiqim")
    await db.add_transaction(12345, "income", 1000000, "Maosh", "Test kirim")
    print("[OK] Tranzaksiyalar qo'shildi")
    
    # Statistika
    stats = await db.get_statistics(12345)
    print(f"[OK] Statistika: Kirim={stats['total_income']}, Chiqim={stats['total_expense']}")
    
    # Maqsad qo'shish
    await db.add_goal(12345, "Yangi telefon", 5000000)
    goals = await db.get_goals(12345)
    print(f"[OK] Maqsad qo'shildi: {goals[0]['title']}")
    
    print("\n[SUCCESS] Barcha testlar muvaffaqiyatli o'tdi!")

if __name__ == "__main__":
    asyncio.run(test_database())

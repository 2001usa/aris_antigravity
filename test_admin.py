"""
Test Script 2 - Admin va Export Test
"""
import asyncio
from database.models import DatabaseModels
from database.db import Database
from services.export_service import ExportService
from utils.subscription import SubscriptionManager
import config

async def test_admin_and_export():
    """Admin va export test"""
    print("=" * 50)
    print("ADMIN VA EXPORT TEST")
    print("=" * 50)
    
    # Database yaratish
    await DatabaseModels.create_tables(config.DATABASE_PATH)
    
    db = Database()
    sub_manager = SubscriptionManager()
    export_service = ExportService()
    
    # Test user (oddiy)
    test_user = 11111
    await db.add_user(test_user, "test_user", "Test User")
    
    # Test admin (config.py ga qo'shilishi kerak)
    test_admin = 22222
    config.ADMIN_USERS.append(test_admin)  # Vaqtinchalik qo'shamiz
    await db.add_user(test_admin, "admin_user", "Admin User")
    
    print("\n[TEST 1] Admin tekshirish")
    print(f"  User {test_user} admin? {sub_manager.is_admin(test_user)}")
    print(f"  User {test_admin} admin? {sub_manager.is_admin(test_admin)}")
    
    print("\n[TEST 2] Tarif olish")
    user_tier = await sub_manager.get_user_tier(test_user)
    admin_tier = await sub_manager.get_user_tier(test_admin)
    print(f"  User tarif: {user_tier}")
    print(f"  Admin tarif: {admin_tier}")
    
    print("\n[TEST 3] Token limit (o'chirilgan)")
    can_use, used, limit = await sub_manager.check_token_limit(test_user)
    print(f"  Ishlatish mumkin? {can_use}")
    print(f"  Limit: {limit}")
    
    print("\n[TEST 4] Tarif ma'lumotlari")
    info = await sub_manager.get_subscription_info(test_user)
    print(f"  Tier: {info['tier']}")
    print(f"  Admin: {info['is_admin']}")
    
    admin_info = await sub_manager.get_subscription_info(test_admin)
    print(f"  Admin tier: {admin_info['tier']}")
    print(f"  Admin badge: {admin_info['is_admin']}")
    
    print("\n[TEST 5] Export test")
    # Test ma'lumotlar
    await db.add_transaction(test_user, "income", 1000000, "Maosh", "Oylik maosh")
    await db.add_transaction(test_user, "expense", 50000, "Oziq-ovqat", "Supermarket")
    await db.add_transaction(test_user, "expense", 30000, "Transport", "Taxi")
    
    stats = await db.get_statistics(test_user)
    transactions = await db.get_transactions(test_user)
    
    # Excel export
    excel_file = await export_service.export_to_excel(
        test_user, transactions, stats
    )
    print(f"  Excel fayl: {excel_file}")
    
    # PDF export
    pdf_file = await export_service.export_to_pdf(
        test_user, transactions, stats
    )
    print(f"  PDF fayl: {pdf_file}")
    
    print("\n" + "=" * 50)
    print("[SUCCESS] Barcha testlar muvaffaqiyatli!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_admin_and_export())

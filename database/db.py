"""
Database Operations
Barcha database operatsiyalari
"""
import aiosqlite
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import config

class Database:
    """Database bilan ishlash uchun klass"""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
    
    # ============ USER OPERATIONS ============
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None) -> bool:
        """Yangi foydalanuvchi qo'shish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT OR IGNORE INTO users (user_id, username, first_name) 
                       VALUES (?, ?, ?)""",
                    (user_id, username, first_name)
                )
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ User qo'shishda xato: {e}")
            return False
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Foydalanuvchi ma'lumotlarini olish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM users WHERE user_id = ?", (user_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return dict(row)
                    return None
        except Exception as e:
            print(f"❌ User olishda xato: {e}")
            return None
    
    async def update_subscription(self, user_id: int, tier: str) -> bool:
        """Tarif o'zgartirish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """UPDATE users SET subscription_tier = ?, updated_at = ? 
                       WHERE user_id = ?""",
                    (tier, datetime.now(), user_id)
                )
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Tarif o'zgartirishda xato: {e}")
            return False
    
    # ============ TRANSACTION OPERATIONS ============
    
    async def add_transaction(
        self, 
        user_id: int, 
        trans_type: str, 
        amount: float, 
        category: str, 
        description: str = None,
        trans_date: date = None
    ) -> bool:
        """Tranzaksiya qo'shish"""
        if trans_date is None:
            trans_date = date.today()
        
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO transactions 
                       (user_id, type, amount, category, description, date) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (user_id, trans_type, amount, category, description, trans_date)
                )
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Tranzaksiya qo'shishda xato: {e}")
            return False
    
    async def get_transactions(
        self, 
        user_id: int, 
        limit: int = 10,
        trans_type: str = None,
        start_date: date = None,
        end_date: date = None
    ) -> List[Dict]:
        """Tranzaksiyalar ro'yxatini olish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                
                query = "SELECT * FROM transactions WHERE user_id = ?"
                params = [user_id]
                
                if trans_type:
                    query += " AND type = ?"
                    params.append(trans_type)
                
                if start_date:
                    query += " AND date >= ?"
                    params.append(start_date)
                
                if end_date:
                    query += " AND date <= ?"
                    params.append(end_date)
                
                query += " ORDER BY date DESC, created_at DESC LIMIT ?"
                params.append(limit)
                
                async with db.execute(query, params) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Tranzaksiyalar olishda xato: {e}")
            return []
    
    async def get_statistics(
        self, 
        user_id: int,
        start_date: date = None,
        end_date: date = None
    ) -> Dict:
        """Statistika olish"""
        if start_date is None:
            start_date = date(date.today().year, date.today().month, 1)
        if end_date is None:
            end_date = date.today()
        
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Jami kirim
                async with db.execute(
                    """SELECT COALESCE(SUM(amount), 0) as total 
                       FROM transactions 
                       WHERE user_id = ? AND type = 'income' 
                       AND date BETWEEN ? AND ?""",
                    (user_id, start_date, end_date)
                ) as cursor:
                    total_income = (await cursor.fetchone())[0]
                
                # Jami chiqim
                async with db.execute(
                    """SELECT COALESCE(SUM(amount), 0) as total 
                       FROM transactions 
                       WHERE user_id = ? AND type = 'expense' 
                       AND date BETWEEN ? AND ?""",
                    (user_id, start_date, end_date)
                ) as cursor:
                    total_expense = (await cursor.fetchone())[0]
                
                # Kategoriya bo'yicha chiqimlar
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    """SELECT category, SUM(amount) as total 
                       FROM transactions 
                       WHERE user_id = ? AND type = 'expense' 
                       AND date BETWEEN ? AND ?
                       GROUP BY category 
                       ORDER BY total DESC""",
                    (user_id, start_date, end_date)
                ) as cursor:
                    expenses_by_category = [dict(row) for row in await cursor.fetchall()]
                
                return {
                    "total_income": total_income,
                    "total_expense": total_expense,
                    "balance": total_income - total_expense,
                    "expenses_by_category": expenses_by_category,
                    "period": {
                        "start": start_date.isoformat(),
                        "end": end_date.isoformat()
                    }
                }
        except Exception as e:
            print(f"❌ Statistika olishda xato: {e}")
            return {}
    
    # ============ GOAL OPERATIONS ============
    
    async def add_goal(
        self, 
        user_id: int, 
        title: str, 
        target_amount: float,
        deadline: date = None
    ) -> bool:
        """Maqsad qo'shish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO goals (user_id, title, target_amount, deadline) 
                       VALUES (?, ?, ?, ?)""",
                    (user_id, title, target_amount, deadline)
                )
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Maqsad qo'shishda xato: {e}")
            return False
    
    async def get_goals(self, user_id: int, status: str = "active") -> List[Dict]:
        """Maqsadlar ro'yxatini olish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    """SELECT * FROM goals 
                       WHERE user_id = ? AND status = ? 
                       ORDER BY created_at DESC""",
                    (user_id, status)
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Maqsadlar olishda xato: {e}")
            return []
    
    async def update_goal_progress(self, goal_id: int, amount: float) -> bool:
        """Maqsad progressini yangilash"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """UPDATE goals 
                       SET current_amount = current_amount + ?, updated_at = ? 
                       WHERE id = ?""",
                    (amount, datetime.now(), goal_id)
                )
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Maqsad yangilashda xato: {e}")
            return False
    
    # ============ DIARY OPERATIONS ============
    
    async def add_diary(
        self, 
        user_id: int, 
        content: str,
        ai_analysis: str = None,
        diary_date: date = None
    ) -> bool:
        """Kundalik qo'shish"""
        if diary_date is None:
            diary_date = date.today()
        
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO diary (user_id, content, ai_analysis, date) 
                       VALUES (?, ?, ?, ?)""",
                    (user_id, content, ai_analysis, diary_date)
                )
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Kundalik qo'shishda xato: {e}")
            return False
    
    async def get_diary(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Kundalik yozuvlarini olish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    """SELECT * FROM diary 
                       WHERE user_id = ? 
                       ORDER BY date DESC, created_at DESC 
                       LIMIT ?""",
                    (user_id, limit)
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Kundalik olishda xato: {e}")
            return []
    
    # ============ AI USAGE TRACKING ============
    
    async def track_ai_usage(self, user_id: int, service: str, tokens: int) -> bool:
        """AI ishlatilishini kuzatish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO ai_usage (user_id, service, tokens_used, date) 
                       VALUES (?, ?, ?, ?)""",
                    (user_id, service, tokens, date.today())
                )
                
                # User'ning umumiy tokenlarini yangilash
                await db.execute(
                    """UPDATE users 
                       SET tokens_used = tokens_used + ? 
                       WHERE user_id = ?""",
                    (tokens, user_id)
                )
                
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ AI usage tracking xato: {e}")
            return False
    
    async def get_monthly_tokens(self, user_id: int) -> int:
        """Oylik ishlatilgan tokenlar"""
        try:
            first_day = date(date.today().year, date.today().month, 1)
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(
                    """SELECT COALESCE(SUM(tokens_used), 0) as total 
                       FROM ai_usage 
                       WHERE user_id = ? AND date >= ?""",
                    (user_id, first_day)
                ) as cursor:
                    return (await cursor.fetchone())[0]
        except Exception as e:
            print(f"❌ Token olishda xato: {e}")
            return 0
    
    # ============ ADMIN OPERATIONS ============
    
    async def get_total_users(self) -> int:
        """Jami foydalanuvchilar soni"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT COUNT(*) FROM users")
                result = await cursor.fetchone()
                return result[0] if result else 0
        except:
            return 0
    
    async def get_active_users_today(self) -> int:
        """Bugun aktiv foydalanuvchilar"""
        try:
            today = date.today().isoformat()
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "SELECT COUNT(DISTINCT user_id) FROM transactions WHERE date = ?",
                    (today,)
                )
                result = await cursor.fetchone()
                return result[0] if result else 0
        except:
            return 0
    
    async def get_total_transactions(self) -> int:
        """Jami tranzaksiyalar soni"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT COUNT(*) FROM transactions")
                result = await cursor.fetchone()
                return result[0] if result else 0
        except:
            return 0
    
    async def get_admin_statistics(self) -> dict:
        """Admin uchun batafsil statistika"""
        from datetime import timedelta
        today = date.today().isoformat()
        week_ago = (date.today() - timedelta(days=7)).isoformat()
        
        try:
            async with aiosqlite.connect(self.db_path) as db:
                stats = {}
                
                # Foydalanuvchilar
                cursor = await db.execute("SELECT COUNT(*) FROM users")
                stats['total_users'] = (await cursor.fetchone())[0]
                
                cursor = await db.execute(
                    "SELECT COUNT(*) FROM users WHERE created_at >= ?", (today,)
                )
                stats['new_users_today'] = (await cursor.fetchone())[0]
                
                cursor = await db.execute(
                    "SELECT COUNT(DISTINCT user_id) FROM transactions WHERE date >= ?",
                    (week_ago,)
                )
                stats['active_week'] = (await cursor.fetchone())[0]
                
                # Tranzaksiyalar
                cursor = await db.execute("SELECT COUNT(*) FROM transactions")
                stats['total_transactions'] = (await cursor.fetchone())[0]
                
                cursor = await db.execute(
                    "SELECT COUNT(*) FROM transactions WHERE date = ?", (today,)
                )
                stats['transactions_today'] = (await cursor.fetchone())[0]
                
                cursor = await db.execute(
                    "SELECT COUNT(*) FROM transactions WHERE date >= ?", (week_ago,)
                )
                stats['transactions_week'] = (await cursor.fetchone())[0]
                
                # Moliyaviy
                cursor = await db.execute(
                    "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'income'"
                )
                stats['total_income'] = (await cursor.fetchone())[0]
                
                cursor = await db.execute(
                    "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'expense'"
                )
                stats['total_expense'] = (await cursor.fetchone())[0]
                
                # Maqsadlar
                cursor = await db.execute("SELECT COUNT(*) FROM goals")
                stats['total_goals'] = (await cursor.fetchone())[0]
                
                cursor = await db.execute(
                    "SELECT COUNT(*) FROM goals WHERE current_amount >= target_amount"
                )
                stats['completed_goals'] = (await cursor.fetchone())[0]
                
                # AI usage
                cursor = await db.execute(
                    "SELECT COALESCE(SUM(tokens_used), 0) FROM ai_usage WHERE service = 'groq'"
                )
                stats['groq_usage'] = (await cursor.fetchone())[0]
                
                cursor = await db.execute(
                    "SELECT COALESCE(SUM(tokens_used), 0) FROM ai_usage WHERE service = 'gemini'"
                )
                stats['gemini_usage'] = (await cursor.fetchone())[0]
                
                return stats
        except Exception as e:
            print(f"❌ Admin stats xato: {e}")
            return {
                'total_users': 0, 'new_users_today': 0, 'active_week': 0,
                'total_transactions': 0, 'transactions_today': 0, 'transactions_week': 0,
                'total_income': 0, 'total_expense': 0,
                'total_goals': 0, 'completed_goals': 0,
                'groq_usage': 0, 'gemini_usage': 0
            }
    
    async def get_all_users(self, limit: int = 50) -> list:
        """Barcha foydalanuvchilar ro'yxati"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    """SELECT user_id, username, first_name, subscription_tier, 
                       tokens_used, created_at
                    FROM users
                    ORDER BY created_at DESC
                    LIMIT ?""",
                    (limit,)
                )
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"❌ Users list xato: {e}")
            return []


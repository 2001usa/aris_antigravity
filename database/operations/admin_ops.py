"""
Admin Operations
Admin va AI tracking bilan bog'liq barcha database operatsiyalari
"""
import aiosqlite
from datetime import date, timedelta
from typing import List, Dict


class AdminOperations:
    """Admin operatsiyalari"""
    
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
    
    async def get_all_users(self, limit: int = 50) -> List[Dict]:
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

"""
User Operations
Foydalanuvchi bilan bog'liq barcha database operatsiyalari
"""
import aiosqlite
from datetime import datetime
from typing import Optional, Dict


class UserOperations:
    """Foydalanuvchi operatsiyalari"""
    
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
    
    async def update_user_settings(
        self, 
        user_id: int, 
        currency: str = None, 
        theme: str = None, 
        phone: str = None, 
        email: str = None,
        notifications_enabled: bool = None
    ) -> bool:
        """Foydalanuvchi sozlamalarini yangilash"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                updates = []
                params = []
                
                if currency is not None:
                    updates.append("currency = ?")
                    params.append(currency)
                
                if theme is not None:
                    updates.append("theme = ?")
                    params.append(theme)
                
                if phone is not None:
                    updates.append("phone = ?")
                    params.append(phone)
                
                if email is not None:
                    updates.append("email = ?")
                    params.append(email)
                
                if notifications_enabled is not None:
                    updates.append("notifications_enabled = ?")
                    params.append(1 if notifications_enabled else 0)
                
                if not updates:
                    return False
                
                updates.append("updated_at = ?")
                params.append(datetime.now())
                params.append(user_id)
                
                query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
                await db.execute(query, params)
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Sozlamalar yangilashda xato: {e}")
            return False

"""
Goal Operations
Maqsad bilan bog'liq barcha database operatsiyalari
"""
import aiosqlite
from datetime import datetime, date
from typing import List, Dict, Optional


class GoalOperations:
    """Maqsad operatsiyalari"""
    
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
    
    async def get_goal_by_id(self, goal_id: int) -> Optional[Dict]:
        """ID bo'yicha maqsadni olish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM goals WHERE id = ?", (goal_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return dict(row)
                    return None
        except Exception as e:
            print(f"❌ Maqsad olishda xato: {e}")
            return None
    
    async def update_goal(self, goal_id: int, title: str = None, target_amount: float = None, deadline: date = None) -> bool:
        """Maqsadni tahrirlash"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                updates = []
                params = []
                
                if title is not None:
                    updates.append("title = ?")
                    params.append(title)
                
                if target_amount is not None:
                    updates.append("target_amount = ?")
                    params.append(target_amount)
                
                if deadline is not None:
                    updates.append("deadline = ?")
                    params.append(deadline)
                
                if not updates:
                    return False
                
                updates.append("updated_at = ?")
                params.append(datetime.now())
                params.append(goal_id)
                
                query = f"UPDATE goals SET {', '.join(updates)} WHERE id = ?"
                await db.execute(query, params)
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Maqsad tahrirlashda xato: {e}")
            return False
    
    async def delete_goal(self, goal_id: int) -> bool:
        """Maqsadni o'chirish"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
                await db.commit()
                return True
        except Exception as e:
            print(f"❌ Maqsad o'chirishda xato: {e}")
            return False

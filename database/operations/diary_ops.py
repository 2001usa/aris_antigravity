"""
Diary Operations
Kundalik bilan bog'liq barcha database operatsiyalari
"""
import aiosqlite
from datetime import date
from typing import List, Dict


class DiaryOperations:
    """Kundalik operatsiyalari"""
    
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

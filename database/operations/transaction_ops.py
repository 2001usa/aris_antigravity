"""
Transaction Operations
Tranzaksiya bilan bog'liq barcha database operatsiyalari
"""
import aiosqlite
from datetime import date
from typing import List, Dict


class TransactionOperations:
    """Tranzaksiya operatsiyalari"""
    
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

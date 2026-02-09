"""
Export Utilities
Tranzaksiyalarni CSV/Excel formatida export qilish
"""
import csv
import io
from datetime import date
from typing import List, Dict


def export_transactions_to_csv(transactions: List[Dict], user_name: str = "User") -> io.BytesIO:
    """
    Tranzaksiyalarni CSV formatida export qilish
    Returns: BytesIO object (faylni yuborish uchun)
    """
    output = io.StringIO()
    
    # CSV writer
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Sana', 'Turi', 'Summa', 'Kategoriya', 'Tavsif'])
    
    # Data
    for trans in transactions:
        writer.writerow([
            trans.get('date', ''),
            'Kirim' if trans.get('type') == 'income' else 'Chiqim',
            trans.get('amount', 0),
            trans.get('category', ''),
            trans.get('description', '')
        ])
    
    # StringIO'dan BytesIO'ga o'tkazish
    output.seek(0)
    bytes_output = io.BytesIO(output.getvalue().encode('utf-8-sig'))  # BOM bilan UTF-8
    bytes_output.seek(0)
    
    return bytes_output


def format_export_filename(user_id: int, start_date: date = None, end_date: date = None) -> str:
    """Export fayl nomini yaratish"""
    if start_date and end_date:
        return f"transactions_{user_id}_{start_date}_{end_date}.csv"
    else:
        return f"transactions_{user_id}_{date.today()}.csv"

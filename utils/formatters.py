"""
Formatters Utility
Ma'lumotlarni formatlash uchun yordamchi funksiyalar
"""
from datetime import date, datetime, timedelta
from typing import Optional

def format_currency(amount: float, currency: str = "UZS") -> str:
    """
    Valyutani formatlash
    
    Args:
        amount: Summa
        currency: Valyuta kodi (UZS, USD, RUB)
    
    Returns:
        Formatlangan summa
    """
    symbols = {
        "UZS": "so'm",
        "USD": "$",
        "RUB": "₽"
    }
    
    symbol = symbols.get(currency, "so'm")
    
    if currency == "UZS":
        return f"{amount:,.0f} {symbol}"
    else:
        return f"{symbol}{amount:,.2f}"


def format_date(date_obj: Optional[date], format_type: str = "short") -> str:
    """
    Sanani formatlash
    
    Args:
        date_obj: Sana obyekti
        format_type: Format turi (short, long, relative)
    
    Returns:
        Formatlangan sana
    """
    if date_obj is None:
        return "Muddatsiz"
    
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj).date()
        except:
            return date_obj
    
    if format_type == "short":
        return date_obj.strftime("%d.%m.%Y")
    elif format_type == "long":
        months = {
            1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel",
            5: "May", 6: "Iyun", 7: "Iyul", 8: "Avgust",
            9: "Sentyabr", 10: "Oktyabr", 11: "Noyabr", 12: "Dekabr"
        }
        return f"{date_obj.day} {months[date_obj.month]} {date_obj.year}"
    elif format_type == "relative":
        return format_relative_date(date_obj)
    
    return str(date_obj)


def format_relative_date(date_obj: date) -> str:
    """
    Nisbiy sanani formatlash (bugun, kecha, 3 kun oldin)
    
    Args:
        date_obj: Sana obyekti
    
    Returns:
        Nisbiy sana
    """
    today = date.today()
    delta = (date_obj - today).days
    
    if delta == 0:
        return "Bugun"
    elif delta == 1:
        return "Ertaga"
    elif delta == -1:
        return "Kecha"
    elif delta > 0:
        return f"{delta} kundan keyin"
    else:
        return f"{abs(delta)} kun oldin"


def format_deadline(deadline: Optional[date]) -> str:
    """
    Muddatni formatlash (rang bilan)
    
    Args:
        deadline: Muddat sanasi
    
    Returns:
        Formatlangan muddat
    """
    if deadline is None:
        return "⏳ Muddatsiz"
    
    if isinstance(deadline, str):
        try:
            deadline = datetime.fromisoformat(deadline).date()
        except:
            return f"📅 {deadline}"
    
    today = date.today()
    delta = (deadline - today).days
    
    if delta < 0:
        return f"🔴 Muddati o'tgan ({format_date(deadline)})"
    elif delta == 0:
        return f"🟡 Bugun ({format_date(deadline)})"
    elif delta <= 7:
        return f"🟠 {delta} kun ({format_date(deadline)})"
    elif delta <= 30:
        return f"🟢 {delta} kun ({format_date(deadline)})"
    else:
        return f"🟢 {format_date(deadline)}"


def format_percentage(current: float, target: float) -> str:
    """
    Foizni formatlash
    
    Args:
        current: Joriy qiymat
        target: Maqsad qiymat
    
    Returns:
        Formatlangan foiz
    """
    if target == 0:
        return "0%"
    
    percentage = (current / target) * 100
    
    if percentage >= 100:
        return f"✅ {percentage:.0f}%"
    elif percentage >= 75:
        return f"🟢 {percentage:.1f}%"
    elif percentage >= 50:
        return f"🟡 {percentage:.1f}%"
    elif percentage >= 25:
        return f"🟠 {percentage:.1f}%"
    else:
        return f"🔴 {percentage:.1f}%"


def format_progress_bar(current: float, target: float, length: int = 10) -> str:
    """
    Progress bar yaratish
    
    Args:
        current: Joriy qiymat
        target: Maqsad qiymat
        length: Bar uzunligi
    
    Returns:
        Progress bar
    """
    if target == 0:
        return "░" * length
    
    percentage = min(current / target, 1.0)
    filled = int(percentage * length)
    
    return "█" * filled + "░" * (length - filled)

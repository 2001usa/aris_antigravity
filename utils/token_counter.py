"""
Token Counter Utility
Oddiy matn uchun token hisoblash
"""

def estimate_tokens(text: str, language: str = "uzbek") -> int:
    """
    Matn uchun taxminiy token sonini hisoblash
    
    Args:
        text: Tahlil qilinadigan matn
        language: Til (uzbek, english, russian)
    
    Returns:
        Taxminiy token soni
    """
    if not text:
        return 0
    
    # Har xil tillar uchun koeffitsiyentlar
    # 1 token ≈ N harf
    coefficients = {
        "uzbek": 3.5,      # O'zbek tili uchun
        "english": 4.0,    # Ingliz tili uchun
        "russian": 3.2,    # Rus tili uchun
    }
    
    coef = coefficients.get(language.lower(), 3.5)
    
    # Belgilar sonini hisoblash
    char_count = len(text)
    
    # Bo'sh joylarni hisobga olish
    word_count = len(text.split())
    
    # Taxminiy hisoblash: (harflar / koeffitsiyent) + (so'zlar / 2)
    estimated = (char_count / coef) + (word_count / 2)
    
    return int(estimated)


def format_token_info(text: str, language: str = "uzbek") -> str:
    """
    Token ma'lumotini formatlangan ko'rinishda qaytarish
    
    Args:
        text: Tahlil qilinadigan matn
        language: Til
    
    Returns:
        Formatlangan ma'lumot
    """
    tokens = estimate_tokens(text, language)
    char_count = len(text)
    word_count = len(text.split())
    
    return (
        f"📊 <b>Token Tahlili:</b>\n\n"
        f"🔢 Taxminiy tokenlar: <b>{tokens:,}</b>\n"
        f"📝 Harflar: {char_count:,}\n"
        f"📖 So'zlar: {word_count:,}\n\n"
        f"<i>💡 Bu taxminiy qiymat. Haqiqiy token soni AI modelga bog'liq.</i>"
    )

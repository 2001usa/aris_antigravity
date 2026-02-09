"""
Subscription Management
Tarif tizimi va ruxsatlarni tekshirish
"""
from typing import Dict
import config
from database.db import Database

class SubscriptionManager:
    """Tarif tizimini boshqarish"""
    
    def __init__(self):
        self.db = Database()
    
    def is_admin(self, user_id: int) -> bool:
        """User admin ekanligini tekshirish"""
        return user_id in config.ADMIN_USERS
    
    async def get_user_tier(self, user_id: int) -> str:
        """
        Foydalanuvchining tarifini olish
        Admin bo'lsa Premium, aks holda Standart
        """
        if self.is_admin(user_id):
            return config.SubscriptionTier.PREMIUM
        
        user = await self.db.get_user(user_id)
        if user:
            return user.get("subscription_tier", config.SubscriptionTier.STANDARD)
        return config.SubscriptionTier.STANDARD
    
    async def check_feature_access(self, user_id: int, feature: str) -> bool:
        """
        Foydalanuvchining funksiyaga ruxsati bormi tekshirish
        
        Args:
            user_id: Foydalanuvchi ID
            feature: Funksiya nomi (masalan: "diary", "excel_export")
        
        Returns:
            True agar ruxsat bo'lsa, False aks holda
        """
        tier = await self.get_user_tier(user_id)
        features = config.SUBSCRIPTION_FEATURES.get(tier, {})
        
        return features.get(feature, False)
    
    async def check_token_limit(self, user_id: int) -> tuple[bool, int, int]:
        """
        Foydalanuvchining token limitini tekshirish
        HOZIRCHA O'CHIRILGAN - config.ENABLE_LIMITS = False
        
        Returns:
            (limit_ichida, ishlatilgan, limit)
        """
        # Agar limitlar o'chirilgan bo'lsa, har doim True qaytarish
        if not config.ENABLE_LIMITS:
            return True, 0, 999999999
        
        tier = await self.get_user_tier(user_id)
        limit = config.SUBSCRIPTION_LIMITS.get(tier, 0)
        
        used = await self.db.get_monthly_tokens(user_id)
        
        return used < limit, used, limit
    
    async def get_subscription_info(self, user_id: int) -> Dict:
        """
        Foydalanuvchining tarif ma'lumotlari
        
        Returns:
            {
                "tier": "standard",
                "tier_name": "💙 Standart",
                "is_admin": False,
                "tokens_used": 1000,
                "tokens_limit": 1890000,
                "tokens_remaining": 1889000,
                "features": {...}
            }
        """
        tier = await self.get_user_tier(user_id)
        is_admin = self.is_admin(user_id)
        limit = config.SUBSCRIPTION_LIMITS.get(tier, 0)
        used = await self.db.get_monthly_tokens(user_id) if config.ENABLE_LIMITS else 0
        
        return {
            "tier": tier,
            "tier_name": config.SUBSCRIPTION_NAMES.get(tier, ""),
            "is_admin": is_admin,
            "tokens_used": used,
            "tokens_limit": limit,
            "tokens_remaining": max(0, limit - used),
            "features": config.SUBSCRIPTION_FEATURES.get(tier, {})
        }
    
    def get_tier_description(self, tier: str) -> str:
        """Tarif tavsifi"""
        descriptions = {
            config.SubscriptionTier.STANDARD: (
                "💙 <b>Standart Tarif</b>\n\n"
                "✅ Ovozli moliyaviy tahlil\n"
                "✅ Statistika\n"
                "✅ Maqsadlar\n"
                "✅ Kundalik\n"
                "✅ Haftalik hisobot\n"
                "✅ Excel/PDF export\n\n"
                "📊 Limit: 1,890,000 token/oy\n"
                "⚠️ Hozircha limitlar o'chirilgan"
            ),
            config.SubscriptionTier.PREMIUM: (
                "💎 <b>Premium Tarif (Admin)</b>\n\n"
                "✅ Standart funksiyalar\n"
                "✅ Kundalik AI tahlili\n"
                "✅ Oylik hisobot\n"
                "✅ Batafsil tahlillar\n"
                "✅ Admin panel\n\n"
                "📊 Limit: 2,400,000 token/oy\n"
                "⚠️ Hozircha limitlar o'chirilgan"
            )
        }
        return descriptions.get(tier, "")
    
    async def format_subscription_status(self, user_id: int) -> str:
        """Tarif holatini formatlash"""
        info = await self.get_subscription_info(user_id)
        if not info:
            return "❌ Ma'lumot topilmadi"
        
        admin_badge = "👑 ADMIN" if info["is_admin"] else ""
        
        if not config.ENABLE_LIMITS:
            return (
                f"{info['tier_name']} {admin_badge}\n\n"
                f"⚠️ <b>Test rejimi:</b> Limitlar o'chirilgan\n"
                f"💡 Barcha funksiyalar cheklovsiz ishlaydi"
            )
        
        percentage = (info["tokens_used"] / info["tokens_limit"] * 100) if info["tokens_limit"] > 0 else 0
        
        # Progress bar
        filled = int(percentage / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        return (
            f"{info['tier_name']} {admin_badge}\n\n"
            f"📊 Ishlatilgan: {info['tokens_used']:,} / {info['tokens_limit']:,}\n"
            f"[{bar}] {percentage:.1f}%\n\n"
            f"💡 Qolgan: {info['tokens_remaining']:,} token"
        )

import secrets
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

class ReferralManager:
    """Менеджер реферальной системы"""
    
    def __init__(self):
        self.referral_days = 1  # Дней за каждого приглашенного
    
    async def generate_referral_code(self, session: AsyncSession, user_id: int) -> str:
        """Генерация реферального кода"""
        from models.referral import ReferralCode
        
        # Проверяем существующий код
        existing_code = await session.get(ReferralCode, user_id)
        if existing_code:
            return existing_code.code
        
        # Генерируем новый код
        code = secrets.token_urlsafe(8)
        referral_code = ReferralCode(
            user_id=user_id,
            code=code,
            is_active=True
        )
        session.add(referral_code)
        await session.commit()
        
        return code
    
    async def get_referral_link(self, session: AsyncSession, user_id: int) -> str:
        """Получение реферальной ссылки"""
        code = await self.generate_referral_code(session, user_id)
        return f"https://t.me/your_bot_username?start={code}"
    
    async def process_referral(self, session: AsyncSession, new_user_id: int, code: str):
        """Обработка реферального кода"""
        from models.referral import ReferralCode, Referral
        from bot.subscription_manager import SubscriptionManager
        
        # Находим код
        referral_code = await session.execute(
            f"SELECT * FROM referral_codes WHERE code = '{code}'"
        )
        referral_code = referral_code.first()
        
        if not referral_code:
            return
        
        referrer_id = referral_code.user_id
        
        # Проверяем, не сам ли пользователь использует свой код
        if referrer_id == new_user_id:
            return
        
        # Проверяем, не использовался ли уже код этим пользователем
        existing_ref = await session.execute(
            f"SELECT * FROM referrals WHERE referred_user_id = {new_user_id}"
        )
        if existing_ref.first():
            return
        
        # Создаем запись о реферале
        referral = Referral(
            referrer_id=referrer_id,
            referred_user_id=new_user_id,
            referral_code=code
        )
        session.add(referral)
        
        # Продлеваем подписку пригласившему
        subscription_manager = SubscriptionManager()
        await subscription_manager.activate_subscription(
            session, referrer_id, self.referral_days
        )
        
        await session.commit()
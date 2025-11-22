from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from core.yookassa_client import YooKassaClient

class SubscriptionManager:
    """Менеджер подписок"""
    
    def __init__(self):
        self.yookassa = YooKassaClient()
    
    async def register_user(self, session: AsyncSession, user_id: int, username: str):
        """Регистрация нового пользователя"""
        from models.user import User
        from models.subscription import Subscription
        
        user = await session.get(User, user_id)
        if not user:
            user = User(
                id=user_id,
                username=username,
                created_at=datetime.now()
            )
            session.add(user)
            
            # Создание пробной подписки
            subscription = Subscription(
                user_id=user_id,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=settings.TRIAL_DAYS),
                is_trial=True,
                is_active=True
            )
            session.add(subscription)
            await session.commit()
    
    async def check_subscription(self, session: AsyncSession, user_id: int) -> bool:
        """Проверка активной подписки"""
        from models.subscription import Subscription
        
        subscription = await session.get(Subscription, user_id)
        if not subscription or not subscription.is_active:
            return False
        
        if subscription.end_date < datetime.now():
            subscription.is_active = False
            await session.commit()
            return False
        
        return True
    
    async def create_subscription(self, session: AsyncSession, user_id: int) -> Optional[str]:
        """Создание подписки через YooKassa"""
        from models.user import User
        
        user = await session.get(User, user_id)
        if not user:
            return None
        
        payment = await self.yookassa.create_payment(
            user_id=user_id,
            amount=settings.SUBSCRIPTION_PRICE,
            description="Подписка на бота Алина на 30 дней"
        )
        
        if payment and payment.get("confirmation_url"):
            return payment["confirmation_url"]
        
        return None
    
    async def activate_subscription(self, session: AsyncSession, user_id: int, days: int = 30):
        """Активация подписки"""
        from models.subscription import Subscription
        
        subscription = await session.get(Subscription, user_id)
        now = datetime.now()
        
        if subscription:
            # Если подписка еще активна, продлеваем
            if subscription.end_date > now:
                subscription.end_date += timedelta(days=days)
            else:
                subscription.end_date = now + timedelta(days=days)
            
            subscription.is_trial = False
            subscription.is_active = True
        else:
            # Создаем новую подписку
            subscription = Subscription(
                user_id=user_id,
                start_date=now,
                end_date=now + timedelta(days=days),
                is_trial=False,
                is_active=True
            )
            session.add(subscription)
        
        await session.commit()
    
    async def get_subscription_status(self, session: AsyncSession, user_id: int) -> str:
        """Получение статуса подписки"""
        from models.subscription import Subscription
        
        subscription = await session.get(Subscription, user_id)
        if not subscription:
            return "У тебя нет активной подписки 😔\nИспользуй /subscribe чтобы оформить!"
        
        if not subscription.is_active:
            return "Твоя подписка неактивна 💫\nИспользуй /subscribe чтобы возобновить!"
        
        days_left = (subscription.end_date - datetime.now()).days
        
        if subscription.is_trial:
            return f"У тебя пробный период! Осталось {days_left} дней 🌸"
        else:
            return f"Твоя подписка активна! Осталось {days_left} дней 💖"
from aiogram import types
from aiogram.filters import BaseFilter
from datetime import datetime, timedelta
from collections import defaultdict

class SubscriptionFilter(BaseFilter):
    """Фильтр проверки подписки"""
    
    async def __call__(self, message: types.Message) -> bool:
        from core.database import get_db
        from bot.subscription_manager import SubscriptionManager
        
        user_id = message.from_user.id
        
        async for session in get_db():
            subscription_manager = SubscriptionManager()
            has_access = await subscription_manager.check_subscription(session, user_id)
        
        if not has_access:
            from ai.personality import Personality
            await message.answer(Personality.get_trial_ended_message())
            return False
        
        return True

class RateLimitFilter(BaseFilter):
    """Фильтр ограничения частоты сообщений"""
    
    def __init__(self):
        self.user_messages = defaultdict(list)
        self.max_messages = 10  # Максимум сообщений в минуту
        self.time_window = 60   # Окно в секундах
    
    async def __call__(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        now = datetime.now()
        
        # Очищаем старые сообщения
        self.user_messages[user_id] = [
            msg_time for msg_time in self.user_messages[user_id]
            if now - msg_time < timedelta(seconds=self.time_window)
        ]
        
        # Проверяем лимит
        if len(self.user_messages[user_id]) >= self.max_messages:
            await message.answer(
                "Слишком много сообщений! Пожалуйста, подожди немного перед следующим сообщением ⏳"
            )
            return False
        
        # Добавляем текущее сообщение
        self.user_messages[user_id].append(now)
        return True
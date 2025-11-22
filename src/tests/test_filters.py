import pytest
from datetime import datetime, timedelta
from bot.filters import RateLimitFilter

@pytest.mark.asyncio
async def test_rate_limit_filter():
    """Тест фильтра ограничения частоты сообщений"""
    filter = RateLimitFilter()
    
    # Создаем mock сообщение
    class MockMessage:
        def __init__(self, user_id):
            self.from_user = type('User', (), {'id': user_id})()
    
    message = MockMessage(123)
    
    # Первые 10 сообщений должны проходить
    for i in range(10):
        result = await filter(message)
        assert result == True
    
    # 11-е сообщение должно быть заблокировано
    result = await filter(message)
    assert result == False

@pytest.mark.asyncio
async def test_rate_limit_reset():
    """Тест сброса ограничения частоты"""
    filter = RateLimitFilter()
    
    class MockMessage:
        def __init__(self, user_id):
            self.from_user = type('User', (), {'id': user_id})()
    
    message = MockMessage(124)
    
    # Имитируем старые сообщения
    old_time = datetime.now() - timedelta(seconds=61)
    filter.user_messages[124] = [old_time] * 10
    
    # Новое сообщение должно пройти (старые удаляются)
    result = await filter(message)
    assert result == True
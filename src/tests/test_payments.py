import pytest
from unittest.mock import AsyncMock, patch
from bot.subscription_manager import SubscriptionManager

@pytest.mark.asyncio
async def test_payment_creation():
    """Тест создания платежа"""
    manager = SubscriptionManager()
    
    with patch('core.yookassa_client.YooKassaClient.create_payment') as mock_payment:
        mock_payment.return_value = {
            "id": "test_payment_id",
            "status": "pending", 
            "confirmation_url": "https://example.com/pay"
        }
        
        result = await manager.create_subscription(AsyncMock(), 123)
        
        assert result == "https://example.com/pay"
        mock_payment.assert_called_once()

@pytest.mark.asyncio
async def test_payment_activation(db_session):
    """Тест активации подписки после платежа"""
    manager = SubscriptionManager()
    
    # Создаем пользователя
    from models.user import User
    user = User(id=123, username="test_user")
    db_session.add(user)
    await db_session.commit()
    
    # Активируем подписку
    await manager.activate_subscription(db_session, 123, days=30)
    
    # Проверяем
    from models.subscription import Subscription
    subscription = await db_session.get(Subscription, 123)
    assert subscription is not None
    assert subscription.is_active == True
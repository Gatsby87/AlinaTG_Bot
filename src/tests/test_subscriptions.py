import pytest
from datetime import datetime, timedelta
from bot.subscription_manager import SubscriptionManager

@pytest.mark.asyncio
async def test_subscription_creation(db_session):
    """Тест создания подписки"""
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
    assert subscription.end_date > datetime.now()

@pytest.mark.asyncio
async def test_subscription_check(db_session):
    """Тест проверки подписки"""
    manager = SubscriptionManager()
    
    # Создаем пользователя с активной подпиской
    from models.user import User
    from models.subscription import Subscription
    user = User(id=124, username="test_user2")
    subscription = Subscription(
        user_id=124,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        is_active=True
    )
    db_session.add(user)
    db_session.add(subscription)
    await db_session.commit()
    
    # Проверяем подписку
    has_access = await manager.check_subscription(db_session, 124)
    assert has_access == True

@pytest.mark.asyncio
async def test_expired_subscription(db_session):
    """Тест просроченной подписки"""
    manager = SubscriptionManager()
    
    # Создаем пользователя с просроченной подпиской
    from models.user import User
    from models.subscription import Subscription
    user = User(id=125, username="test_user3")
    subscription = Subscription(
        user_id=125,
        start_date=datetime.now() - timedelta(days=60),
        end_date=datetime.now() - timedelta(days=30),
        is_active=True
    )
    db_session.add(user)
    db_session.add(subscription)
    await db_session.commit()
    
    # Проверяем подписку
    has_access = await manager.check_subscription(db_session, 125)
    assert has_access == False
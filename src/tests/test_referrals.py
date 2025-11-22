import pytest
from bot.referral_manager import ReferralManager

@pytest.mark.asyncio
async def test_referral_link_generation(db_session):
    """Тест генерации реферальной ссылки"""
    manager = ReferralManager()
    
    # Создаем пользователя
    from models.user import User
    user = User(id=123, username="test_user")
    db_session.add(user)
    await db_session.commit()
    
    link = await manager.get_referral_link(db_session, 123)
    
    assert link.startswith("https://t.me/")
    assert "start=" in link

@pytest.mark.asyncio
async def test_referral_processing(db_session):
    """Тест обработки реферала"""
    manager = ReferralManager()
    
    # Создаем реферера
    from models.user import User
    from models.subscription import Subscription
    referrer = User(id=123, username="referrer")
    referrer_sub = Subscription(
        user_id=123,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=10),
        is_active=True
    )
    db_session.add(referrer)
    db_session.add(referrer_sub)
    
    # Создаем реферальный код
    from models.referral import ReferralCode
    ref_code = ReferralCode(user_id=123, code="test_code")
    db_session.add(ref_code)
    await db_session.commit()
    
    # Обрабатываем реферала
    await manager.process_referral(db_session, 124, "test_code")
    
    # Проверяем, что подписка продлилась
    subscription = await db_session.get(Subscription, 123)
    assert subscription.end_date > datetime.now() + timedelta(days=10)
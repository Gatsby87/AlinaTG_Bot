from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.yookassa_client import YooKassaClient
from bot.subscription_manager import SubscriptionManager

router = APIRouter()

@router.post("/webhook/yookassa")
async def yookassa_webhook(request: Request):
    """Webhook для обработки уведомлений от YooKassa"""
    data = await request.json()
    
    # Проверяем тип события
    event = data.get('event')
    if event != 'payment.succeeded':
        return {"status": "ignored"}
    
    # Получаем данные платежа
    payment_object = data.get('object', {})
    payment_id = payment_object.get('id')
    status = payment_object.get('status')
    metadata = payment_object.get('metadata', {})
    user_id = metadata.get('user_id')
    
    if not user_id or status != 'succeeded':
        raise HTTPException(status_code=400, detail="Invalid payment data")
    
    async for session in get_db():
        # Активируем подписку
        subscription_manager = SubscriptionManager()
        await subscription_manager.activate_subscription(session, user_id, days=30)
        
        # Сохраняем информацию о платеже
        from models.payment import Payment
        payment = Payment(
            user_id=user_id,
            payment_id=payment_id,
            amount=float(payment_object['amount']['value']),
            currency=payment_object['amount']['currency'],
            status=status,
            description=payment_object.get('description', ''),
            paid_at=payment_object.get('captured_at')
        )
        session.add(payment)
        await session.commit()
    
    return {"status": "success"}
from yookassa import Configuration, Payment
from yookassa.domain.models import Amount
import uuid
from core.config import settings

class YooKassaClient:
    """Клиент для работы с YooKassa"""
    
    def __init__(self):
        Configuration.account_id = settings.YOOKASSA_SHOP_ID
        Configuration.secret_key = settings.YOOKASSA_API_KEY
    
    async def create_payment(self, user_id: int, amount: float, description: str) -> dict:
        """Создание платежа"""
        idempotence_key = str(uuid.uuid4())
        
        payment = Payment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"https://t.me/your_bot_username"
            },
            "capture": True,
            "description": description,
            "metadata": {
                "user_id": user_id
            }
        }, idempotence_key)
        
        return {
            "id": payment.id,
            "status": payment.status,
            "confirmation_url": payment.confirmation.confirmation_url
        }
    
    async def check_payment_status(self, payment_id: str) -> str:
        """Проверка статуса платежа"""
        payment = Payment.find_one(payment_id)
        return payment.status
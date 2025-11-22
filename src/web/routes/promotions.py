from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from core.database import get_db
from web.auth import get_current_user
from models.user import User
from bot.subscription_manager import SubscriptionManager

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")

@router.get("/promotions")
async def promotions_page(
    request: Request,
    current_user: str = Depends(get_current_user)
):
    """Страница промо-кампаний"""
    context = {
        "request": request
    }
    
    return templates.TemplateResponse("promotions.html", context)

@router.post("/promotions/add_days")
async def add_days_to_all(
    days: int = Form(...),
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Добавление дней подписки всем активным пользователям"""
    subscription_manager = SubscriptionManager()
    
    # Получаем всех пользователей с активными подписками
    from models.subscription import Subscription
    from sqlalchemy import select
    
    result = await db.execute(
        select(Subscription)
        .where(Subscription.is_active == True)
    )
    subscriptions = result.scalars().all()
    
    for subscription in subscriptions:
        subscription.end_date += timedelta(days=days)
    
    await db.commit()
    
    return {"status": "success", "message": f"Добавлено {days} дней для {len(subscriptions)} пользователей"}
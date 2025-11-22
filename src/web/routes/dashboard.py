from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from datetime import datetime, timedelta

from core.database import get_db
from web.auth import get_current_user
from models.user import User
from models.subscription import Subscription
from models.payment import Payment

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")

@router.get("/dashboard")
async def dashboard(
    request: Request,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Главная панель администратора"""
    
    # Статистика пользователей
    total_users = await db.scalar(select(func.count(User.id)))
    active_subscriptions = await db.scalar(
        select(func.count(Subscription.user_id))
        .where(Subscription.is_active == True)
        .where(Subscription.end_date > datetime.now())
    )
    trial_users = await db.scalar(
        select(func.count(Subscription.user_id))
        .where(Subscription.is_trial == True)
        .where(Subscription.is_active == True)
    )
    
    # Статистика платежей
    total_revenue = await db.scalar(
        select(func.sum(Payment.amount))
        .where(Payment.status == 'succeeded')
    ) or 0
    
    # Активность за последние 7 дней
    week_ago = datetime.now() - timedelta(days=7)
    new_users_week = await db.scalar(
        select(func.count(User.id))
        .where(User.created_at >= week_ago)
    )
    
    context = {
        "request": request,
        "total_users": total_users,
        "active_subscriptions": active_subscriptions,
        "trial_users": trial_users,
        "total_revenue": total_revenue,
        "new_users_week": new_users_week
    }
    
    return templates.TemplateResponse("dashboard.html", context)
from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from core.database import get_db
from web.auth import get_current_user
from models.user import User
from models.subscription import Subscription

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")

@router.get("/users")
async def users_list(
    request: Request,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Список пользователей"""
    users = await db.execute(
        select(User, Subscription)
        .join(Subscription, User.id == Subscription.user_id, isouter=True)
    )
    users_data = users.all()
    
    context = {
        "request": request,
        "users": users_data
    }
    
    return templates.TemplateResponse("users.html", context)

@router.post("/users/{user_id}/block")
async def block_user(
    user_id: int,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Блокировка пользователя"""
    user = await db.get(User, user_id)
    if user:
        user.is_blocked = True
        await db.commit()
    
    return {"status": "success"}

@router.post("/users/{user_id}/unblock")
async def unblock_user(
    user_id: int,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Разблокировка пользователя"""
    user = await db.get(User, user_id)
    if user:
        user.is_blocked = False
        await db.commit()
    
    return {"status": "success"}
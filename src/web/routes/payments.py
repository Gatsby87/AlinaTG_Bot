from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import get_db
from web.auth import get_current_user
from models.payment import Payment

router = APIRouter()
templates = Jinja2Templates(directory="src/web/templates")

@router.get("/payments")
async def payments_list(
    request: Request,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Список платежей"""
    payments = await db.execute(select(Payment))
    payments_data = payments.scalars().all()
    
    context = {
        "request": request,
        "payments": payments_data
    }
    
    return templates.TemplateResponse("payments.html", context)
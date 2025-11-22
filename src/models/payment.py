from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from core.database import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_id = Column(String(100), unique=True)
    amount = Column(Float)
    currency = Column(String(10), default="RUB")
    status = Column(String(50))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    paid_at = Column(DateTime, nullable=True)
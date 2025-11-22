from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    first_name = Column(String(100))
    memory_summary = Column(Text, default="")
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    referral_codes = relationship("ReferralCode", back_populates="user")
    referrals_made = relationship("Referral", back_populates="referrer", foreign_keys="Referral.referrer_id")
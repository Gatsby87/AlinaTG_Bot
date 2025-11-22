from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class ReferralCode(Base):
    __tablename__ = "referral_codes"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    code = Column(String(50), unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationship
    user = relationship("User", back_populates="referral_codes")

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    referrer_id = Column(Integer, ForeignKey("users.id"))
    referred_user_id = Column(Integer, ForeignKey("users.id"))
    referral_code = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    referrer = relationship("User", back_populates="referrals_made", foreign_keys=[referrer_id])
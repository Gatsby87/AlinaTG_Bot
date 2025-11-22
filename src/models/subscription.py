from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    is_trial = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Relationship
    user = relationship("User", back_populates="subscription")
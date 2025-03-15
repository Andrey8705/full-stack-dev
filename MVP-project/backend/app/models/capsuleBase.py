from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base import Base
import uuid

class Capsule(Base):
    __tablename__ = "capsules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    unlock_date = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="capsules")
    create_date = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=True)
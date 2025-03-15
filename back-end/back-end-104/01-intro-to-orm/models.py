from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from models.base import Base

class Capsule(Base):
    __tablename__ = "capsules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unlock_date = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="capsules")
    create_date = Column(DateTime, default=datetime.utcnow)

    #Пример из уже написанного кода
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    avatar_url = Column(String, nullable=True)

    
    capsules = relationship("Capsule", back_populates="user")
    tokens = relationship("Token", back_populates='user')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from fastapi import Depends
from models.base import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session_local():
    yield SessionLocal()

def get_db(db: Session = Depends(get_session_local)):
    try:
        yield db
    finally:
        db.close()

def create_db():
    Base.metadata.create_all(bind=engine)
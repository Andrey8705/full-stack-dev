from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from models.userBase import User
from database.db_setup import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



def create_refresh_token(user_id: int, db: Session):
    from models.tokenBase import Token
    token_id = str(uuid4())  # Генерируем уникальный идентификатор
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = { "id": token_id, "exp": expires_at}
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Сохраняем токен как активный
    new_token = Token(token_id= token_id, user_id= user_id, expires_at= expires_at)
    db.add(new_token)
    db.commit()
    return refresh_token

def verify_acces_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

def check_user_role(token_data: dict, required_role: str):
    user_role = token_data.get("role")
    if user_role != required_role:
        raise HTTPException(status_code = 403, detail = f"Acces denied: requires {required_role} role")
    
def check_user_and_capsule_user_id(user_data, capsule_user_id):
    if user_data != capsule_user_id:
        raise HTTPException(status_code= 403, detail= "Acces denied!")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user  # Возвращает объект пользователя

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
from database.db_setup import SessionLocal
from uuid import uuid4
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jose import jwt
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))



def create_refresh_token(user_id: int, db: SessionLocal):
    from models.tokenBase import Token
    token_id = str(uuid4())  # Генерируем уникальный идентификатор
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = { "id": token_id, "exp": expires_at}
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Сохраняем токен как активный
    new_token = Token(token_id= token_id, user_id= user_id, expires_at= expires_at)
    db.add(new_token)
    db.commit()
    #active_refresh_tokens[token_id] = {"email": email, "expires_at": expire}
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
        raise HTTPException(status_code= 403, detail= "Acces debied: it's not your capsule!")

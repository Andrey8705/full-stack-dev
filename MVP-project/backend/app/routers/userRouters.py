from fastapi import APIRouter, HTTPException, Depends
from database.db_setup import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models.userBaseModel import UserRegister, UserLogin
import bcrypt
from fastapi.security import OAuth2PasswordBearer
import os
from models.userBase import User
from models.tokenBase import Token
from datetime import datetime
from jose import jwt
from models.tokenBaseModel import TokenRefreshRequest
from dotenv import load_dotenv
from functions.mainLogic import create_access_token, create_refresh_token, check_user_role, verify_acces_token


load_dotenv()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
DATABASE_URL = os.getenv("DATABASE_URL")

@router.post("/auth/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return JSONResponse(status_code=400, content={"message": "email already registered"})
    if len(user.password) < 6:
        return JSONResponse(content={"error": "Password too short"})

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(content={"message": f"User {new_user.name} successfully registered"})

@router.post("/auth/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
        return JSONResponse(status_code=400, content={"message": "Incorrect email or password"})
    
    access_token = create_access_token({"sub": existing_user.email, "role": existing_user.role, "name": existing_user.name, "id": existing_user.id})
    refresh_token = create_refresh_token(existing_user.id, db)
    
    return JSONResponse(content={
        "message": f"User {existing_user.name} successfully logged in",
        "access_token": access_token,
        "refresh_token": refresh_token
    })

@router.get("/admin/get/users/all")
def get_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    users = db.query(User).all()
    return users

@router.get("/admin/get/users/{id}")
def get_user_by_id(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/admin/edit/users/{id}")
def update_user_data(id: int, user_data: UserRegister,role: str = None, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from models.userBase import User  # Перемещаем импорт сюда
    user_data_from_token = verify_acces_token(token)
    check_user_role(user_data_from_token, "admin")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_data.name
    user.email = user_data.email
    user.role = role
    db.commit()
    return user

@router.delete("/admin/delete/users/{id}")
def delete_user(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"{user.name} successfully deleted"}

@router.get("/me")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_data = verify_acces_token(token)
    user_id = user_data.get("id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "avatar_url": user.avatar_url
    }


@router.post("/auth/refresh")
def refresh_access_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    refresh_token = request.refresh_token
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token is required")
    try:
        payload = jwt.decode(refresh_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        token_id = payload.get("id")

        token = db.query(Token).filter(Token.token_id == token_id).first()
        if not token or token.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
        db.delete(token)
        db.commit()
        
        # Генерируем новый Access Token и Refresh Token
        user = db.query(User).filter(User.id == token.user_id).first()
        new_access_token = create_access_token({"sub": user.email, "role": user.role, "id": user.id})
        new_refresh_token = create_refresh_token(user.id, db)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.post("/auth/logout")
def logout_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    payload = verify_acces_token(token)
    user_id = payload.get("id")
    
    db.query(Token).filter(Token.user_id == user_id).delete()
    db.commit()
    return {"message": "Successfully logged out"}
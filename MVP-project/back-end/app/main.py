from email import message
from time import strptime
from tkinter import SE
import token
from fastapi import FastAPI, HTTPException, Depends
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr, BaseModel, Field
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

active_refresh_tokens = {}

app = FastAPI()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Capsule(Base):
    __tablename__ = "capsules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unlock_date = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="capsules")
    create_date = Column(DateTime, default=datetime.utcnow)

User.capsules = relationship("Capsule", back_populates= "user")

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="tokens")

User.tokens = relationship("Token", back_populates="user")

Base.metadata.create_all(bind= engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "it_is_my_hard_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class CapsuleCreate(BaseModel):
    name: str = Field(description= "Название капсулы")
    unlock_date: str = Field(description= "Дата когда капсула будет открыта. Формат *ГГГГ.ММ.ДД*")
    message: str = Field(description= "Короткое сообщение для получателя.")

class UserRegister(BaseModel):
    name: str
    password: str
    email: EmailStr
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


def create_refresh_token(user_id: int, db: SessionLocal):
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

@app.post("/auth/register")  #Эндпроинт для регистрации нового пользователя и присвоения ему id
def register_user(user: UserRegister, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first() #Если почта уже занята - выводим ошибку.
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(user.password) < 6: #Если пароль короче 6 символов - выводим ошибку.
        return {"error": "Password too short"}

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(name= user.name, email= user.email, password= hashed_password, role= user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {new_user.name} successfully registered"}

@app.post("/auth/login")
def login_user(user: UserLogin, db: SessionLocal = Depends(get_db)):
    # Проверяем пользователя
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Удаляем все активные Refresh Tokens для этого пользователя
    #tokens_to_revoke = [key for key, value in active_refresh_tokens.items() if value["email"] == user.email]
    #for token_id in tokens_to_revoke:
    #    del active_refresh_tokens[token_id]
    
    # Генерируем новые токены
    access_token = create_access_token({"sub": existing_user.email, "role": existing_user.role, "name": existing_user.name, "id": existing_user.id})
    refresh_token = create_refresh_token(existing_user.id, db)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@app.get("/admin/get/users/all") #Эндпоинт вывода всех пользователей
def get_users(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    users = db.query(User).all()
    return users

@app.get("/admin/get/users/{id}", summary="Get user by id") #Эндпоинт выводящий пользователя по id
def get_user_by_id(id:int, token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/admin/edit/users/{id}", summary="Update user data") #Эндпоинт для обновления информации о пользователе
def update_user_data(id:int, user_data: UserRegister, token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    payload = verify_acces_token(token)
    check_user_role(payload, "admin")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    db.commit()
    return user

@app.delete("/admin/delete/users/{id}", summary="Delete user") #Эндпоинт для удаления пользователя
def delete_user(id:int, token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return{"message":f"{user.name} successfuly deleted"}

@app.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    return {
        "email": user_data["sub"],
        "name": user_data["name"],
        "role": user_data["role"]
    }

@app.get("/admin")
def admin_route(token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    return {"message": "Welcome, Admin! You have full acces!"}

@app.get("/user/user-resource")
def user_resourse(token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "user")
    return {"message": f"Welcome, {user_data["name"]}! This resource for users only."}

@app.post("/auth/refresh")
def refresh_access_token(refresh_token: str, db: SessionLocal = Depends(get_db)):
    try:
        # Проверяем валидность токена
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
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
    
@app.post ("/auth/logout")
def logout_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    payload = verify_acces_token(token)
    user_id = payload.get("id")
    
    db.query(Token).filter(Token.user_id == user_id).delete()
    db.commit()
    return {"message": "Successfully logged out"}

@app.post ("/capsule/create-capsule/")
def create_capsule(capsule: CapsuleCreate, db: SessionLocal = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    create_date_now = datetime.utcnow()
    new_capsule = Capsule(
        name = capsule.name,
        create_date = create_date_now,
        unlock_date = datetime.strptime(capsule.unlock_date, "%Y-%m-%d"),
        message = capsule.message,
        user_id = user_data["id"]
    )
    db.add(new_capsule)
    db.commit()
    db.refresh(new_capsule)    
    return {"message": f"Capsule {new_capsule.name} successfuly created."}

@app.get("/admin/get/capsule/all")
def get_capsules(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    capsules = db.query(Capsule).all()

    return capsules

@app.get("/admin/get/capsule/{id}")
def get_capsule_by_id(id : int, token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    user_data =  verify_acces_token(token)
    capsule = db.query(Capsule).filter(Capsule.id == id).first()
    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")
    
    check_user_and_capsule_user_id(user_data["id"], capsule.user_id)

    return capsule

@app.delete("/admin/delete/capsule/{id}")
def delete_capsule(id: int, token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    capsule = db.query(Capsule).filter(Capsule.id == id).first()
    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")
    db.delete(capsule)
    db.commit()

    return{"message":f"{capsule["name"]} successfuly deleted"}

@app.put("/admin/edit/capsule/{id}")
def edit_capsule(id: int, capsule_data: CapsuleCreate, token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    capsule = db.query(Capsule).filter(Capsule.id == id).first()
    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")
    
    capsule.name = capsule_data.name
    capsule.unlock_date = capsule_data.unlock_date
    capsule.message = capsule_data.message
    db.commit()
    return capsule

    
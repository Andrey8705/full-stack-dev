from sys import deactivate_stack_trampoline
from tkinter import NO
import token
from fastapi import FastAPI, HTTPException
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr, BaseModel, Field
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
from pathlib import Path

active_refresh_tokens = {}

app = FastAPI()

SECRET_KEY = "it_is_my_hard_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class CapsuleCreate(BaseModel):
    name: str = Field(description= "Название капсулы")
    unlock_data: str = Field(description= "Дата когда капсула будет открыта. Формат *ГГГГ.ММ.ДД*")
    message: str = Field(description= "Короткое сообщение для получателя.")

class UserRegister(BaseModel):
    name: str
    password: str
    email: EmailStr
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

users = []
capsules = []

def create_refresh_token(email: EmailStr) -> str:
    token_id = str(uuid4())  # Генерируем уникальный идентификатор
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": email, "id": token_id, "exp": expire}
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # Сохраняем токен как активный
    active_refresh_tokens[token_id] = {"email": email, "expires_at": expire}
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
def register_user(user: UserRegister):
    if any(u["email"] == user.email for u in users): #Если почта уже занята - выводим ошибку.
        return {"error": "Email already exists"}
    if len(user.password) < 6: #Если пароль короче 6 символов - выводим ошибку.
        return {"error": "Password too short"}

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = {
        "id" : len(users) + 1,
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
    }
    users.append(new_user)
    return {"message": f"User {new_user["name"]} created successfully!"}

@app.post("/auth/login")
def login_user(user: UserLogin):
    # Проверяем пользователя
    existing_user = next((u for u in users if u["email"] == user.email), None)
    if not user or not bcrypt.checkpw(user.password.encode('utf-8'), existing_user["password"].encode('utf-8')):
        return {"error": "Invalid email or password"}
    
    # Удаляем все активные Refresh Tokens для этого пользователя
    tokens_to_revoke = [key for key, value in active_refresh_tokens.items() if value["email"] == user.email]
    for token_id in tokens_to_revoke:
        del active_refresh_tokens[token_id]
    
    # Генерируем новые токены
    access_token = create_access_token({"sub": existing_user["email"], "role": existing_user["role"], "name": existing_user["name"], "id": existing_user["id"]})
    refresh_token = create_refresh_token(existing_user["email"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@app.get("/admin/get/users/all") #Эндпоинт вывода всех пользователей
def get_users(token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    return users

@app.get("/admin/get/users/{id}", summary="Get user by id") #Эндпоинт выводящий пользователя по id
def get_user_by_id(id:int, token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/admin/edit/users/{id}", summary="Update user data") #Эндпоинт для обновления информации о пользователе
def update_user_data(id:int, user_data: UserRegister, token: str = Depends(oauth2_scheme)):
    payload = verify_acces_token(token)
    check_user_role(payload, "admin")
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["name"] = user_data.name
    user["email"] = user_data.email
    user["role"] = user_data.role
    return user

@app.delete("/admin/delete/users/{id}", summary="Delete user") #Эндпоинт для удаления пользователя
def delete_user(id:int, token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    global users #Изменяем глобальную переменную(словарь с начальными пользователями)
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users = [t for t in users if t["id"] != id]
    return{"message":f"{user["name"]} successfuly deleted"}

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
def refresh_access_token(refresh_token: str):
    try:
        # Проверяем валидность токена
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_id = payload.get("id")
        email = payload.get("sub")
        
        # Проверяем, что токен активен
        if token_id not in active_refresh_tokens:
            raise HTTPException(status_code=401, detail="Refresh token is not active")
        
        # Удаляем старый токен из списка активных
        del active_refresh_tokens[token_id]
        
        # Генерируем новый Access Token и Refresh Token
        new_access_token = create_access_token({"sub": email})
        new_refresh_token = create_refresh_token(email)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@app.post ("/auth/logout")
def logout_user(token: str = Depends(oauth2_scheme)):
        payload = verify_acces_token(token)
        email = payload.get("sub")
        tokens_to_revoke = [key for key, value in active_refresh_tokens.items() if value["email"] == email]
        for token_id in tokens_to_revoke:
            del active_refresh_tokens[token_id]

        return {"message": "Successfully logged out"}

@app.post ("/capsule/create-capsule/")
def create_capsule(capsule: CapsuleCreate, token: str = Depends(oauth2_scheme)):
    payload = verify_acces_token(token)
    user_data = payload
    new_capsule = {
        "id": len(capsules) + 1,
        "name": capsule.name,
        "user_id": user_data["id"],
        "create_data": datetime.utcnow().strftime("%Y.%m.%d"),
        "unlock_data": datetime.strptime(capsule.unlock_data, "%Y.%m.%d").strftime("%Y.%m.%d"),
        "message": capsule.message
    }
    capsules.append(new_capsule)
    create_date = datetime.strptime(new_capsule["create_data"], "%Y.%m.%d").date()
    unlock_date = datetime.strptime(new_capsule["unlock_data"], "%Y.%m.%d").date()
    days_to_open = (unlock_date - create_date).days

    return {"message": f"Capsule {new_capsule["name"]} successfuly created. Capsule id - {new_capsule["id"]}. Capsule will be opened in {days_to_open} days"}

@app.get("/admin/get/capsule/all")
def get_capsules(token: str = Depends(oauth2_scheme)):

    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")

    return capsules

@app.get("/admin/get/capsule/{id}")
def get_capsule_by_id(id : int, token: str = Depends(oauth2_scheme)):
    payload =  verify_acces_token(token)
    user_data = payload

    capsule = next((capsule for capsule in capsules if capsule["id"] == id), None)
    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")
    
    check_user_and_capsule_user_id(user_data, capsule["user_id"])

    return capsule

@app.delete("/admin/delete/capsule/{id}")
def delete_capsule(id: int, token: str = Depends(oauth2_scheme)):
    payload = verify_acces_token(token)
    user_data = payload
    check_user_role(user_data, "admin")
    global capsules

    capsule = next((capsule for capsule in capsules if capsule["id"] == id), None)
    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")
    capsules = [t for t in capsules if t["id"] != id]

    return{"message":f"{capsule["name"]} successfuly deleted"}

@app.put("/admin/edit/capsule/{id}")
def edit_capsule(id: int, capsule_data: CapsuleCreate, token: str = Depends(oauth2_scheme)):
    payload = verify_acces_token(token)
    user_data = payload
    check_user_role(user_data, "admin")
    global capsules

    capsule = next((capsule for capsule in capsules if capsule["id"] == id), None)
    if not capsule:
        raise HTTPException(status_code=404, detail="Capsule not found")
    capsules = [t for t in capsules if t["id"] != id]
    capsule["name"] = capsule_data.name
    capsule["unlock_data"] = capsule_data.unlock_data
    capsule["message"] = capsule_data.message

    return capsule

    

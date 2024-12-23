import email
import token
from fastapi import FastAPI, HTTPException
import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

SECRET_KEY = "it_is_my_hard_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

users = [ #Начальный словарь с пользователями
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "role": "user"}
]

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_acces_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def create_acces_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

def check_user_role(token_data: dict, required_role: str):
    user_role = token_data.get("role")
    if user_role != required_role:
        raise HTTPException(status_code = 403, detail = f"Acces denied: requires {required_role} role")

@app.post("/auth/register")  #Эндпроинт для регистрации нового пользователя и присвоения ему id
def register_user(name: str, email: EmailStr, password: str, role: str = "user"):
    if any(u["email"] == email for u in users): #Если почта уже занята - выводим ошибку.
        return {"error": "Email already exists"}
    if len(password) < 6: #Если пароль короче 6 символов - выводим ошибку.
        return {"error": "Password too short"}

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = {
        "id" : len(users) + 1,
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
    }
    users.append(new_user)
    return {"message": f"User {new_user["name"]} created successfully!"}

@app.post("/auth/login")#Эндпоинт авторизации пользователя
def login_user(email: EmailStr, password: str):
    user = next((u for u in users if u["email"] == email), None)
    token = create_acces_token({"sub": user["email"], "role": user["role"], "name": user["name"]})
    refresh_token = create_refresh_token({"sub": user["email"]})
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):#Сравнение хэшей паролей
        return {"error": "Invalid email or password"}
    return {"refresh_token": refresh_token, "acces_token": token,"message": f"Welcome, {user["name"]}"}

@app.get("/users") #Эндпоинт вывода всех пользователей
def get_users(token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    return users

@app.get("/users/{id}", summary="Get user by id") #Эндпоинт выводящий пользователя по id
def get_user_by_id(id:int, token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{id}", summary="Update user data") #Эндпоинт для обновления информации о пользователе
def update_user_data(id:int, user_name:str, email:EmailStr, role:str, token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "admin")
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["name"] = user_name
    user["email"] = email
    user["role"] = role
    return user

@app.delete("/users/{id}", summary="Delete user") #Эндпоинт для удаления пользователя
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

@app.get("/user-resource")
def user_resourse(token: str = Depends(oauth2_scheme)):
    user_data = verify_acces_token(token)
    check_user_role(user_data, "user")
    return {"message": f"Welcome, {user_data["name"]}! This resource for users only."}

@app.post("/auth/refresh")
def refresh_acces_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token,SECRET_KEY,algorithms=ALGORITHM)
        email = payload.get("sub")
        name = payload.get("name")
        role = payload.get("role")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        new_acces_token = create_acces_token({"sub": email, "name": name,"role": role})
        return {"access_token": new_acces_token}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
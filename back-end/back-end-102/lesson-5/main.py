from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import bcrypt

app = FastAPI()

users = [ #Начальный словарь с пользователями
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "role": "user"}
]

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
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):#Сравнение хэшей паролей
        return {"error": "Invalid email or password"}
    return {"message": f"Welcome, {user["name"]}"}


@app.get("/users") #Эндпоинт вывода всех пользователей
def get_users():
    return users

@app.get("/users/{id}", summary="Get user by id") #Эндпоинт выводящий пользователя по id
def get_user_by_id(id:int):
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{id}", summary="Update user data") #Эндпоинт для обновления информации о пользователе
def update_user_data(id:int, user_name:str, email:EmailStr, role:str):
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["name"] = user_name
    user["email"] = email
    user["role"] = role
    return user

@app.delete("/users/{id}", summary="Delete user") #Эндпоинт для удаления пользователя
def delete_user(id:int):
    global users #Изменяем глобальную переменную(словарь с начальными пользователями)
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users = [t for t in users if t["id"] != id]
    return{"message":f"{user["name"]} successfuly deleted"}
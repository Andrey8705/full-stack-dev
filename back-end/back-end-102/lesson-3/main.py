from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

users = [ #Начальный словарь с пользователями
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "role": "user"}
]

class User(BaseModel):
    name: str
    email: EmailStr
    role: str

@app.post("/users")  #Эндпроинт для создания пользователя и присвоения ему id
def create_user(user:User):
    new_id = users[-1]["id"] + 1 if users else 1
    new_user = {"id":new_id, "name":user.name, "email":user.email, "role":user.role}
    users.append(new_user)
    return {"message": f"User {user.name} created successfully!"}

@app.get("/users") #Эндпоинт вывода всех пользователей
def get_users():
    return users

@app.get("/users/{new_id}", summary="Get user by id") #Эндпоинт выводящий пользователя по id
def get_user_by_id(new_id:int):
    user = next((user for user in users if user["id"] == new_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{new_id}", summary="Update user data") #Эндпоинт для обновления информации о пользователе
def update_user_data(new_id:int, user_name:str, email:EmailStr, role:str):
    user = next((user for user in users if user["id"] == new_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["name"] = user_name
    user["email"] = email
    user["role"] = role
    return user

@app.delete("/users/{new_id}", summary="Delete user") #Эндпоинт для удаления пользователя
def delete_user(new_id:int):
    global users #Изменяем глобальную переменную(словарь с начальными пользователями)
    user = next((user for user in users if user["id"] == new_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users = [t for t in users if t["id"] != new_id]
    return{"message":f"{User.name} successfuly deleted"}
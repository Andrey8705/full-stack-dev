from pydantic import EmailStr, BaseModel

class UserRegister(BaseModel):
    name: str
    password: str
    email: EmailStr
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
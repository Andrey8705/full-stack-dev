from pydantic import BaseModel, Field

class CapsuleCreate(BaseModel):
    name: str = Field(description= "Название капсулы")
    unlock_date: str = Field(description= "Дата когда капсула будет открыта. Формат *ГГГГ.ММ.ДД*")
    message: str = Field(description= "Короткое сообщение для получателя.")
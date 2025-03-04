from pydantic import BaseModel, Field
from datetime import datetime

class CapsuleCreate(BaseModel):
    name: str = Field(description= "Название капсулы")
    unlock_date: str = Field(description= "Дата когда капсула будет открыта. Формат *ГГГГ.ММ.ДД*")
    message: str = Field(description= "Короткое сообщение для получателя.")


class CapsuleSchema(BaseModel):
    id: int
    name: str
    unlock_date: datetime
    message: str
    user_id: int
    create_date: datetime 

    class Config:
        from_attributes = True  # Позволяет использовать SQLAlchemy-объекты

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class CapsuleCreate(BaseModel):
    name: str = Field(description= "Название капсулы")
    unlock_date: str = Field(description= "Дата когда капсула будет открыта. Формат *ГГГГ.ММ.ДД*")
    message: str = Field(description= "Короткое сообщение для получателя.")


class CapsuleSchema(BaseModel):
    id: UUID
    name: str
    unlock_date: datetime
    message: str
    user_id: int
    create_date: datetime
    is_public: bool

    model_config = {
        "from_attributes": True  # это как orm_mode в Pydantic 1
    } 
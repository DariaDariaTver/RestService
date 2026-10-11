from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    """Общие поля для схем User."""
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=5, max_length=20)

class UserCreate(UserBase):
    """Что приходит на register."""
    password: str = Field(min_length=8, max_length=100)

class RoleRead(BaseModel):
    """Вложенный объект в UserRead."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserRead(UserBase):
    """Что приходит клиенту."""
    id: int
    role: RoleRead
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """Обновление пользователя."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, min_length=5, max_length=20)
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True)

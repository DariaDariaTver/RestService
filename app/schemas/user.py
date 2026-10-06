from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=5, max_length=20)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class RoleRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserRead(UserBase):
    id: int
    role: RoleRead
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, min_length=5, max_length=20)
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True)

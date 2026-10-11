from pydantic import BaseModel, EmailStr
from app.schemas.user import UserRead

class LoginRequest(BaseModel):
    """Что приходит на login."""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Что уходит клиенту."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead

class RefreshRequest(BaseModel):
    """Что приходит на refresh."""
    refresh_token: str
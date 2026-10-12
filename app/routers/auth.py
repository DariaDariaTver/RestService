from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.role import Role
from app.models.refresh_token import RefreshToken
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.schemas.user import UserCreate, UserRead
from app.dependencies.auth import get_current_user
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.config import settings
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("register", response_model=UserRead, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Зарегистрировать пользователя."""
    existing = db.query(User).filter(User.email == data.email) | (User.phome == data.phone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail="Email or phone already exists",
        )
    
    default_role = db.query(Role).filter(Role.name == "customer").first()
    if not default_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default role not found",
        )

    hashed = hash_password(data.password)

    user = User(
        email=data.email,
        name=data.name,
        phone=data.phone,
        pw_hash=hashed,
        role_id=default_role.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user




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
from sqlalchemy import or_

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Зарегистрировать пользователя."""
    existing = db.query(User).filter(
    or_(
        User.email == data.email,
        User.phone == data.phone,
    )
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone already exists",
        )
    
    default_role = db.query(Role).filter(Role.name == "user").first()
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

@router.post("/login", response_model=TokenResponse, status_code=200)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Войти в систему."""
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not verify_password(data.password, user.pw_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    refresh_save = RefreshToken(
        user_id=user.id,
        token=refresh,
        expires_at=datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(refresh_save)
    db.commit()

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserRead, status_code=200)
def get_me(user: User = Depends(get_current_user)):
    """Получить данные пользователя."""
    return user

@router.post("/refresh", status_code=200)
def update_refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    """Обновить access через refresh."""
    payload = decode_token(data.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not payload"
        )
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    token_save = db.query(RefreshToken).filter(RefreshToken.token == data.refresh_token).first()
    if not token_save:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )
    if token_save.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    if token_save.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    user_id = int(payload["sub"])
    new_access = create_access_token(user_id)
    return {
        "access_token": new_access,
        "token_type": "bearer",
    }
    
    
    
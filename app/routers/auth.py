from typing import Annotated
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
from sqlalchemy import or_, select

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=201)
def register(data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Зарегистрировать пользователя."""
    stmt = select(User).where(
    or_(
        User.email == data.email,
        User.phone == data.phone,
    ))
    existing_user = db.execute(stmt).scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or phone already exists",
        )
    role_stmt = select(Role).where(Role.name == "user")
    default_role = db.execute(select(Role)).scalars().first()
    if not default_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default role not found",
        )

    hashed = hash_password(data.password)

    new_user = User(
        email=data.email,
        name=data.name,
        phone=data.phone,
        pw_hash=hashed,
        role_id=default_role.id
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )
    return new_user

@router.post("/login", response_model=TokenResponse, status_code=200)
def login(data: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    """Войти в систему."""
    stmt = select(User).where(User.email == data.email)
    user = db.execute(stmt).scalars().first()
    if not user or not verify_password(data.password, user.pw_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
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
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error save refesh token"
        )

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserRead, status_code=200)
def get_me(user: Annotated[User, Depends(get_current_user)]):
    """Получить данные пользователя."""
    return user

@router.post("/refresh", status_code=200)
def update_refresh_token(data: RefreshRequest, db: Annotated[Session, Depends(get_db)]):
    """Обновить пару токенов: access и refresh."""
    payload = decode_token(data.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    stmt = select(RefreshToken).where(RefreshToken.token == data.refresh_token)
    token_save = db.execute(stmt).scalars().first()
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
    token_save.revoked = True
    new_refresh = create_refresh_token(user_id)
    new_token_save = RefreshToken(
        user_id=user_id,
        token=new_refresh,
        expires_at=datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
    )
    db.add(new_token_save)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error update token"
        )

    new_access = create_access_token(user_id)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer"
    }

@router.post("/logout", status_code=204)
def logout(data: RefreshRequest, db: Annotated[Session, Depends(get_db)]):
    """Выйти из системы."""
    stmt = select(RefreshToken).where(RefreshToken.token == data.refresh_token)
    token_save = db.execute(stmt).scalars().first()
    if token_save:
        token_save.revoked = True
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            pass
        return None
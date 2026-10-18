from datetime import datetime, timedelta, timezone
from typing import Any
import bcrypt
import jwt
import uuid

from app.config import settings

def hash_password(password: str) -> str:
    """Превратить пароль в bcrypt-хэш."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить соответствие пароля хэшу."""
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(user_id: int) -> str:
    """Создать access-токен."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(user_id),
        "exp": expires_at,
        "type": "access",
        "jti": uuid.uuid4().hex,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    """Создать refresh-токен."""
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": str(user_id),
        "exp": expires_at,
        "type": "refresh",
        "jti": uuid.uuid4().hex,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict | None:
    """Расшифровать JWT."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
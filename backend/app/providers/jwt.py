from datetime import datetime, timedelta, timezone
from typing import Any, Union

from app.config import setting
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: Union[str, Any], expiration: timedelta = None):
    delta = expiration or timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + delta

    to_encode = {"exp": expire, "sub": str(data)}
    return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

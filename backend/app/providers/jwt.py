from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union

from jose import jwt
from jose.exceptions import JWTError

from app.config import setting


def create_access_token(data: Union[str, Any], expiration: timedelta = None) -> str:
    delta = expiration or timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + delta

    to_encode = {"exp": expire, "sub": str(data)}
    return jwt.encode(to_encode, setting.SECRET_KEY)


def create_password_reset_token(email: str) -> str:
    delta = timedelta(hours=setting.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expire = now + delta
    to_encode = {"exp": expire, "nbf": now, "sub": email}
    return jwt.encode(to_encode, setting.SECRET_KEY)


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, setting.SECRET_KEY)
        return decoded_token["sub"]
    except JWTError:
        return None

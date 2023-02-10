from datetime import datetime, timedelta, timezone
from typing import Any, Union

from app.config import setting
from jose import jwt


def create_access_token(data: Union[str, Any], expiration: timedelta = None):
    delta = expiration or timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + delta

    to_encode = {"exp": expire, "sub": str(data)}
    return jwt.encode(to_encode, setting.SECRET_KEY)

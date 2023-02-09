from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.config import setting
from app.errors import AuthFailed, ExpiredToken, UserNotExist
from app.providers.database import get_db

oauth2 = OAuth2PasswordBearer(tokenUrl=f"{setting.API_PREFIX}/login/token")


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, setting.SECRET_KEY)
        data = schemas.TokenPayload(**payload)
    except ExpiredSignatureError:
        raise ExpiredToken
    except (ValidationError, JWTError):
        raise AuthFailed

    user = await crud.user.get(db, id=data.sub)
    if not user:
        raise UserNotExist
    return user

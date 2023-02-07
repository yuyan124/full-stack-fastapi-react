from typing import Any
from datetime import timedelta
from app.config import setting
from app import crud, schemas
from app.providers.database import get_db
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.providers import jwt
from app.errors import IncorrectEmailOrPassword, InactiveUser

router = APIRouter()


@router.post("/login/token", response_model=schemas.Token)
async def token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.auth(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise IncorrectEmailOrPassword
    elif not crud.user.is_active(user):
        raise InactiveUser

    token = jwt.create_access_token(
        user.id, timedelta(setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "token": token,
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}")
def password_recovery(email: str, db: AsyncSession = Depends(get_db)) -> Any:
    ...


@router.post("/reset-password/")
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(get_db),
) -> Any:
    ...

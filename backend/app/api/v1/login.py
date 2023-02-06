from typing import Any

from app import crud, schemas
from app.errors import UserExist, UserNotExist
from app.providers.database import get_db
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.providers import jwt
from app.errors import IncorrectEmailOrPassword

router = APIRouter()


@router.post("/login/token")
async def token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.auth(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise IncorrectEmailOrPassword
    token = jwt.create_access_token("1")
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

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.config import setting
from app.errors import InactiveUser, IncorrectEmailOrPassword
from app.providers import jwt
from app.providers.database import get_db

router = APIRouter()


@router.post("/login/token", response_model=schemas.Token)
async def token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> JSONResponse:
    """
    OAuth2兼容的令牌登录, 为未来的请求获取一个访问令牌。

    @param:
        db: 数据库session. Defaults to Depends(get_db).
        form_data: 用户登录帐号密码. Defaults to Depends().

    @raise:
        IncorrectEmailOrPassword: 帐号不存在或密码错误
        InactiveUser: 帐号未激活

    @return:
        JSONResponse: 成功返回令牌，失败返回错误信息及错误码。
    """
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
        "access_token": token,
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

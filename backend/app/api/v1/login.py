from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.config import setting
from app.errors import (
    InactiveUser,
    IncorrectEmailOrPassword,
    InvalidToken,
    UserNotExist,
)
from app.providers import jwt
from app.providers.crypto import generate_password_hash
from app.providers.database import get_db
from app.response import response_ok
from app.response.msg import MsgResponse

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


@router.post("/password-recovery/{email}", response_model=MsgResponse)
async def password_recovery(
    email: str, db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    user = await crud.user.get_by_email(db, email=email)

    if not user:
        raise UserNotExist

    token = jwt.create_password_reset_token(email)
    # TODO: send reset email
    return response_ok(MsgResponse, data={"msg": "密码重置邮件已发送."})


@router.post("/reset-password/", response_model=MsgResponse)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    email = jwt.verify_password_reset_token(token)
    if not email:
        raise InvalidToken

    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise UserNotExist
    elif not crud.user.is_active(user):
        raise InactiveUser

    user.password = generate_password_hash(new_password)
    db.add(user)
    await db.flush()
    db.expunge(user)
    await db.commit()
    return response_ok(MsgResponse, data={"msg": "密码重置成功."})

from typing import Any

import pydantic
from app import crud, schemas
from app.errors import UserExist, UserNotExist
from app.providers.database import get_db
from app.response.user import UserListResponse, UserResponse
from faker import Faker
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


def create_fake_user(id: int):
    faker = Faker(locals="zh-CN")
    return {
        "email": faker.email(),
        "phone": faker.phone_number(),
        "is_superuser": True,
        "nickname": faker.name(),
        "id": id,
        "status": 1,
        "create_time": faker.date_time().strftime("%Y-%m-%d %H:%M:%S"),
    }


@router.post("/", response_model=UserResponse)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise UserExist
    user = await crud.user.create(db, user_in=user_in)
    r = UserResponse(code=0, success=True, data=user)
    return JSONResponse(content=jsonable_encoder(r))


@router.get("/", response_model=UserListResponse)
async def get_users(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
) -> JSONResponse:
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    r = UserListResponse(code=0, success=True, data=users)
    return JSONResponse(content=jsonable_encoder(r))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> JSONResponse:
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise UserNotExist
    r = UserResponse(code=0, success=True, data=user)
    return JSONResponse(content=jsonable_encoder(r))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    *, db: AsyncSession = Depends(get_db), user_id: int, user_in: schemas.UserUpdate
) -> JSONResponse:
    # user = await crud.user.get(db, id=user_id)
    # if not user:
    # raise UserNotExist
    user = await crud.user.update(db, id=user_id, obj_in=user_in)
    r = UserResponse(code=0, success=True, data=user)
    return JSONResponse(content=jsonable_encoder(r))

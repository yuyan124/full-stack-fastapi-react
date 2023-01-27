from typing import Any

import pydantic
from app import crud, schemas
from app.providers.database import get_db
from faker import Faker
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

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


@router.get("/", response_class=schemas.User, response_model_exclude_unset=True)
def read_users() -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(create_fake_user(1)))


@router.post("/", response_class=schemas.User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
):
    print(user_in)
    user = crud.user.create_user(db, user_in)
    print(user)
    return JSONResponse(content=jsonable_encoder(user))


@router.get("/{user_id}", response_class=schemas.User)
async def get_user(user_id: int) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(create_fake_user(user_id)))

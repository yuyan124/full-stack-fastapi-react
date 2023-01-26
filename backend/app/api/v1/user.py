from typing import Any

import pydantic
from app import schemas
from faker import Faker
from fastapi import APIRouter

router = APIRouter()


def create_fake_user():
    faker = Faker(locals="zh-CN")
    return {
        "email": faker.email(),
        "phone": faker.phone_number(),
        "is_superuser": True,
        "nickname": faker.name(),
        "id": 1,
        "status": 1,
        "create_time": faker.date_time().strftime("%Y-%m-%d %H:%M:%S"),
    }


@router.get("/", response_class=schemas.User)
def read_users() -> Any:
    return create_fake_user()


@router.get("/{user_id}", response_class=schemas.User)
async def get_user(user_id: int) -> Any:

    return create_fake_user()

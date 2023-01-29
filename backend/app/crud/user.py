from datetime import datetime
from typing import Any

from app.crud.base import CrudBase
from app.models.user import User
from app.schemas import UserCreate, UserUpdate
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# async def create_user(db: AsyncSession, user: UserCreate) -> User:
#     db_user = User(
#         email=user.email,
#         password=user.password,
#         nickname=user.nickname,
#         create_time=int(datetime.now().timestamp()),
#     )
#     async with db.begin():
#         db.add(db_user)
#         await db.commit()
#         # await db.refresh(db_user)
#         db.expunge(db_user)
#         return db_user


class CrudUser(CrudBase[User, UserCreate, UserUpdate]):
    async def create(self, db: AsyncSession, *, user_in: UserCreate) -> Any:
        user_db = User(
            email=user_in.email,
            password=user_in.password,
            nickname=user_in.nickname,
            is_superuser=False,
            create_time=int(datetime.now().timestamp()),
        )

        # async with db.begin():
        try:
            async with db.begin():
                db.add(user_db)
                await db.flush()
                db.expunge(user_db)
                return user_db
        except (UniqueViolationError, IntegrityError) as e:
            return {f"{e.detail}"}


user = CrudUser(User)

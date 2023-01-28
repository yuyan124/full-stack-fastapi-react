from datetime import datetime

from app.crud.base import CrudBase
from app.models.user import User
from app.schemas import UserCreate, UserUpdate
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
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=obj_in.password,
            nickname=obj_in.nickname,
            create_time=int(datetime.now().timestamp()),
        )
        async with db.begin():
            db.add(db_obj)
            await db.commit()
            db.expunge(db_obj)
            return db_obj


user = CrudUser(User)

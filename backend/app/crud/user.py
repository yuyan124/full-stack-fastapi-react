from datetime import datetime
from typing import Any, Dict, Optional, Union

from app.crud.base import CrudBase
from app.models.user import User
from app.schemas import UserCreate, UserUpdate
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import select, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.providers.crypto import check_password_hash


class CrudUser(CrudBase[User, UserCreate, UserUpdate]):
    async def create(self, db: AsyncSession, *, user_in: UserCreate) -> Any:
        try:
            async with db.begin():
                user_db = User(
                    email=user_in.email,
                    password=user_in.password,
                    nickname=user_in.nickname,
                    is_superuser=user_in.is_superuser,
                    create_time=int(datetime.now().timestamp()),
                )
                db.add(user_db)
                await db.flush()
                db.expunge(user_db)
                return user_db
        except (UniqueViolationError, IntegrityError) as e:
            # return {f"{e.detail}"}
            return None

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        try:
            # async with db.begin():
            sql = select(self.model).where(self.model.email == email)
            r = await db.execute(sql)
            return r.scalars().first()
        except Exception:
            db.rollback()

    async def update(
        self,
        db: AsyncSession,
        *,
        id: int,
        obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        async with db.begin():
            user = await self.get(db, id)
            if not user:
                return None
            user.email = obj_in.email
            user.nickname = obj_in.nickname
            await db.flush()
            db.expunge(user)
            return user

        # sql = (
        #     update(self.model)
        #     .where(self.model.id == id)
        #     .values(email=obj_in.email, nickname=obj_in.nickname)
        # )
        # sql = text(f"UPDATE \"user\" SET email = '{obj_in.email}' WHERE id = {id}")
        # r = await db.execute(sql)
        # return obj_in

    async def auth(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None

        if not check_password_hash(password, user.password):
            return None
        return user


user = CrudUser(User)

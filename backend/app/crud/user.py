from datetime import datetime
from typing import Any, Dict, Optional, Union

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import select, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.models.user import User
from app.providers.crypto import check_password
from app.schemas import UserCreate, UserUpdate


class CrudUser(CrudBase[User, UserCreate, UserUpdate]):
    async def create(self, db: AsyncSession, *, user_in: UserCreate) -> Any:
        try:
            user_db = User(
                email=user_in.email,
                password=user_in.password,
                nickname=user_in.nickname,
                is_superuser=user_in.is_superuser,
                create_time=int(datetime.now().timestamp()),
            )
            db.add(user_db)
            await db.commit()
            return user_db
        except Exception as e:
            await db.rollback()
        return None

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        sql = select(self.model).where(self.model.email == email)
        r = await db.execute(sql)
        return r.scalars().first()

    async def auth(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email=email)

        if not user:
            return None

        return user if check_password(password, user.password) else None

    def is_active(self, user: User) -> bool:
        return user.status == 1

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CrudUser(User)

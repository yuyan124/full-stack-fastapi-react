from datetime import datetime

from app.models.user import User
from app.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        password=user.password,
        nickname=user.nickname,
        create_time=int(datetime.now().timestamp()),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

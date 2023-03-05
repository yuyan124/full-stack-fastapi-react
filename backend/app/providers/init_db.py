from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.config import setting


async def init_db(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(db, email=setting.SUPERUSER)
    if not user:
        user = schemas.UserCreate(
            email=setting.SUPERUSER,
            password=setting.SUPERUSER_PASSWORD,
            is_superuser=True,
            nickname="Admin",
        )
        await crud.user.create(db, user_in=user)

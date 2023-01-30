from typing import AsyncGenerator, Callable

from app.config import setting
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(setting.ASYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal: Callable[..., AsyncSession] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

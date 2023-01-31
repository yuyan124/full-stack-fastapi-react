from typing import AsyncGenerator, Callable

from app.config import setting
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# @brief:
#   @param: echo, 打印执行日志
#   @param: future: 使用2.0行特性, engine延迟初始化，直到第一次请求真正连接
engine = create_async_engine(
    setting.ASYNC_SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    future=True,
    # echo=True,
)
SessionLocal: Callable[..., AsyncSession] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

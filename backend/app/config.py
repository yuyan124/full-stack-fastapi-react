import os
import secrets
from typing import Any, Dict, Optional

import pydantic
from dotenv.main import load_dotenv

load_dotenv()


class Setting(pydantic.BaseSettings):
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # PROJECT_NAME: str
    POSTGRESQL_SERVER: str = os.environ["POSTGRES_SERVER"]
    POSTGRESQL_USER: str = os.environ["POSTGRES_USER"]
    POSTGRESQL_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRESQL_DB: str = os.environ["POSTGRES_DB"]
    SQLALCHEMY_DATABASE_URI: Optional[
        pydantic.PostgresDsn
    ] = pydantic.PostgresDsn.build(
        scheme="postgresql",
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_SERVER"],
        path=f"/{os.environ['POSTGRES_DB'] or ''}",
    )
    ASYNC_SQLALCHEMY_DATABASE_URI: Optional[
        pydantic.PostgresDsn
    ] = pydantic.PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_SERVER"],
        path=f"/{os.environ['POSTGRES_DB'] or ''}",
    )

    class Config:
        case_sensitive = True


setting = Setting()

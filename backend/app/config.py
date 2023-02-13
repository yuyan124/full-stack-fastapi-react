import os
import secrets
from typing import Any, Dict, List, Optional

import pydantic
from dotenv.main import load_dotenv

load_dotenv()


class Setting(pydantic.BaseSettings):
    PROJECT_NAME: str = os.environ["PROJECT_NAME"]
    API_PREFIX: str = "/api/v1"

    # ------------------------------------------
    # security
    # ------------------------------------------
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    # 60 minutes * 24 hours * 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM = "HS256"

    # ------------------------------------------
    # database
    # ------------------------------------------

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
    # ------------------------------------------
    # database init
    # ------------------------------------------
    # email
    SUPERUSER: pydantic.EmailStr = os.environ["SUPERUSER"]
    SUPERUSER_PASSWORD: str = os.environ["SUPERUSER_PASSWORD"]
    CORS_ORIGINS: List[pydantic.AnyHttpUrl] = os.environ["CORS_ORIGINS"]

    LOG_DIRECTORY = "logs/"

    EMAIL_ENABLED_CONFIRM: bool = True

    class Config:
        case_sensitive = True


setting = Setting()

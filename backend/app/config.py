import secrets
import typing

import pydantic


class Setting(pydantic.BaseSettings):
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # PROJECT_NAME: str
    # POSTGRESQL_SERVER: str
    # POSTGRESQL_USER: str
    # POSTGRESQL_PASSWORD: str
    # POSTGRESQL_DB: str
    SQLALCHEMY_DATABASE_URI: typing.Optional[pydantic.PostgresDsn] = None

    class Config:
        case_sensitive = True


setting = Setting()

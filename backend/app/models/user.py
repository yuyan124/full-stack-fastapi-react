from sqlalchemy import Boolean, Column, Integer, SmallInteger, String

from app.providers.crypto import check_password, generate_password_hash

from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(SmallInteger, default=1)
    is_superuser = Column(Boolean(), default=False)
    create_time = Column(Integer)

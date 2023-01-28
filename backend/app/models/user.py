from app.providers.crypto import check_password_hash, generate_password_hash
from sqlalchemy import Boolean, Column, Integer, SmallInteger, String

from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    _password = Column("password", String, nullable=False)
    status = Column(SmallInteger, default=1)
    is_superuser = Column(Boolean(), default=False)
    create_time = Column(Integer)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_pwd: str):
        self._password = str(generate_password_hash(raw_pwd.encode("utf8")))

    def check_password(self, raw_pwd: str):
        if not self._password:
            return False
        password_hash = str(generate_password_hash(self._password.encode("utf8")))
        return check_password_hash(password_hash, self._password)

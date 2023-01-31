from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_superuser: bool = False
    nickname: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserDbBase(UserBase):
    id: Optional[int] = None
    status: Optional[int] = None
    create_time: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserDbBase):
    pass


class UserInDb(UserDbBase):
    hashed_password: str

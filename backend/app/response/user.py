from typing import List

from app.schemas import User

from .base import ResponseBase


class UserResponse(ResponseBase):
    data: User


class UserListResponse(ResponseBase):
    data: List[User]

from app.schemas import User

from .base import ResponseBase


class UserResponse(ResponseBase):
    data: User

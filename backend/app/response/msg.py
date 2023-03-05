from typing import Dict

from app.schemas.msg import Msg

from .base import ResponseBase


class MsgResponse(ResponseBase):
    data: Msg

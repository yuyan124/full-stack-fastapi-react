from typing import Any

from pydantic import BaseModel


class ResponseBase(BaseModel):
    code: int = None
    success: bool = None
    data: Any = None

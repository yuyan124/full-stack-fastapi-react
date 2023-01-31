from typing import Any, Type

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .base import ResponseBase


def custom_response(
    class_name: Type[ResponseBase], data: Any, code: int = 0, success: bool = True
) -> JSONResponse:
    r = class_name(code=code, success=success, data=data)
    return JSONResponse(content=jsonable_encoder(r))

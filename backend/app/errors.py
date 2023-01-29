from typing import Optional, Dict, Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ApiResponse(JSONResponse):
    status_code: int = 200
    api_code: int = 0
    message: str = "success"
    success: bool = True
    data: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        status_code: int = None,
        api_code: int = None,
        data: Optional[Dict[str, Any]] = None,
        message: str = None,
        success: bool = None,
        **options
    ):
        if data:
            self.data = data
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        if api_code:
            self.api_code = api_code
        if success:
            self.success = success

        body = Dict()

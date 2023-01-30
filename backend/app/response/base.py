from pydantic import BaseModel


class ResponseBase(BaseModel):
    code: int = None
    success: bool = None

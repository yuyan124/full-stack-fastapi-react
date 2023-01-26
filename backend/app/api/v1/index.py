from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def index() -> JSONResponse:
    return jsonable_encoder({"success": True, "message": "This is backend index."})

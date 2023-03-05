from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.providers.log import logger

router = APIRouter()


@router.get("/")
async def index() -> JSONResponse:
    logger.debug("enter index.")
    return jsonable_encoder({"success": True, "message": "This is backend index."})

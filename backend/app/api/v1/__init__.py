from fastapi import APIRouter, Depends, Request

from app.api.v1 import login, user
from app.providers.log import logger


async def request_info(request: Request) -> None:
    logger.bind(name=None).info(f"{request.method} {request.url} ")
    try:
        body = await request.json()
        logger.bind(payload=body, name=None).debug("request_json: ")
    except Exception:
        body = await request.body()
        if len(body) != 0:
            logger.bind(payload=body, name=None).debug(body)


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(request_info)]
)

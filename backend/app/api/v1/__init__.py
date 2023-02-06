from app.api.v1 import user
from app.api.v1 import login
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])

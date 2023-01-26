from app.api.v1 import user
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])

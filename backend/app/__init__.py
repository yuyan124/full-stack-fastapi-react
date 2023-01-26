from app.config import setting
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app_version = "0.0.1"


def register_router(app: FastAPI):
    from app.api.v1 import api_router
    from app.api.v1 import index

    app.include_router(index.router)
    app.include_router(api_router, prefix=setting.API_PREFIX)


def carete_app() -> FastAPI:
    app = FastAPI(version=app_version)
    register_router(app)

    return app

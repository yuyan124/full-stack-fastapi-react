from app.config import setting
from fastapi import FastAPI

app_version = "0.0.1"


def register_router(app: FastAPI):
    from app.api.v1 import api_router, index

    app.include_router(index.router)
    app.include_router(api_router, prefix=setting.API_PREFIX)


def register_exception_handler(app: FastAPI) -> None:
    from fastapi import Request
    from fastapi.encoders import jsonable_encoder
    from fastapi.exceptions import RequestValidationError
    from fastapi.responses import JSONResponse
    from starlette.exceptions import HTTPException as StarletteHTTPException

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc) -> JSONResponse:
        headers = getattr(exc, "headers", None)

        content = {
            "code": getattr(exc, "code", 9999),
            "msg": getattr(exc, "msg", "╮(๑•́ ₃•̀๑)╭"),
            "request": f"{request.method} {request.scope['path']}",
        }
        if headers:
            return JSONResponse(
                status_code=exc.status_code,
                content=jsonable_encoder(content),
                headers=headers,
            )
        return JSONResponse(
            status_code=exc.status_code, content=jsonable_encoder(content)
        )


def register_middleware(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware

    origins = setting.CORS_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 强制请求协议为HTTPS
    # from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
    # app.add_middleware(HTTPSRedirectMiddleware)

    # 避免 HTTP Host Header攻击
    # from fastapi.middleware.trustedhost import TrustedHostMiddleware
    # app.add_middleware(TrustedHostMiddleware, allow_hosts=[*.example.com])

    # 请求头Accept-Encoding带有gzip，GZipMiddleware负责完成相应的返回结果处理。
    # from fastapi.middleware.gzip import GZipMiddleware
    # app.add_middleware(GZipMiddleware, minimum_size=1000)


def register_plugin():
    from app.models.base import Base
    from app.providers.database import engine

    # Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(version=app_version)
    register_middleware(app)
    register_router(app)
    register_exception_handler(app)
    register_plugin()

    return app

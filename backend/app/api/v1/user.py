from faker import Faker
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import depends
from app.errors import Forbidden, UserExist, UserNotExist
from app.providers.database import get_db
from app.response import response_ok
from app.response.user import UserListResponse, UserResponse

router = APIRouter()


def create_fake_user(id: int):
    faker = Faker(locals="zh-CN")
    return {
        "email": faker.email(),
        "phone": faker.phone_number(),
        "is_superuser": True,
        "nickname": faker.name(),
        "id": id,
        "status": 1,
        "create_time": faker.date_time().strftime("%Y-%m-%d %H:%M:%S"),
    }


@router.post("/", response_model=UserResponse)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(depends.get_current_superuser)
) -> JSONResponse:
    """
    创建新用户

    @param:
        user_in: 待创建新用户的信息
        db: 数据库session. Defaults to Depends(get_db).

    @raise:
        UserExist: 用户存在，

    @return:
        JSONResponse: 成功返回创建用户的信息，失败返回错误码及错误信息。
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise UserExist
    user = await crud.user.create(db, user_in=user_in)
    return response_ok(UserResponse, user)


@router.get("/", response_model=UserListResponse)
async def get_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(depends.get_current_superuser),
) -> JSONResponse:
    """
    批量读取用户。

    @param:
        db: 数据库session. Defaults to Depends(get_db).
        skip: 从第skip之后读取. Defaults to 0.
        limit: 读取用户的数量. Defaults to 100.

    @return:
        JSONResponse: 成功返回用户信息。
    """
    users = await crud.user.get_multi(db, skip=skip, limit=limit)
    return response_ok(UserListResponse, users)


@router.get("/me", response_model=UserResponse)
def get_user_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> JSONResponse:
    return response_ok(UserResponse, current_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> JSONResponse:
    """
    通过user_id获取特定用户信息。

    @param:
        user_id: 用户id
        db: 数据库session. Defaults to Depends(get_db).

    @raise:
        Forbidden: 权限不足
        UserNotExist: 用户不存在

    @return:
        JSONResponse: 成功返回用户信息，失败返回错误码及错误信息。
    """
    user = await crud.user.get(db, id=user_id)
    if user == current_user:
        return response_ok(UserResponse, user)

    if not crud.user.is_superuser(current_user):
        raise Forbidden

    if not user:
        raise UserNotExist

    return response_ok(UserResponse, user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(depends.get_current_superuser)
) -> JSONResponse:
    """
    通过user_id更新用户信息

    @param:
        user_id: 用户id
        user_in: 待更新的用户信息
        db: 数据库session. Defaults to Depends(get_db).

    @raise:
        UserNotExist: 用户不存在

    @return:
        JSONResponse: 成功返回用户信息，失败返回错误码及错误信息。
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise UserNotExist
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return response_ok(UserResponse, user)

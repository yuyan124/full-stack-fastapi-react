from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.models.base import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        # return await db.
        async with db.begin():
            sql = select(self.model).where(self.model.id == id)
            r = await db.execute(sql)
            return r.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        # return await db.

        async with db.begin():
            sql = select(self.model).offset(skip).limit(limit)
            r = await db.execute(sql)
            return r.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        json_data = jsonable_encoder(obj_in)
        db_obj = self.model(**json_data)
        async with db.begin():
            db.add(db_obj)
            await db.commit()
            db.expunge(db_obj)
            return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_model: ModelType,
        model_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        json_data = jsonable_encoder(db_model)
        if isinstance(model_in, dict):
            update_data = model_in
        else:
            update_data = model_in.dict(exclude_unset=True)

        for filed in json_data:
            if filed in update_data:
                setattr(db_model, filed, update_data[filed])
        async with db.begin():
            db.add(db_model)
            await db.commit()
            db.expunge(db_model)
            return db_model

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        async with db.begin():
            sql = select(self.model).where(self.model.id == id)
            r = db.execute(sql)
            original = r.scalars().first()
            db.delete(original)
            await db.commit()
            return original

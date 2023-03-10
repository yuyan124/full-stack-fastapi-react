from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        sql = select(self.model).where(self.model.id == id)
        r = await db.execute(sql)
        return r.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        sql = text(
            f'SELECT * FROM "{self.model.__tablename__}" LIMIT {limit} OFFSET {skip}'
        )
        r = await db.execute(sql)
        return r.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            json_data = jsonable_encoder(obj_in)
            db_obj = self.model(**json_data)
            db.add(db_obj)
            await db.flush()
            db.expunge(db_obj)
            await db.commit()
            return db_obj
        except Exception as e:
            await db.rollback()
        return None

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        json_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for filed in json_data:
            if filed in update_data:
                setattr(db_obj, filed, update_data[filed])

        db.add(db_obj)
        await db.flush()
        db.expunge(db_obj)
        await db.commit()
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        sql = select(self.model).where(self.model.id == id)
        r = db.execute(sql)
        original = r.scalars().first()
        db.delete(original)
        await db.flush()
        db.expunge(original)
        await db.commit()
        return original

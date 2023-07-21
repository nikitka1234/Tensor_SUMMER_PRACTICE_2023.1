import uuid
from datetime import datetime
from typing import Any, Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, *, model_id: uuid.UUID | int) -> ModelType | None:
        model_obj = await db.get(self.model, model_id)
        return model_obj

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            offset: int = 0,
            limit: int = 100
    ) -> list[ModelType]:
        q = select(self.model).offset(offset).limit(limit)
        result = await db.execute(q)
        curr = list(result.scalars())
        return curr

    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["updated_at"] = datetime.utcnow()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, model_id: uuid.UUID | int) -> ModelType:
        db_obj = await self.get(db, model_id=model_id)
        setattr(db_obj, "deleted_at", datetime.utcnow())
        setattr(db_obj, "updated_at", datetime.utcnow())

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(
            self, db: AsyncSession, *, model_id: uuid.UUID | int
    ) -> ModelType:
        obj = await self.get(db, model_id=model_id)
        await db.delete(obj)
        await db.commit()
        return obj

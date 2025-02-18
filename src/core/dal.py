from typing import Any, Generic, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.src import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseDAL(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, item_id: int) -> ModelType | None:
        return await db.get(self.model, item_id)

    async def get_multi(
        self, db: AsyncSession, *, pagi: dict[str, Any] | None = None, search_data: dict[str, Any] | None = None
    ) -> list[ModelType]:
        query = select(self.model)
        if pagi:
            query = query.limit(pagi.get("limit", 20)).offset(pagi.get("offset", 0))
        ...
        result = await db.execute(query)
        return result.scalars().all()  # type: ignore

    async def create(self, db: AsyncSession, data: dict[str, Any]) -> ModelType:
        obj = self.model(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, item_id: int, data: dict[str, Any]) -> ModelType | None:
        query = update(self.model).where(self.model.id == item_id).values(**data).returning(self.model)
        result = await db.execute(query)
        await db.commit()
        updated = result.scalars().first()
        if updated:
            await db.refresh(updated)
        return updated

    async def delete(self, db: AsyncSession, item_id: int) -> int | None:
        query = delete(self.model).where(self.model.id == item_id).returning(self.model.id)
        result = await db.execute(query)
        await db.commit()
        return result.scalars().first()

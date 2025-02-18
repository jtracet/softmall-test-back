from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dal import BaseDAL
from src.models.src.modules.settings import Settings, SettingsDict


class SettingsDAL(BaseDAL[Settings]):
    async def update(self, db: AsyncSession, item_id: int, data: dict[str, Any]) -> Settings | None:
        query = update(self.model).where(self.model.id == item_id).values(**data).returning(self.model)
        result = await db.execute(query)
        await db.commit()
        updated = result.scalars().first()
        if updated:
            await db.refresh(updated)
        return updated


settings_dal = SettingsDAL(Settings)


class SettingsDictDAL(BaseDAL[SettingsDict]):
    async def get_by_code(self, db: AsyncSession, code: str) -> SettingsDict | None:
        query = select(SettingsDict).where(SettingsDict.code == code)
        result = await db.execute(query)
        return result.scalars().first()


settings_dict_dal = SettingsDictDAL(SettingsDict)

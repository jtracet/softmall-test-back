from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dal import BaseDAL
from src.models.src.modules.dicts import TimezoneDict


class TimezoneDAL(BaseDAL[TimezoneDict]):
    async def get_by_name(self, db: AsyncSession, name: str) -> TimezoneDict | None:
        query = select(TimezoneDict).where(TimezoneDict.timezone_name == name)
        result = await db.execute(query)
        return result.scalars().first()


timezone_dal = TimezoneDAL(TimezoneDict)

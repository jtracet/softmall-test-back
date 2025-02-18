from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.timezones.dals import timezone_dal
from src.timezones.schemas import TimezoneCreateSchema, TimezoneSchema


class TimezoneActions:
    @staticmethod
    async def create(db: AsyncSession, data: TimezoneCreateSchema) -> TimezoneSchema:
        tz = await timezone_dal.create(db, data.dict())
        return TimezoneSchema.from_orm(tz)

    @staticmethod
    async def get_by_id(db: AsyncSession, tz_id: int) -> TimezoneSchema:
        tz = await timezone_dal.get(db, tz_id)
        if not tz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timezone not found")
        return TimezoneSchema.from_orm(tz)

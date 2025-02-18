from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.timezones.actions import TimezoneActions
from src.timezones.schemas import TimezoneCreateSchema, TimezoneSchema

timezones_router = APIRouter()


@timezones_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_timezone(data: TimezoneCreateSchema, db: AsyncSession = Depends(get_db)) -> TimezoneSchema:
    return await TimezoneActions.create(db, data)


@timezones_router.get("/{tz_id}")
async def get_timezone(tz_id: int, db: AsyncSession = Depends(get_db)) -> TimezoneSchema:
    return await TimezoneActions.get_by_id(db, tz_id)

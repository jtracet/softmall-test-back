from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.settings.actions import SettingsActions, SettingsDictActions
from src.settings.schemas import SettingCreateSchema, SettingSchema, SettingsDictCreateSchema, SettingsDictSchema

settings_router = APIRouter()


@settings_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_setting(data: SettingCreateSchema, db: AsyncSession = Depends(get_db)) -> SettingSchema:
    return await SettingsActions.create_setting(db, data)


@settings_router.get("/{setting_id}")
async def get_setting(setting_id: int, db: AsyncSession = Depends(get_db)) -> SettingSchema:
    return await SettingsActions.get_setting(db, setting_id)


@settings_router.put("/{setting_id}")
async def update_setting(
    setting_id: int, data: SettingCreateSchema, db: AsyncSession = Depends(get_db)
) -> SettingSchema:
    return await SettingsActions.update_setting(db, setting_id, data.dict())


@settings_router.post("/dict", status_code=status.HTTP_201_CREATED)
async def create_settings_dict(
    data: SettingsDictCreateSchema, db: AsyncSession = Depends(get_db)
) -> SettingsDictSchema:
    return await SettingsDictActions.create_settings_dict(db, data)

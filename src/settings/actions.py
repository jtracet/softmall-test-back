from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.dals import settings_dal, settings_dict_dal
from src.settings.schemas import SettingCreateSchema, SettingSchema, SettingsDictCreateSchema, SettingsDictSchema


class SettingsActions:
    @staticmethod
    async def create_setting(db: AsyncSession, data: SettingCreateSchema) -> SettingSchema:
        setting = await settings_dal.create(db, data.dict())
        return SettingSchema.from_orm(setting)

    @staticmethod
    async def get_setting(db: AsyncSession, setting_id: int) -> SettingSchema:
        setting = await settings_dal.get(db, setting_id)
        if not setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
        return SettingSchema.from_orm(setting)

    @staticmethod
    async def update_setting(db: AsyncSession, setting_id: int, data: Dict[str, Any]) -> SettingSchema:
        setting = await settings_dal.update(db, setting_id, data)
        if not setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
        return SettingSchema.from_orm(setting)


class SettingsDictActions:
    @staticmethod
    async def create_settings_dict(db: AsyncSession, data: SettingsDictCreateSchema) -> SettingsDictSchema:
        sd = await settings_dict_dal.create(db, data.dict())
        return SettingsDictSchema.from_orm(sd)

    @staticmethod
    async def get_by_code(db: AsyncSession, code: str) -> SettingsDictSchema:
        sd = await settings_dict_dal.get_by_code(db, code)
        if not sd:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings dict not found")
        return SettingsDictSchema.from_orm(sd)

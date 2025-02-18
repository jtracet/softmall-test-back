import datetime
from typing import Optional

from src.core.schemas import BaseSchema


class SettingSchema(BaseSchema):
    id: int
    setting_code_id: int
    value: str
    active_from: datetime.date
    active_to: Optional[datetime.date] = None


class SettingCreateSchema(BaseSchema):
    setting_code_id: int
    value: str
    active_from: datetime.date
    active_to: Optional[datetime.date] = None


class SettingsDictSchema(BaseSchema):
    id: int
    code: str
    name: str


class SettingsDictCreateSchema(BaseSchema):
    code: str
    name: str

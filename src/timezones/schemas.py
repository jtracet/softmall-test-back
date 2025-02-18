import datetime
from typing import Optional

from src.core.schemas import BaseSchema


class TimezoneSchema(BaseSchema):
    id: int
    timezone_name: Optional[str]
    timezone: Optional[datetime.time]


class TimezoneCreateSchema(BaseSchema):
    timezone_name: Optional[str]
    timezone: Optional[datetime.time]

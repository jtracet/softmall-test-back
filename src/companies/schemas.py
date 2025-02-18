import datetime
from typing import Optional

from src.core.schemas import BaseSchema


class CompanySchema(BaseSchema):
    id: int
    property_id: int
    name: str
    created_date: datetime.date
    inn: str
    kpp: str
    ogrn: Optional[str] = None
    bic: Optional[str] = None


class CompanyCreateSchema(BaseSchema):
    property_id: int
    name: str
    inn: str
    kpp: str
    ogrn: Optional[str] = None
    bic: Optional[str] = None

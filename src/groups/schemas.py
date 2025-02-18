from typing import Optional

from src.core.schemas import BaseSchema


class UserGroupSchema(BaseSchema):
    id: int
    company_id: int
    group_name: str
    comment: Optional[str] = None


class UserGroupCreateSchema(BaseSchema):
    company_id: int
    group_name: str
    comment: Optional[str] = None

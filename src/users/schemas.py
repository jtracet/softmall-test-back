from datetime import date
from typing import List, Optional

from pydantic import validator

from src.core.schemas import BaseSchema


class UserSchema(BaseSchema):
    id: int
    username: str
    firstname: str
    lastname: str
    patronymic: Optional[str] = None
    created_date: date
    company_id: int
    group_id: int
    timezone_id: int
    comment: Optional[str] = None

    @validator("created_date")
    def convert_date_to_str(cls, v: date | None) -> str | None:
        if v is not None:
            return v.strftime("%Y-%m-%d")
        return v


class UserCreateSchema(BaseSchema):
    username: str
    password: str
    firstname: str
    lastname: str
    patronymic: Optional[str] = None
    company_id: Optional[int] = 0
    group_id: Optional[int] = 0


class UserUpdateSchema(BaseSchema):
    firstname: Optional[str]
    lastname: Optional[str]
    patronymic: Optional[str]
    password: Optional[str]


class UsersListSchema(BaseSchema):
    total: int
    items: List[UserSchema]


class UsersRolesUpdateSchema(BaseSchema):
    role_ids: List[int]

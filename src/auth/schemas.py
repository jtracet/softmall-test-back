from typing import Optional

from src.core.schemas import BaseSchema


class SignupUserSchema(BaseSchema):
    username: str
    password: str
    firstname: str
    lastname: str
    patronymic: Optional[str] = None
    company_id: int
    group_id: int
    timezone_id: int


class SignupCompanySchema(BaseSchema):
    property_id: int
    name: str
    inn: str
    kpp: str
    ogrn: Optional[str] = None
    bic: Optional[str] = None


class SigninSchema(BaseSchema):
    username: str
    password: str


class AccessToken(BaseSchema):
    access_token: str


class RefreshToken(BaseSchema):
    refresh_token: str


class TokensPair(AccessToken, RefreshToken):
    user: BaseSchema


class ErrorResponse(BaseSchema):
    detail: str

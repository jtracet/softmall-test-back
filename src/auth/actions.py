from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dals import auth_dal
from src.auth.jwt import TokenHandler
from src.auth.schemas import AccessToken, RefreshToken, SigninSchema, SignupCompanySchema, SignupUserSchema, TokensPair
from src.config import get_app_settings
from src.core.utils import get_password_hash, verify_password
from src.models.src.modules.company import Company
from src.users.dals import user_dal
from src.users.schemas import UserSchema

settings = get_app_settings()


class AuthActions:
    @staticmethod
    async def login(data: SigninSchema, db: AsyncSession) -> TokensPair:
        user = await user_dal.get_user_by_username(db, data.username)
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_obj = UserSchema.from_orm(user)
        token_data = {"user_data": user_obj.dict()}

        access_token, _ = TokenHandler.encode_token(
            token_data, settings.JWT_ACCESS_SECRET_KEY, float(settings.JWT_ACCESS_TOKEN_EXPIRES_IN)
        )
        refresh_token, expire = TokenHandler.encode_token(
            token_data, settings.JWT_REFRESH_SECRET_KEY, float(settings.JWT_REFRESH_TOKEN_EXPIRES_IN)
        )

        await auth_dal.create_token(
            db,
            {
                "user_id": user.id,
                "token": refresh_token,
                "expires_at": expire,
                "ua": "",
                "ip": "",
                "is_unlimited": False,
            },
        )

        return TokensPair(access_token=access_token, refresh_token=refresh_token, user=user_obj)

    @staticmethod
    def refresh(token: RefreshToken) -> AccessToken:
        if TokenHandler.verify_token(token.refresh_token, settings.JWT_REFRESH_SECRET_KEY):
            new_access = TokenHandler.get_new_access_token(token.refresh_token)
            return AccessToken(access_token=new_access)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def logout(token: RefreshToken, db: AsyncSession) -> bool:
        if TokenHandler.verify_token(token.refresh_token, settings.JWT_REFRESH_SECRET_KEY):
            return await auth_dal.delete_token(db, token.refresh_token)
        return False

    @staticmethod
    async def signup_user(data: SignupUserSchema, db: AsyncSession) -> UserSchema:
        # Проверка на уникальность username
        existing = await user_dal.get_user_by_username(db, data.username)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        hashed_password = get_password_hash(data.password)
        user_data = {
            "username": data.username,
            "password": hashed_password,
            "firstname": data.firstname,
            "lastname": data.lastname,
            "patronymic": data.patronymic,
            "created_date": datetime.utcnow(),
            "company_id": data.company_id,
            "group_id": data.group_id,
            "timezone_id": data.timezone_id,
            "user_lock": False,
            "comment": "",
        }
        user = await user_dal.create(db, user_data)
        return UserSchema.from_orm(user)

    @staticmethod
    async def signup_company(data: SignupCompanySchema, db: AsyncSession) -> Company:
        company_data = {
            "property_id": data.property_id,
            "name": data.name,
            "created_date": datetime.utcnow(),
            "inn": data.inn,
            "kpp": data.kpp,
            "ogrn": data.ogrn,
            "bic": data.bic,
        }
        from src.core.dal import BaseDAL

        company_dal = BaseDAL(Company)
        company = await company_dal.create(db, company_data)
        return company

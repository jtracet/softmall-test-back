from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.actions import AuthActions
from src.auth.schemas import AccessToken, RefreshToken, SigninSchema, SignupCompanySchema, SignupUserSchema, TokensPair
from src.database import get_db

auth_router = APIRouter()


@auth_router.post("/token", summary="Получить access и refresh токены")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> TokensPair:
    signin_data = SigninSchema(username=form_data.username, password=form_data.password)
    return await AuthActions.login(signin_data, db)


@auth_router.post("/token/refresh", summary="Обновить access токен")
def refresh_token(token: RefreshToken) -> AccessToken:
    return AuthActions.refresh(token)


@auth_router.post("/logout", summary="Удалить refresh токен (logout)")
async def logout(token: RefreshToken, db: AsyncSession = Depends(get_db)) -> Any:
    success = await AuthActions.logout(token, db)
    if not success:
        raise HTTPException(status_code=400, detail="Logout failed")
    return {"detail": "Logged out successfully"}


@auth_router.post("/signup/user", summary="Регистрация пользователя")
async def signup_user(data: SignupUserSchema, db: AsyncSession = Depends(get_db)) -> Any:
    user = await AuthActions.signup_user(data, db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"detail": "User registered", "user": user.dict()}
    )


@auth_router.post("/signup/company", summary="Регистрация компании")
async def signup_company(data: SignupCompanySchema, db: AsyncSession = Depends(get_db)) -> Any:
    company = await AuthActions.signup_company(data, db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"detail": "Company registered", "company": company.name}
    )

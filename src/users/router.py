from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users.actions import UserActions
from src.users.schemas import UserCreateSchema, UserSchema, UsersListSchema, UsersRolesUpdateSchema, UserUpdateSchema

users_router = APIRouter()


@users_router.get("/")
async def list_users(db: AsyncSession = Depends(get_db)) -> UsersListSchema:
    return await UserActions.get_all(db)


@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> UserSchema:
    return await UserActions.create(db, data)


@users_router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserSchema:
    return await UserActions.get_by_id(db, user_id)


@users_router.patch("/{user_id}")
async def update_user(user_id: int, data: UserUpdateSchema, db: AsyncSession = Depends(get_db)) -> UserSchema:
    return await UserActions.update(db, user_id, data)


@users_router.post("/{user_id}/roles")
async def assign_roles(user_id: int, data: UsersRolesUpdateSchema, db: AsyncSession = Depends(get_db)) -> Any:
    success = await UserActions.assign_roles(db, user_id, data)
    if success:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Roles assigned"})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role assignment failed")

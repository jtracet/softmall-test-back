from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.groups.actions import UserGroupActions
from src.groups.schemas import UserGroupCreateSchema, UserGroupSchema

groups_router = APIRouter()


@groups_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_group(data: UserGroupCreateSchema, db: AsyncSession = Depends(get_db)) -> UserGroupSchema:
    return await UserGroupActions.create(db, data)


@groups_router.get("/{group_id}")
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)) -> UserGroupSchema:
    return await UserGroupActions.get_by_id(db, group_id)

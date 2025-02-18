from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.groups.dals import user_group_dal
from src.groups.schemas import UserGroupCreateSchema, UserGroupSchema


class UserGroupActions:
    @staticmethod
    async def create(db: AsyncSession, data: UserGroupCreateSchema) -> UserGroupSchema:
        group = await user_group_dal.create(db, data.dict())
        return UserGroupSchema.from_orm(group)

    @staticmethod
    async def get_by_id(db: AsyncSession, group_id: int) -> UserGroupSchema:
        group = await user_group_dal.get(db, group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User group not found")
        return UserGroupSchema.from_orm(group)

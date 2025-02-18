from datetime import datetime

from fastapi import HTTPException, status
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils import get_password_hash
from src.users.dals import user_dal, users_roles_dal
from src.users.schemas import UserCreateSchema, UserSchema, UsersListSchema, UsersRolesUpdateSchema, UserUpdateSchema


class UserActions:
    @staticmethod
    async def get_all(db: AsyncSession) -> UsersListSchema:
        users = await user_dal.get_multi(db)
        total = len(users)
        return UsersListSchema(total=total, items=parse_obj_as(list[UserSchema], users))

    @staticmethod
    async def create(db: AsyncSession, data: UserCreateSchema) -> UserSchema:
        data_dict = data.dict()
        data_dict["password"] = get_password_hash(data_dict["password"])
        data_dict["created_date"] = datetime.utcnow()
        user = await user_dal.create(db, data_dict)
        return UserSchema.from_orm(user)

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> UserSchema:
        user = await user_dal.get(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserSchema.from_orm(user)

    @staticmethod
    async def update(db: AsyncSession, user_id: int, data: UserUpdateSchema) -> UserSchema:
        update_data = data.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["password"] = get_password_hash(update_data["password"])
        user = await user_dal.update(db, user_id, update_data)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserSchema.from_orm(user)

    @staticmethod
    async def assign_roles(db: AsyncSession, user_id: int, data: UsersRolesUpdateSchema) -> bool:
        existing_roles = await users_roles_dal.get_multi(db, search_data={"user_id": user_id})
        for role in existing_roles:
            await users_roles_dal.delete(db, role.id)
        for role_id in data.role_ids:
            await users_roles_dal.create(
                db, {"user_id": user_id, "role_id": role_id, "active_from": datetime.utcnow(), "active_to": None}
            )
        return True

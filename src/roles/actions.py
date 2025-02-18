from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.roles.dals import function_dal, role_function_dal, roles_dal
from src.roles.schemas import (
    FunctionCreateSchema,
    FunctionSchema,
    RoleCreateSchema,
    RoleFunctionsAssignSchema,
    RoleSchema,
)


class RoleActions:
    @staticmethod
    async def create_role(db: AsyncSession, data: RoleCreateSchema) -> RoleSchema:
        role = await roles_dal.create(db, data.dict())
        return RoleSchema.from_orm(role)

    @staticmethod
    async def get_role(db: AsyncSession, role_id: int) -> RoleSchema:
        role = await roles_dal.get(db, role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return RoleSchema.from_orm(role)


class FunctionActions:
    @staticmethod
    async def create_function(db: AsyncSession, data: FunctionCreateSchema) -> FunctionSchema:
        func = await function_dal.create(db, data.dict())
        return FunctionSchema.from_orm(func)


class RoleFunctionActions:
    @staticmethod
    async def assign_functions(db: AsyncSession, data: RoleFunctionsAssignSchema) -> bool:
        existing = await role_function_dal.get_multi(db, search_data={"role_id": data.role_id})
        for rf in existing:
            await role_function_dal.delete(db, rf.id)
        for func_id in data.function_ids:
            await role_function_dal.create(db, {"role_id": data.role_id, "function_code_id": func_id})
        return True

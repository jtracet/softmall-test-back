from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dal import BaseDAL
from src.models.src.modules.roles import FunctionDict, RoleFunction, RolesDict


class RolesDAL(BaseDAL[RolesDict]):
    async def get_by_code(self, db: AsyncSession, code: str) -> RolesDict | None:
        query = select(RolesDict).where(RolesDict.code == code)
        result = await db.execute(query)
        return result.scalars().first()


roles_dal = RolesDAL(RolesDict)


class RoleFunctionDAL(BaseDAL[RoleFunction]):
    pass


role_function_dal = RoleFunctionDAL(RoleFunction)


class FunctionDAL(BaseDAL[FunctionDict]):
    async def get_by_code(self, db: AsyncSession, code: str) -> FunctionDict | None:
        query = select(FunctionDict).where(FunctionDict.code == code)
        result = await db.execute(query)
        return result.scalars().first()


function_dal = FunctionDAL(FunctionDict)

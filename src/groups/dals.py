from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dal import BaseDAL
from src.models.src.modules.user import UserGroup


class UserGroupDAL(BaseDAL[UserGroup]):
    async def get_by_company(self, db: AsyncSession, company_id: int) -> list[UserGroup]:
        query = select(UserGroup).where(UserGroup.company_id == company_id)
        result = await db.execute(query)
        return result.scalars().all()  # type: ignore


user_group_dal = UserGroupDAL(UserGroup)

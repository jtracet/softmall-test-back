from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dal import BaseDAL
from src.models.src.modules.company import Company


class CompanyDAL(BaseDAL[Company]):
    async def get_by_inn(self, db: AsyncSession, inn: str) -> Company | None:
        query = select(Company).where(Company.inn == inn)
        result = await db.execute(query)
        return result.scalars().first()


company_dal = CompanyDAL(Company)

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.companies.dals import company_dal
from src.companies.schemas import CompanyCreateSchema, CompanySchema


class CompanyActions:
    @staticmethod
    async def create(db: AsyncSession, data: CompanyCreateSchema) -> CompanySchema:
        data_dict = data.dict()
        data_dict["created_date"] = datetime.utcnow().date()
        company = await company_dal.create(db, data_dict)
        return CompanySchema.from_orm(company)

    @staticmethod
    async def get_by_id(db: AsyncSession, company_id: int) -> CompanySchema:
        company = await company_dal.get(db, company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return CompanySchema.from_orm(company)

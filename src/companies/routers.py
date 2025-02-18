from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.companies.actions import CompanyActions
from src.companies.schemas import CompanyCreateSchema, CompanySchema
from src.database import get_db

companies_router = APIRouter()


@companies_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(data: CompanyCreateSchema, db: AsyncSession = Depends(get_db)) -> CompanySchema:
    return await CompanyActions.create(db, data)


@companies_router.get("/{company_id}")
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)) -> CompanySchema:
    return await CompanyActions.get_by_id(db, company_id)

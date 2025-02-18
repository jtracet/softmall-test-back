from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.roles.actions import FunctionActions, RoleActions, RoleFunctionActions
from src.roles.schemas import (
    FunctionCreateSchema,
    FunctionSchema,
    RoleCreateSchema,
    RoleFunctionsAssignSchema,
    RoleSchema,
)

roles_router = APIRouter()


@roles_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleCreateSchema, db: AsyncSession = Depends(get_db)) -> RoleSchema:
    return await RoleActions.create_role(db, data)


@roles_router.get("/{role_id}")
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)) -> RoleSchema:
    return await RoleActions.get_role(db, role_id)


@roles_router.post("/functions", status_code=status.HTTP_201_CREATED)
async def create_function(data: FunctionCreateSchema, db: AsyncSession = Depends(get_db)) -> FunctionSchema:
    return await FunctionActions.create_function(db, data)


@roles_router.post("/assign-functions")
async def assign_functions(data: RoleFunctionsAssignSchema, db: AsyncSession = Depends(get_db)) -> Any:
    success = await RoleFunctionActions.assign_functions(db, data)
    if success:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Functions assigned"})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignment failed")

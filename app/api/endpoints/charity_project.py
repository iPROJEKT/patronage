from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.core.db import get_async_session
from app.schemas.charity_project import (
    CharityProjectBD,
    CharityProjectCreate
)
from app.crud.charity_project import charity_project_crud
from app.api.endpoints.validater import check_name_duplicate, execute_investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectBD],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
):
    all_project = await charity_project_crud.get_multi(session)
    return all_project


@router.post(
    '/',
    response_model=CharityProjectBD,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(
        charity_project.name, session
    )
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await execute_investment_process(
        new_charity_project, session
    )
    await session.refresh(new_charity_project)
    return new_charity_project

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.core.db import get_async_session
from app.schemas.charity_project import (
    CharityProjectBD,
    CharityProjectCreate,
    CharityProjectUpdate
)
from app.crud.charity_project import charity_project_crud
from app.api.endpoints.validater import (
    check_name_duplicate,
    check_charity_project_exists,
    check_project_was_invested,
    check_project_was_closed,
    check_project_name_donation_updata,
    check_full_mount
)
from app.core.services import investment

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectBD],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


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
    await check_full_mount(
        charity_project.full_amount
    )
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    investment(
        new_charity_project,
        await charity_project_crud.get_not_invested_objects(
            new_charity_project,
            session
        )
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectBD,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_exists(project_id, session)
    await check_project_was_invested(project_id, session)
    return await (charity_project_crud.remove(await charity_project_crud.get_by_id(project_id, session), session))


@router.patch(
    '/{project_id}',
    response_model=CharityProjectBD,
    dependencies=[Depends(current_superuser)],
)
async def patch_charity_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_exists(project_id, session)
    await check_project_was_closed(project_id, session)
    if charity_project.full_amount is not None:
        await check_project_name_donation_updata(project_id, charity_project.full_amount, session)
    if charity_project.name is not None:
        await check_name_duplicate(charity_project.name, session)
    return await charity_project_crud.update(
        await charity_project_crud.get_by_id(
            project_id,
            session
        ),
        charity_project,
        session
    )

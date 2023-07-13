from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
) -> None:
    charity_project_id = await (
        charity_project_crud.get_charity_project_id_by_name(
            project_name=project_name, session=session
        )
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_by_id(project_id, session)
    if project_id is None:
        raise HTTPException(
            status_code=404,
            detail='Проекта с таким id не существует'
        )
    return project_id


async def check_project_was_invested(
    project_id: int,
    session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_by_id(project_id, session)
    if project_id.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )

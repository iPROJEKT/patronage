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
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_by_id(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проекта с таким id не существует'
        )


async def check_project_was_invested(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_by_id(project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_project_was_closed(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_by_id(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_project_name_donation_updata(
    project_id: int,
    charity_project_full_amount,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_by_id(project_id, session)
    if charity_project.invested_amount > charity_project_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя менять сретсва'
        )


async def check_correct_donation(
    donation_full_amount: int
) -> None:
    if donation_full_amount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Сумма пожертвований должна быть больше нуля'
        )


async def check_full_mount(
    project_full_mount: int
) -> None:
    if project_full_mount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Сумма пожертвований должна быть больше нуля'
        )

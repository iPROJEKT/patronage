from http import HTTPStatus


from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation


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
            detail=f'Проект с именем "{project_name}"уже сущесвует'
        )


async def get_not_invested_objects(
    model_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    db_objects = await session.execute(
        select(
            model_in
        ).where(
            model_in.fully_invested == False
        ).order_by(
            model_in.create_date
        )
    )
    return db_objects.scalars().all()


async def close_invested_object(
    obj_to_close: Union[CharityProject, Donation],
) -> None:
    obj_to_close.fully_invested = True
    obj_to_close.close_date = datetime.now()


async def execute_investment_process(
    object_in: Union[CharityProject, Donation],
    session: AsyncSession
):
    db_model = (
        CharityProject if isinstance(object_in, Donation) else Donation
    )
    not_invested_objects = await get_not_invested_objects(db_model, session)
    available_amount = object_in.full_amount

    if not_invested_objects:
        for not_invested_obj in not_invested_objects:
            need_to_invest = not_invested_obj.full_amount - not_invested_obj.invested_amount
            to_invest = (
                need_to_invest if need_to_invest < available_amount else available_amount
            )
            not_invested_obj.invested_amount += to_invest
            object_in.invested_amount += to_invest
            available_amount -= to_invest

            if not_invested_obj.full_amount == not_invested_obj.invested_amount:
                await close_invested_object(not_invested_obj)

            if not available_amount:
                await close_invested_object(object_in)
                break
        await session.commit()
    return object_in

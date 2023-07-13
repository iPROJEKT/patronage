from datetime import datetime
from typing import List, Union, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_charity_project_id_by_name(
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        charity_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return charity_project.scalars().first()

    @staticmethod
    async def get_not_invested_objects(
            model_in: Union[CharityProject, Donation],
            session: AsyncSession
    ) -> List[Union[CharityProject, Donation]]:
        db_objects = await session.execute(
            select(
                model_in
            ).where(
                model_in.fully_invested == 0
            ).order_by(
                model_in.create_date
            )
        )
        return db_objects.scalars().all()

    @staticmethod
    async def close_invested_object(
            obj_to_close: Union[CharityProject, Donation],
    ) -> None:
        obj_to_close.fully_invested = True
        obj_to_close.close_date = datetime.now()

    @staticmethod
    async def execute_investment_process(
            object_in: Union[CharityProject, Donation],
            session: AsyncSession
    ):
        model = (
            CharityProject if isinstance(object_in, Donation) else Donation
        )
        not_invested_objects = await CRUDCharityProject.get_not_invested_objects(model, session)
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
                    await CRUDCharityProject.close_invested_object(not_invested_obj)

                if not available_amount:
                    await CRUDCharityProject.close_invested_object(object_in)
                    break
            await session.commit()
        return object_in


charity_project_crud = CRUDCharityProject(CharityProject)

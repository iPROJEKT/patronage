from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_not_invested_objects(
        type_obj: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> List[Union[CharityProject, Donation]]:
        model = (
            CharityProject if isinstance(type_obj, Donation) else Donation
        )
        db_objects = await session.execute(
            select(
                model
            ).where(
                model.fully_invested == False
            ).order_by(
                model.create_date
            )
        )
        return db_objects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)

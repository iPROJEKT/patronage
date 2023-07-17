from datetime import datetime
from typing import List, Union, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation


class CRUDCharityProject(CRUDBase):

    @staticmethod
    def get_model(
        model
    ):
        return(
            CharityProject if isinstance(model, Donation) else Donation
        )

    @staticmethod
    async def update(
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

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
        type_obj: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> List[Union[CharityProject, Donation]]:
        db_objects = await session.execute(
            select(
                CRUDCharityProject.get_model(type_obj)
            ).where(
                CRUDCharityProject.get_model(type_obj).fully_invested == 0
            ).order_by(
                CRUDCharityProject.get_model(type_obj).create_date
            )
        )
        return db_objects.scalars().all()

    @staticmethod
    def close_invested_object(
        obj_to_close: Union[CharityProject, Donation],
    ) -> None:
        obj_to_close.fully_invested = True
        obj_to_close.close_date = datetime.now()

    @staticmethod
    def investment(
        target: Union[CharityProject, Donation],
        sources: Union[CharityProject, Donation]
    ):
        if sources:
            for not_invested_obj in sources:
                need_to_invest = not_invested_obj.full_amount - not_invested_obj.invested_amount

                to_invest = (
                    need_to_invest if need_to_invest < target.full_amount else target.full_amount
                )

                not_invested_obj.invested_amount += to_invest
                target.invested_amount += to_invest
                target.full_amount -= to_invest

                if not_invested_obj.full_amount == not_invested_obj.invested_amount:
                    CRUDCharityProject.close_invested_object(not_invested_obj)
                if not target.full_amount:
                    CRUDCharityProject.close_invested_object(target)
                    break
        return target


charity_project_crud = CRUDCharityProject(CharityProject)

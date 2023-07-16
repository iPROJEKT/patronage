from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.user import User
from app.models.donation import Donation


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def get_by_id(self, object_in, session: AsyncSession):
        db_objects = await session.execute(
            select(
                self.model
            ).where(
                self.model.id == object_in
            )
        )
        return db_objects.scalars().first()

    async def create(
            self,
            object_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        object_in_data = object_in.dict()

        if user is not None:
            object_in_data['user_id'] = user.id

        db_object = self.model(**object_in_data)

        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    @staticmethod
    async def remove(
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @staticmethod
    async def get_donations_by_user(
            session: AsyncSession,
            user: User
    ) -> List[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

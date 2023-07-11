from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

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
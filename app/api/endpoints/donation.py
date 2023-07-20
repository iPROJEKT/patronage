from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import DonationDB, DonationCreate
from app.models.user import User
from app.api.endpoints.validater import check_correct_donation
from app.core.services import investment


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True
)
async def get_all_donations_superuser(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={'user_id', 'invested_amount', 'fully_invested', 'close_date'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={'user_id', 'invested_amount', 'fully_invested', 'close_date'},
    response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    await check_correct_donation(donation.full_amount)
    new_donation = await donation_crud.create(
        donation, session, user
    )
    investment(
        new_donation,
        await charity_project_crud.get_not_invested_objects(
            new_donation,
            session
        )
    )
    await session.commit()
    await session.refresh(new_donation)

    return new_donation

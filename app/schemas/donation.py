from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field
from app.schemas.charity_project import FROM_TIME, TO_TIME


class DonationBase(BaseModel):
    full_amount: int = Field(..., example=100)
    comment: Optional[str] = Field(..., example='На помощь бэкенд разрабам')
    id: int = Field(..., example=100)
    create_date: datetime = Field(..., example=FROM_TIME)


class DonationBD(DonationBase):
    user_id: int = Field(..., example=100)
    full_amount: int = Field(..., example=100)
    fully_invested: bool = Field(False, example=False)
    close_date: datetime = Field(..., example=TO_TIME)

    class Config:
        orm_mode = True

from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field, Extra

from app.core.const import (
    MIN_LEGTH_PROJEKT,
    MAX_LEGTH_PROJEKT,
    START_INVERSED_AMOUNT,
    FROM_TIME,
    TO_TIME,
)


class CharityProjectBase(BaseModel):
    name: str = Field(min_length=MIN_LEGTH_PROJEKT, max_length=MAX_LEGTH_PROJEKT)
    description: str = Field(min_length=MIN_LEGTH_PROJEKT, example='На помощь бэкенд разрабам')
    full_amount: int = Field(gt=0, example=10000)

    class Config:
        extra = Extra.forbid


class CharityProjectBD(CharityProjectBase):
    id: int
    invested_amount: int = Field(START_INVERSED_AMOUNT, example=100)
    fully_invested: bool
    create_date: datetime = Field(example=FROM_TIME)
    close_date: Optional[datetime] = Field(example=TO_TIME)

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=MIN_LEGTH_PROJEKT, max_length=MAX_LEGTH_PROJEKT)
    description: Optional[str] = Field(None, min_length=MIN_LEGTH_PROJEKT, example='На помощь бэкенд разрабам')
    full_amount: Optional[int] = Field(None, gt=0, example=10000)

    class Config:
        extra = Extra.forbid

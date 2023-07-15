from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field, Extra


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, example='На помощь бэкенд разрабам')
    full_amount: int = Field(..., gt=0, example=10000)

    class Config:
        extra = Extra.forbid


class CharityProjectBD(CharityProjectBase):
    id: int
    invested_amount: int = Field(0, example=100)
    fully_invested: bool
    create_date: datetime = Field(..., example=FROM_TIME)
    close_date: Optional[datetime] = Field(..., example=TO_TIME)

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, example='На помощь бэкенд разрабам')
    full_amount: Optional[int] = Field(None, gt=0, example=10000)

    class Config:
        extra = Extra.forbid

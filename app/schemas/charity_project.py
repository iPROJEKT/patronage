from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field, validator, Extra


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, example='На помощь бэкенд разрабам')
    full_amount: int = Field(..., example=100)

    class Config:
        extra = Extra.forbid


class CharityProjectBD(CharityProjectBase):
    id: int = Field(..., example=100)
    invested_amount: int = Field(0, example=100)
    fully_invested: bool = Field(False, example=False)
    create_date: datetime = Field(..., example=FROM_TIME)

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    @validator('name')
    def valid_name(cls, value: str):
        if value == '':
            raise ValueError('Не может быть пустым')
        if len(value) > 100:
            raise ValueError('Не может привышать 100 символов')
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value

    @validator('description')
    def valid_description(cls, value: str):
        if len(value) < 1:
            raise ValueError('Описание проекта должно содеражть не менее одного символа')


class CharityProjectUpdate(CharityProjectBase):
    pass

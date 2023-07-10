from datetime import datetime, timedelta

from pydantic import BaseModel, Field, validator, root_validator


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., example='На помощь бэкенд разрабам')
    full_amount: int = Field(..., example=100)
    id: int = Field(..., example=100)
    invested_amount: int = Field(0, example=100)
    fully_invested: bool = Field(False, example=False)
    create_date: datetime = Field(..., example=FROM_TIME)
    close_date: datetime = Field(..., example=TO_TIME)

    @validator('name')
    def valid_name(cls, value: str):
        if value == '':
            raise ValueError('Не может быть пустым')
        if len(value) > 100:
            raise ValueError('Не может привышать 100 символов')
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value

    @root_validator(skip_on_failure=True)
    def check_invested_amount(cls, value):
        if value['invested_amount'] > value['full_amount']:
            raise ValueError('Инвестированных средсв не может быть больше чем запрошено')

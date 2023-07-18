from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra
from sqlalchemy.orm import validates


class DonationBase(BaseModel):
    full_amount: Optional[int]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: int


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    @validates("full_amount")
    def validate_full_amount(self, key, full_amount):
        if full_amount < self.invested_amount:
            raise ValueError("Нельзя установить требуемую сумму меньше уже вложенной")
        return full_amount

    class Config:
        orm_mode = True

from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime

from app.core.db import Base
from app.core.const import MAX_LEGTH_PROJEKT


class CharityProject(Base):
    """
    У меня из-за CheckConstraint не проходят тесты,(логика тестов нарушается) и на gt=0 тоже
    Поэтому я вынес историю с валидацией full_amount в валидатор endponits
    """
    name = Column(String(MAX_LEGTH_PROJEKT), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

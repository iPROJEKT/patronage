from datetime import datetime

from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

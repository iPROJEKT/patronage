from sqlalchemy import Column, String, Text

from app.models.base import BaseModel
from app.core.const import MAX_LEGTH_PROJEKT


class CharityProject(BaseModel):
    name = Column(String(MAX_LEGTH_PROJEKT), unique=True, nullable=False)
    description = Column(Text, nullable=False)

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    pass


charity_project_crud = CRUDCharityProject(CharityProject)

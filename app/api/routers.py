from fastapi import APIRouter

# Через __init__ не проходит PEP 8
from app.api.endpoints.user import router as user_router
from app.api.endpoints.charity_project import router as charity_project_router
from app.api.endpoints.donation import router as donation_router

main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['Charity Project']
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donation']
)
main_router.include_router(user_router)

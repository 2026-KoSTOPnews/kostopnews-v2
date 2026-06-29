from fastapi import APIRouter

from app.apis.company_router import router as company_router
from app.apis.user_router import router as user_router
from app.apis.daily_router import router as daily_router

api_router = APIRouter(prefix="/api")

api_router.include_router(company_router)
api_router.include_router(user_router)
api_router.include_router(daily_router)
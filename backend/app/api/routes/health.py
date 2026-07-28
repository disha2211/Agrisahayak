from fastapi import APIRouter

from app.services.health_service import HealthService


router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "Welcome to AgriSahayak AI 🚜"
    }


@router.get("/health")
async def health():
    return HealthService.get_health_status()
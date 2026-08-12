from fastapi import APIRouter

from app.services.health_service import HealthService
from app.core.tools import tool_registry


router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "Welcome to AgriSahayak AI 🚜"
    }


@router.get("/health")
async def health():
    return HealthService.get_health_status()

@router.get("/tools")
async def tools():

    return [
        {
            "name": tool.name,
            "description": tool.description,
        }
        for tool in tool_registry.list_tools()
    ]
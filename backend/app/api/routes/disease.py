from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies import get_disease_service
from app.services.disease_service import DiseaseService

router = APIRouter(
    prefix="/disease",
    tags=["Disease Detection"]
)


@router.get("/status")
async def status(
    service: DiseaseService = Depends(get_disease_service)
):

    return {
        "model_loaded": True,
        "service": service.__class__.__name__
    }
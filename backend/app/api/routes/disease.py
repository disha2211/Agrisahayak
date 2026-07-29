import shutil
from pathlib import Path
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)

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

@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    service: DiseaseService = Depends(get_disease_service)
):

    return await service.analyze(file)
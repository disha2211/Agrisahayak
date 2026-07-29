import shutil
from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile


from app.api.dependencies import get_disease_service
from app.services.disease_service import DiseaseService

router = APIRouter(
    prefix="/disease",
    tags=["Disease Detection"]
)

UPLOAD_DIR = Path("temp")

UPLOAD_DIR.mkdir(exist_ok=True)

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

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    result = service.predict(str(file_path))

    return result
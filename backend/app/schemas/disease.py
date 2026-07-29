from pydantic import BaseModel


class DiseasePrediction(BaseModel):
    disease: str
    confidence: float


class DiseaseResponse(BaseModel):
    success: bool
    predictions: list[DiseasePrediction]
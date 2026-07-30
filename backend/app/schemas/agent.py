from pydantic import BaseModel


class DiseaseAnalysis(BaseModel):

    crop: str

    disease: str

    confidence: float

    severity: str

    recommended_action: str

    needs_weather: bool

    needs_rag: bool
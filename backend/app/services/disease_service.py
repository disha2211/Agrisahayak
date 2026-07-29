from app.models.disease_model import DiseaseModel
from app.schemas.disease import (
    DiseasePrediction,
    DiseaseResponse
)


class DiseaseService:

    def __init__(self):

        self.model = DiseaseModel(
            model_path="yolov8n.pt"
        )

    def predict(self, image_path):

        predictions = self.model.predict(image_path)

        return DiseaseResponse(
            success=True,
            predictions=[
                DiseasePrediction(**p)
                for p in predictions
            ]
        )
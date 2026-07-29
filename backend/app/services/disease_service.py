from app.models.disease_model import DiseaseModel
from app.utils.file_manager import FileManager
from app.utils.validators import ImageValidator
from app.schemas.disease import (
    DiseasePrediction,
    DiseaseResponse
)
from app.core.registry import model_registry

class DiseaseService:

    def __init__(self):

        self.model = model_registry.get(
            "disease"
        )

    async def analyze(self, file):
        extension = await ImageValidator.validate(file)
        

        path = FileManager.save_upload(
                file,
                extension,
            )

        try:

            predictions = self.model.predict(str(path))

            return DiseaseResponse(
                        success=True,
                        predictions=[
                            DiseasePrediction(**p)
                            for p in predictions
                        ]
                    )

        finally:

                FileManager.delete(path)

    

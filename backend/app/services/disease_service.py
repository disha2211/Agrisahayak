from app.models.disease_model import DiseaseModel
from app.utils.file_manager import FileManager
from app.utils.validators import ImageValidator
from app.schemas.disease import (
    DiseasePrediction,
    DiseaseResponse
)
from app.core.registry import model_registry
from app.agents.disease_agent import DiseaseAgent

class DiseaseService:

    def __init__(self):

        self.model = model_registry.get(
            "disease"
        )

        self.agent = DiseaseAgent()

    async def analyze(self, file):
        extension = await ImageValidator.validate(file)
        

        path = FileManager.save_upload(
                file,
                extension,
            )

        try:

            predictions = self.model.predict(str(path))

            if not predictions:
                 return {
                        "success": False,
                        "message": "No disease detected."
                    }
            analysis = self.agent.analyze(predictions[0])

            return analysis

        finally:

                FileManager.delete(path)

    

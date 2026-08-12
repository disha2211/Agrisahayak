from app.core.registry import model_registry
from app.tools.base import BaseTool


class DiseaseDetectionTool(BaseTool):

    name = "disease_detection"

    description = (
        "Analyze a plant image and detect possible "
        "plant diseases with confidence scores."
    )

    def __init__(self):
        self.model = model_registry.get("disease")

    def run(self, image_path: str):

        predictions = self.model.predict(image_path)

        return {
            "success": True,
            "predictions": predictions,
        }
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

    def schema(self):

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": (
                                "Path to the plant "
                                "image."
                            ),
                        },
                    },
                    "required": ["image_path"],
                },
            },
        }

    def run(self, image_path: str):

        predictions = self.model.predict(image_path)

        return {
            "success": True,
            "predictions": predictions,
        }
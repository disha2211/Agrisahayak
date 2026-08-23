from app.core.services import service_registry
from app.tools.base import BaseTool


class DiseaseDetectionTool(BaseTool):

    name = "disease_detection"

    description = (
        "Analyze a plant image and detect "
        "possible plant diseases with confidence scores. "
        "Use this tool only when an actual plant image "
        "is available."
    )

    def __init__(self):

        self.disease_service = (
            service_registry.get("disease")
        )

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
                                "Path to the actual "
                                "uploaded plant image."
                            ),
                        },
                    },
                    "required": ["image_path"],
                },
            },
        }

    def run(self, image_path: str):

        return self.disease_service.predict(
            image_path
        )

from app.core.services import service_registry
from app.tools.base import BaseTool


class DiseaseDetectionTool(BaseTool):
    name = "disease_detection"

    description = (
        "Analyze the plant image attached to the current conversation "
        "and detect possible diseases with confidence scores. "
        "Use only when an uploaded plant image is available. "
        "Do not use for text-only questions."
    )

    def __init__(self):
        self.disease_service = service_registry.get("disease")

    def schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        }

    def run(self, image_path: str):
        return self.disease_service.predict(image_path)

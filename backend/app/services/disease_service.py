from app.core.registry import model_registry
from app.utils.file_manager import FileManager
from app.utils.validators import ImageValidator


class DiseaseService:

    def __init__(self):
        self.model = model_registry.get("disease")

    async def analyze(self, file):
        """
        Run disease detection on an uploaded image.
        Used by the standalone /disease/predict endpoint.
        """

        extension = await ImageValidator.validate(file)

        path = FileManager.save_upload(
            file,
            extension,
        )

        try:
            predictions = self.model.predict(
                str(path)
            )

            if not predictions:
                return {
                    "success": False,
                    "message": "No disease detected.",
                }

            return {
                "success": True,
                "predictions": predictions,
            }

        finally:
            FileManager.delete(path)

    def predict(self, image_path: str):
        """
        Run disease detection on an existing image path.

        Used by DiseaseDetectionTool.
        """

        predictions = self.model.predict(
            image_path
        )

        if not predictions:
            return {
                "success": False,
                "message": "No disease detected.",
            }

        return {
            "success": True,
            "predictions": predictions,
        }
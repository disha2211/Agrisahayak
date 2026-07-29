from pathlib import Path

from ultralytics import YOLO


class DiseaseModel:

    def __init__(self, model_path: str):

        self.model_path = Path(model_path)

        self.model = YOLO(self.model_path)

    def predict(self, image_path: str):

        results = self.model.predict(
            source=image_path,
            verbose=False
        )

        return results
from pathlib import Path

from ultralytics import YOLO

from app.exceptions.disease import (
    ModelNotLoadedException,
)


class DiseaseModel:

    def __init__(self, model_path):

        path = Path(model_path)

        if not path.exists():

            raise ModelNotLoadedException(
                f"{model_path} not found."
            )

        self.model = YOLO(path)

    def predict(self, image_path: str):

        results = self.model.predict(
            source=image_path,
            verbose=False
        )

        output = []

        result = results[0]
        names = result.names

        for box in result.boxes:
            cls = int(box.cls.item())
            confidence = float(box.conf.item())
            disease_name = names[cls]
            output.append(
                 {
                "disease": disease_name,
                "confidence": round(confidence, 3)
            }
        )



        return output
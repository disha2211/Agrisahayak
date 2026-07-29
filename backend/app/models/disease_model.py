from pathlib import Path

from ultralytics import YOLO

from app.exceptions.disease import (
    ModelNotLoadedException,
)
from app.core.logger import logger

class DiseaseModel:

    def __init__(self, model_path: str):

        self.model_path = Path(model_path)

        logger.info(
            f"Loading Disease Model: {self.model_path}"
        )

        self.model = YOLO(
            self.model_path
        )

        logger.success(
            "Disease model ready."
        )
        

    def predict(self, image_path: str):

        logger.info(
            f"Running inference: {image_path}"
        )


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
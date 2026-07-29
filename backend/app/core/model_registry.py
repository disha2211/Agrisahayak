from typing import Any

from app.core.logger import logger
from app.core.config import settings
from app.models.disease_model import DiseaseModel


class ModelRegistry:

    def __init__(self):

        self.models: dict[str, Any] = {}

    def load_models(self):

        logger.info("Loading AI models...")

        self.models["disease"] = DiseaseModel(
            settings.DISEASE_MODEL_PATH
        )

        logger.success("Disease model loaded.")

    def get(self, name: str):

        if name not in self.models:

            raise ValueError(
                f"Model '{name}' not found."
            )

        return self.models[name]
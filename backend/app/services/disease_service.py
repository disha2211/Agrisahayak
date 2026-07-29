from app.models.disease_model import DiseaseModel


class DiseaseService:

    def __init__(self):

        self.model = DiseaseModel(
            model_path="models/best.pt"
        )

    def predict(self, image_path):

        return self.model.predict(image_path)
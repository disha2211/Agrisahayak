from functools import lru_cache

from app.services.disease_service import DiseaseService


@lru_cache
def get_disease_service():

    return DiseaseService()
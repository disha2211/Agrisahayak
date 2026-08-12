from functools import lru_cache

from app.services.disease_service import DiseaseService
from app.agents.farmer_agent import FarmerAgent


@lru_cache
def get_disease_service():

    return DiseaseService()

@lru_cache
def get_farmer_agent():

    return FarmerAgent()
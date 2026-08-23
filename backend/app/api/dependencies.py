from functools import lru_cache
from app.core.services import service_registry
from app.agents.farmer_agent import FarmerAgent


@lru_cache
def get_disease_service():

    return service_registry.get("disease")

@lru_cache
def get_farmer_agent():

    return FarmerAgent()
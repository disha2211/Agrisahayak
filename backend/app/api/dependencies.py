from functools import lru_cache
from app.core.services import service_registry
from app.agents.farmer_agent import FarmerAgent

from app.agents.farmer_graph_agent import (
    FarmerGraphAgent,
)


@lru_cache
def get_disease_service():

    return service_registry.get("disease")

@lru_cache
def get_farmer_agent():

    return FarmerAgent()

@lru_cache
def get_farmer_graph_agent():

    return FarmerGraphAgent()
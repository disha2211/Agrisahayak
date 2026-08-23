from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.disease import router as disease_router

from app.core.config import settings
from app.core.logger import logger
from app.core.registry import model_registry
from app.core.services import service_registry
from app.core.tools import tool_registry

from app.rag.vector_store import VectorStore
from app.tools.rag_tool import (KnowledgeRetrievalTool,)

from app.services.llm_service import LLMService
from app.api.routes.chat import router as chat_router

from app.services.weather_service import WeatherService
from app.tools.weather_tool import WeatherTool

from app.services.market_service import MarketService
from app.tools.market_tool import MarketPriceTool

from app.services.disease_service import DiseaseService
from app.tools.disease_tool import DiseaseDetectionTool



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AgriSahayak AI Backend...")

    model_registry.load_models()

    service_registry.register(
    "disease",
    DiseaseService(),
)
    tool_registry.register(
    DiseaseDetectionTool()
)

    service_registry.register(
    "vector_store",
    VectorStore(),
)

    tool_registry.register(
    KnowledgeRetrievalTool()
)

    service_registry.register(
    "llm",
    LLMService(),
)

    service_registry.register(
    "weather",
    WeatherService(),
)

    tool_registry.register(
    WeatherTool()
)

    service_registry.register(
    "market",
    MarketService(),
)
    tool_registry.register(
    MarketPriceTool()
)

    logger.success("All AI models loaded.")
    
    yield
    
    logger.info("Shutting down AgriSahayak AI Backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(disease_router)
app.include_router(chat_router)
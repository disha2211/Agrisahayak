from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.disease import router as disease_router
from app.core.config import settings
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AgriSahayak AI Backend...")
    yield
    logger.info("Shutting down AgriSahayak AI Backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(disease_router)
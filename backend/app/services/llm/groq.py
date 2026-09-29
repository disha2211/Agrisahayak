from langchain_groq import ChatGroq

from app.core.config import settings
from app.core.logger import logger
from app.services.llm.base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    def __init__(self):
        logger.info(
            f"Initializing Groq model: {settings.LLM_MODEL}"
        )

        self.model = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.2,
        )

        logger.success("Groq LLM initialized.")

    def get_model(self):
        return self.model
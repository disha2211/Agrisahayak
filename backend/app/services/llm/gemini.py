from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.core.logger import logger
from app.services.llm.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):

    def __init__(self):
        logger.info(
            f"Initializing Gemini model: {settings.LLM_MODEL}"
        )

        self.model = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2,
        )

        logger.success("Gemini LLM initialized.")

    def get_model(self):
        return self.model
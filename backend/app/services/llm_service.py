from ollama import Client

from app.core.config import settings
from app.core.logger import logger


class LLMService:

    def __init__(self):

        logger.info(
            f"Initializing LLM: {settings.LLM_MODEL}"
        )

        self.client = Client(
            host=settings.OLLAMA_HOST
        )

        self.model = settings.LLM_MODEL

        logger.success(
            "LLM service initialized."
        )

    def chat(
        self,
        messages: list,
        tools: list | None = None,
    ):

        kwargs = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            kwargs["tools"] = tools

        response = self.client.chat(
            **kwargs
        )

        return response
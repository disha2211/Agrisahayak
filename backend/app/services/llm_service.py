from app.core.config import settings
from app.services.llm.gemini import GeminiProvider


class LLMService:

    def __init__(self):
        self.provider = self._create_provider()

    def _create_provider(self):
        provider = settings.LLM_PROVIDER.lower()

        if provider == "gemini":
            return GeminiProvider()

        raise ValueError(
            f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
        )

    def get_model(self):
        return self.provider.get_model()
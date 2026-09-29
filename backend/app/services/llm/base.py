from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):

    @abstractmethod
    def get_model(self) -> Any:
        raise NotImplementedError
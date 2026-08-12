from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Base interface for every AgriSahayak tool.
    """

    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        Execute the tool.
        """
        raise NotImplementedError

    @abstractmethod
    def schema(self) -> dict:
        raise NotImplementedError
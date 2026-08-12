from typing import Any


class ServiceRegistry:

    def __init__(self):

        self.services: dict[str, Any] = {}

    def register(
        self,
        name: str,
        service: Any,
    ):

        self.services[name] = service

    def get(self, name: str):

        if name not in self.services:

            raise ValueError(
                f"Service '{name}' not found."
            )

        return self.services[name]
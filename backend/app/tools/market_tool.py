from app.core.services import service_registry
from app.tools.base import BaseTool


class MarketPriceTool(BaseTool):

    name = "market_price"

    description = (
        "Get agricultural market prices for a "
        "specific crop and optionally a location."
    )

    def __init__(self):

        self.market_service = (
            service_registry.get("market")
        )

    def schema(self):

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "crop": {
                            "type": "string",
                            "description": (
                                "Crop name, such as "
                                "tomato, rice, potato, "
                                "or chilli."
                            ),
                        },
                        "location": {
                            "type": "string",
                            "description": (
                                "Optional market "
                                "location."
                            ),
                        },
                    },
                    "required": ["crop"],
                },
            },
        }

    def run(
        self,
        crop: str,
        location: str | None = None,
    ):

        return self.market_service.get_price(
            crop=crop,
            location=location,
        )
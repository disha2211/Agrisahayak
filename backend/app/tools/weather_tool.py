from app.core.services import service_registry
from app.tools.base import BaseTool


class WeatherTool(BaseTool):

    name = "weather"

    description = (
        "Get current weather and short-term forecast "
        "for a farmer's location. Use this when the "
        "farmer explicitly asks about weather or when "
        "weather conditions are relevant to farming "
        "activities such as spraying, irrigation, or "
        "field work."
    )

    def __init__(self):

        self.weather_service = (
            service_registry.get("weather")
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
                        "location": {
                            "type": "string",
                            "description": (
                                "Village, town, or city "
                                "where the farmer's field "
                                "is located."
                            ),
                        },
                        "forecast_days": {
                            "type": "integer",
                            "description": (
                                "Number of forecast days "
                                "to retrieve."
                            ),
                            "default": 3,
                        },
                    },
                    "required": ["location"],
                },
            },
        }

    async def run(
        self,
        location: str,
        forecast_days: int = 3,
    ):

        return await self.weather_service.get_forecast(
            location=location,
            forecast_days=forecast_days,
        )
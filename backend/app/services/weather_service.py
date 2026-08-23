import httpx

from app.core.logger import logger


class WeatherService:

    GEOCODING_URL = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    FORECAST_URL = (
        "https://api.open-meteo.com/v1/forecast"
    )

    async def get_coordinates(
        self,
        location: str,
    ):

        params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:

            response = await client.get(
                self.GEOCODING_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

        results = data.get("results", [])

        if not results:
            raise ValueError(
                f"Location not found: {location}"
            )

        result = results[0]

        return {
            "name": result["name"],
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "country": result.get("country"),
            "admin1": result.get("admin1"),
        }

    async def get_forecast(
        self,
        location: str,
        forecast_days: int = 3,
    ):

        coordinates = await self.get_coordinates(
            location
        )

        params = {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "wind_speed_10m"
            ),
            "hourly": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation_probability,"
                "precipitation,"
                "wind_speed_10m"
            ),
            "forecast_days": forecast_days,
            "timezone": "auto",
        }

        logger.info(
            f"Fetching weather for {location}"
        )

        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:

            response = await client.get(
                self.FORECAST_URL,
                params=params,
            )

            response.raise_for_status()

            weather = response.json()

        return {
            "location": coordinates,
            "current": weather.get(
                "current",
                {},
            ),
            "hourly": weather.get(
                "hourly",
                {},
            ),
        }
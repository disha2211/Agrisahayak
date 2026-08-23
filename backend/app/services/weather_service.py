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
            "weather": self._build_weather_summary(
                weather
            ),
        }

    def _build_weather_summary(
    self,
    weather: dict,
):
        current = weather.get("current", {})
        hourly = weather.get("hourly", {})

        times = hourly.get("time", [])
        temperatures = hourly.get(
            "temperature_2m", []
        )
        humidity = hourly.get(
            "relative_humidity_2m", []
        )
        precipitation_probability = hourly.get(
            "precipitation_probability", []
        )
        precipitation = hourly.get(
            "precipitation", []
        )
        wind = hourly.get(
            "wind_speed_10m", []
        )

        if not times:
            return {
                "current": current,
                "summary": "No hourly forecast available.",
            }

        # Group forecast into days
        daily = {}

        for i, timestamp in enumerate(times):

            date = timestamp.split("T")[0]

            if date not in daily:
                daily[date] = {
                    "temperatures": [],
                    "humidity": [],
                    "rain_probability": [],
                    "rain": [],
                    "wind": [],
                }

            daily[date]["temperatures"].append(
                temperatures[i]
            )

            daily[date]["humidity"].append(
                humidity[i]
            )

            daily[date]["rain_probability"].append(
                precipitation_probability[i]
            )

            daily[date]["rain"].append(
                precipitation[i]
            )

            daily[date]["wind"].append(
                wind[i]
            )

        forecast = []

        for date, values in daily.items():

            forecast.append(
                {
                    "date": date,
                    "min_temperature": min(
                        values["temperatures"]
                    ),
                    "max_temperature": max(
                        values["temperatures"]
                    ),
                    "max_rain_probability": max(
                        values["rain_probability"]
                    ),
                    "total_precipitation": round(
                        sum(values["rain"]),
                        2,
                    ),
                    "max_wind_speed": max(
                        values["wind"]
                    ),
                    "average_humidity": round(
                        sum(values["humidity"])
                        / len(values["humidity"]),
                        1,
                    ),
                }
            )

        return {
            "current": {
                "temperature": current.get(
                    "temperature_2m"
                ),
                "humidity": current.get(
                    "relative_humidity_2m"
                ),
                "precipitation": current.get(
                    "precipitation"
                ),
                "wind_speed": current.get(
                    "wind_speed_10m"
                ),
            },
            "forecast": forecast,
        }
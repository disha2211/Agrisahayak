import asyncio

from app.services.weather_service import (
    WeatherService,
)


async def main():

    service = WeatherService()

    result = await service.get_forecast(
        location="Guntur",
        forecast_days=3,
    )

    print(result)


if __name__ == "__main__":

    asyncio.run(main())
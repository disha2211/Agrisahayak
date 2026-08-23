from app.services.market_service import (
    MarketService,
)


service = MarketService()

result = service.get_price(
    crop="tomato",
    location="Guntur",
)

print(result)
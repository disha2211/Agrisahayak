from pathlib import Path

import pandas as pd


class MarketService:

    def __init__(self):

        self.data_path = Path(
            "data/market_prices.csv"
        )

        if not self.data_path.exists():

            raise FileNotFoundError(
                f"Market data not found: "
                f"{self.data_path}"
            )

        self.data = pd.read_csv(
            self.data_path
        )

    def get_price(
        self,
        crop: str,
        location: str | None = None,
    ):

        df = self.data[
            self.data["crop"].str.lower()
            == crop.lower()
        ]

        if location:

            location_mask = (
                df["location"]
                .str.lower()
                .str.contains(
                    location.lower(),
                    na=False,
                )
            )

            filtered = df[location_mask]

            if not filtered.empty:

                df = filtered

        if df.empty:

            return {
                "found": False,
                "crop": crop,
                "location": location,
                "message": (
                    "No market price found."
                ),
            }

        latest = df.sort_values(
            "date"
        ).iloc[-1]

        return {
            "found": True,
            "crop": latest["crop"],
            "market": latest["market"],
            "location": latest["location"],
            "price_per_kg": float(
                latest["price_per_kg"]
            ),
            "date": latest["date"],
        }
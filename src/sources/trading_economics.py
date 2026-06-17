from typing import Optional
from src.config import TRADING_ECONOMICS_API_KEY

DEMO_MARKET_PRICES = [
    {"commodity": "Wheat", "price": 215.50, "unit": "USD/ton", "change": "+2.30", "date": "2026-06-17"},
    {"commodity": "Corn", "price": 185.75, "unit": "USD/ton", "change": "-1.20", "date": "2026-06-17"},
    {"commodity": "Soybeans", "price": 425.00, "unit": "USD/ton", "change": "+3.50", "date": "2026-06-17"},
    {"commodity": "Coffee", "price": 245.80, "unit": "USD/lb", "change": "-0.85", "date": "2026-06-17"},
    {"commodity": "Cocoa", "price": 3850.00, "unit": "USD/ton", "change": "+15.00", "date": "2026-06-17"},
    {"commodity": "Sugar", "price": 0.22, "unit": "USD/lb", "change": "+0.01", "date": "2026-06-17"},
    {"commodity": "Barley", "price": 165.30, "unit": "USD/ton", "change": "-0.50", "date": "2026-06-17"},
    {"commodity": "Rice", "price": 395.00, "unit": "USD/ton", "change": "+1.20", "date": "2026-06-17"},
    {"commodity": "Cotton", "price": 0.82, "unit": "USD/lb", "change": "+0.03", "date": "2026-06-17"},
    {"commodity": "Sunflower", "price": 450.00, "unit": "USD/ton", "change": "+5.00", "date": "2026-06-17"},
]


def fetch_market_prices() -> list[dict]:
    if TRADING_ECONOMICS_API_KEY:
        try:
            import requests

            headers = {"Authorization": f"Client {TRADING_ECONOMICS_API_KEY}"}
            response = requests.get(
                "https://api.tradingeconomics.com/markets/commodities",
                headers=headers,
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                prices = []
                for item in data:
                    prices.append(
                        {
                            "commodity": item.get("Name", "Unknown"),
                            "price": item.get("Last", 0),
                            "unit": item.get("Unit", ""),
                            "change": item.get("Change", 0),
                            "date": item.get("Date", ""),
                        }
                    )
                if prices:
                    return prices
        except Exception:
            pass

    return DEMO_MARKET_PRICES


def is_demo_data() -> bool:
    return not bool(TRADING_ECONOMICS_API_KEY)

import os
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
TRADING_ECONOMICS_API_KEY = os.getenv("TRADING_ECONOMICS_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NEWS_REFRESH_INTERVAL_MINUTES = int(os.getenv("NEWS_REFRESH_INTERVAL_MINUTES", "60"))
DATABASE_PATH = os.getenv("DATABASE_PATH", "news_cache.db")

CATEGORIES = [
    "General Agriculture",
    "Weather Risk",
    "Commodities",
    "Market Prices",
    "Policy & Trade",
    "Export/Import",
    "Fertilizer & Inputs",
    "Crop Production",
    "Food Security",
]

COMMODITIES = [
    "Wheat",
    "Corn",
    "Soybeans",
    "Barley",
    "Rice",
    "Sunflower",
    "Sugar",
    "Coffee",
    "Cocoa",
    "Cotton",
    "Fertilizer",
]

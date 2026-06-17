from typing import Optional
from src.config import FIRECRAWL_API_KEY

FIRECRAWL_SOURCES = [
    {
        "name": "Reuters Agriculture",
        "url": "https://www.reuters.com/business/agriculture/",
        "default_category": "Commodities",
        "region": "Global",
        "country": "Global",
        "continent": "Global",
        "reliability": 9,
    },
    {
        "name": "Bloomberg Commodities",
        "url": "https://www.bloomberg.com/commodities",
        "default_category": "Commodities",
        "region": "Global",
        "country": "Global",
        "continent": "Global",
        "reliability": 9,
    },
    {
        "name": "Trading Economics Commodities",
        "url": "https://tradingeconomics.com/commodities",
        "default_category": "Market Prices",
        "region": "Global",
        "country": "Global",
        "continent": "Global",
        "reliability": 7,
    },
]


def fetch_firecrawl(source_config: dict) -> list[dict]:
    if not FIRECRAWL_API_KEY:
        return []

    try:
        from firecrawl import FirecrawlApp

        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        result = app.scrape_url(source_config["url"])

        if result and "data" in result:
            articles = []
            content = result["data"].get("content", "")
            title = result["data"].get("title", "")
            if title and content:
                articles.append(
                    {
                        "title": title,
                        "url": source_config["url"],
                        "source": source_config["name"],
                        "summary": content[:300] if content else "",
                        "content": content,
                        "image_url": None,
                        "published_date": None,
                        "category": source_config["default_category"],
                        "commodities": [],
                        "region": source_config["region"],
                        "country": source_config["country"],
                        "continent": source_config["continent"],
                        "reliability": source_config["reliability"],
                    }
                )
            return articles
    except Exception:
        pass

    return []


def fetch_all_firecrawl() -> list[dict]:
    all_articles = []
    for source in FIRECRAWL_SOURCES:
        articles = fetch_firecrawl(source)
        all_articles.extend(articles)
    return all_articles

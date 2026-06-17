from datetime import datetime
from src.storage.database import Database
from src.sources.rss_sources import fetch_all_rss
from src.sources.firecrawl_sources import fetch_all_firecrawl
from src.news.classifier import classify_articles
from src.news.deduplication import deduplicate
from src.config import NEWS_REFRESH_INTERVAL_MINUTES


def fetch_and_store_articles(db: Database) -> int:
    all_articles = []

    rss_articles = fetch_all_rss()
    all_articles.extend(rss_articles)

    firecrawl_articles = fetch_all_firecrawl()
    all_articles.extend(firecrawl_articles)

    all_articles = classify_articles(all_articles)

    all_articles = deduplicate(all_articles)

    db.store_articles(all_articles)

    return len(all_articles)


def get_articles(
    db: Database,
    category: str = "All",
    region: str = "Global",
    commodity: str = "All",
) -> list[dict]:
    cached = db.get_cached_articles(
        category=category if category != "All" else None,
        region=region if region != "Global" else None,
        commodity=commodity if commodity != "All" else None,
        limit=200,
    )

    if not cached:
        new_count = fetch_and_store_articles(db)
        cached = db.get_cached_articles(
            category=category if category != "All" else None,
            region=region if region != "Global" else None,
            commodity=commodity if commodity != "All" else None,
            limit=200,
        )

    return cached


def refresh_articles(db: Database) -> int:
    return fetch_and_store_articles(db)

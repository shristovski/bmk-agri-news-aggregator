from datetime import datetime, timezone
from typing import Optional
from src.geolocation import UserLocation


def calculate_relevance(
    article: dict,
    user_location: Optional[UserLocation] = None,
    selected_region: str = "Global",
    selected_country: str = "Global",
    selected_commodity: str = "All",
) -> float:
    score = 0.0
    article_region = article.get("region", "Global")
    article_continent = article.get("continent", "Global")
    article_country = article.get("country", "Global")

    if user_location and user_location.country != "Global":
        if article_country == user_location.country:
            score += 40
        elif article_region == user_location.region:
            score += 30
        elif article_continent == user_location.continent:
            score += 15

    if selected_region != "Global":
        if article_region == selected_region:
            score += 20
        elif article_continent == selected_region:
            score += 10
        elif article_region == "Global":
            score += 5

    if selected_country != "Global" and article_country == selected_country:
        score += 15

    if selected_commodity != "All":
        article_commodities = article.get("commodities", [])
        if selected_commodity in article_commodities:
            score += 25

    if user_location and user_location.country != "Global":
        article_commodities = article.get("commodities", [])
        if article_commodities:
            score += 5

    freshness = calculate_freshness(article.get("published_date", ""))
    score += freshness

    reliability = article.get("reliability", 5)
    score += reliability * 1.5

    category = article.get("category", "General Agriculture")
    if article_region == "Global" and category in ["Weather Risk", "Food Security"]:
        score += 10

    return score


def calculate_freshness(published_date: str) -> float:
    if not published_date:
        return 0.0

    try:
        pub_date = datetime.fromisoformat(published_date)
        if pub_date.tzinfo is None:
            pub_date = pub_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        days_old = (now - pub_date).days

        if days_old < 0:
            return 30.0
        if days_old <= 1:
            return 30.0
        if days_old <= 3:
            return 25.0
        if days_old <= 7:
            return 20.0
        if days_old <= 14:
            return 10.0
        return 5.0
    except Exception:
        return 15.0


def rank_articles(
    articles: list[dict],
    user_location: Optional[UserLocation] = None,
    selected_region: str = "Global",
    selected_country: str = "Global",
    selected_commodity: str = "All",
) -> list[dict]:
    scored_articles = []
    for article in articles:
        score = calculate_relevance(
            article, user_location, selected_region, selected_country, selected_commodity
        )
        article["relevance_score"] = round(score, 1)
        scored_articles.append(article)

    scored_articles.sort(key=lambda a: a.get("relevance_score", 0), reverse=True)
    return scored_articles


def filter_by_category(articles: list[dict], category: str) -> list[dict]:
    if category == "All":
        return articles
    return [a for a in articles if a.get("category") == category]

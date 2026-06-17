import feedparser
import re
import requests
from datetime import datetime
from typing import Optional


RSS_FEEDS = [
    {
        "name": "USDA News Releases",
        "url": "https://www.usda.gov/rss/latest-releases.xml",
        "default_category": "Policy & Trade",
        "region": "North America",
        "country": "USA",
        "continent": "North America",
        "reliability": 9,
    },
    {
        "name": "FAO News",
        "url": "https://www.fao.org/news/rss-feed.xml",
        "default_category": "Food Security",
        "region": "Global",
        "country": "Global",
        "continent": "Global",
        "reliability": 9,
    },
    {
        "name": "EC Agriculture News",
        "url": "https://ec.europa.eu/info/news/agriculture/rss_en",
        "default_category": "Policy & Trade",
        "region": "Western Europe",
        "country": "EU",
        "continent": "Europe",
        "reliability": 8,
    },
    {
        "name": "World Bank Agriculture",
        "url": "https://www.worldbank.org/en/news/rss/agriculture-and-food",
        "default_category": "Policy & Trade",
        "region": "Global",
        "country": "Global",
        "continent": "Global",
        "reliability": 8,
    },
    {
        "name": "AgWeb",
        "url": "https://www.agweb.com/rss/feed",
        "default_category": "Crop Production",
        "region": "North America",
        "country": "USA",
        "continent": "North America",
        "reliability": 7,
    },
    {
        "name": "Brownfield Ag News",
        "url": "https://brownfieldagnews.com/feed",
        "default_category": "Crop Production",
        "region": "North America",
        "country": "USA",
        "continent": "North America",
        "reliability": 7,
    },
    {
        "name": "Agriculture.com",
        "url": "https://www.agriculture.com/rss",
        "default_category": "General Agriculture",
        "region": "North America",
        "country": "USA",
        "continent": "North America",
        "reliability": 7,
    },
    {
        "name": "Farm Progress",
        "url": "https://www.farmprogress.com/rss/",
        "default_category": "Crop Production",
        "region": "North America",
        "country": "USA",
        "continent": "North America",
        "reliability": 7,
    },
    {
        "name": "Successful Farming",
        "url": "https://www.successfulfarming.com/rss",
        "default_category": "General Agriculture",
        "region": "North America",
        "country": "USA",
        "continent": "North America",
        "reliability": 7,
    },
    {
        "name": "Commodity.com",
        "url": "https://commodity.com/feed",
        "default_category": "Commodities",
        "region": "Global",
        "country": "Global",
        "continent": "Global",
        "reliability": 6,
    },
]


def parse_date(date_string: Optional[str]) -> str:
    if not date_string:
        return datetime.now().isoformat()

    try:
        from email.utils import parsedate_to_datetime

        dt = parsedate_to_datetime(date_string)
        return dt.isoformat()
    except Exception:
        pass

    try:
        from dateutil.parser import parse

        dt = parse(date_string)
        return dt.isoformat()
    except Exception:
        pass

    return datetime.now().isoformat()


def extract_image_url(entry) -> Optional[str]:
    if hasattr(entry, "media_content") and entry.media_content:
        for media in entry.media_content:
            if "url" in media:
                return media["url"]

    for link in getattr(entry, "links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href")

    if hasattr(entry, "summary"):
        img_match = re.search(
            r'<img[^>]+src=["\']([^"\']+)["\']', entry.summary
        )
        if img_match:
            return img_match.group(1)

    if hasattr(entry, "content"):
        for content_item in entry.content:
            if hasattr(content_item, "value"):
                img_match = re.search(
                    r'<img[^>]+src=["\']([^"\']+)["\']', content_item.value
                )
                if img_match:
                    return img_match.group(1)

    return None


def extract_summary(entry) -> str:
    if hasattr(entry, "summary") and entry.summary:
        text = re.sub(r"<[^>]+>", "", entry.summary)
        return text[:300].strip()

    if hasattr(entry, "content") and entry.content:
        for content_item in entry.content:
            if hasattr(content_item, "value") and content_item.value:
                text = re.sub(r"<[^>]+>", "", content_item.value)
                return text[:300].strip()

    if hasattr(entry, "description") and entry.description:
        text = re.sub(r"<[^>]+>", "", entry.description)
        return text[:300].strip()

    return ""


def fetch_feed(feed_config: dict) -> list[dict]:
    articles = []
    try:
        resp = requests.get(feed_config["url"], timeout=8, headers={
            "User-Agent": "Mozilla/5.0 (compatible; BMKAgriNews/1.0)"
        })
        if resp.status_code != 200:
            return []
        feed = feedparser.parse(resp.content)
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "")

            if not title or not link:
                continue

            article = {
                "title": title,
                "url": link,
                "source": feed_config["name"],
                "summary": extract_summary(entry),
                "content": entry.get("description", entry.get("summary", "")),
                "image_url": extract_image_url(entry),
                "published_date": parse_date(entry.get("published")),
                "category": feed_config["default_category"],
                "commodities": [],
                "region": feed_config["region"],
                "country": feed_config["country"],
                "continent": feed_config["continent"],
                "reliability": feed_config["reliability"],
            }
            articles.append(article)

    except Exception:
        pass

    return articles


def fetch_all_rss() -> list[dict]:
    all_articles = []
    for feed in RSS_FEEDS:
        articles = fetch_feed(feed)
        all_articles.extend(articles)
    return all_articles

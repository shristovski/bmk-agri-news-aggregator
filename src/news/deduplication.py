import re
from collections import defaultdict


def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"\b(the|a|an|in|on|at|to|for|of|and|is|are|was|were)\b", "", title)
    return title.strip()


def are_similar(title1: str, title2: str, threshold: float = 0.7) -> bool:
    norm1 = normalize_title(title1)
    norm2 = normalize_title(title2)

    if not norm1 or not norm2:
        return False

    if norm1 == norm2:
        return True

    words1 = set(norm1.split())
    words2 = set(norm2.split())

    if not words1 or not words2:
        return False

    intersection = words1 & words2
    union = words1 | words2

    jaccard = len(intersection) / len(union)
    return jaccard >= threshold


def deduplicate(articles: list[dict]) -> list[dict]:
    seen_urls = set()
    seen_titles = []
    unique_articles = []

    for article in articles:
        url = article.get("url", "")
        title = article.get("title", "")

        if not url and not title:
            continue

        if url and url in seen_urls:
            continue

        is_duplicate = False
        for seen_title in seen_titles:
            if are_similar(title, seen_title):
                is_duplicate = True
                break

        if is_duplicate:
            continue

        if url:
            seen_urls.add(url)
        seen_titles.append(title)
        unique_articles.append(article)

    return unique_articles

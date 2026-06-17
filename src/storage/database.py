import sqlite3
import json
from datetime import datetime
from typing import Optional
from src.config import DATABASE_PATH


class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_db()

    def get_conn(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    url TEXT UNIQUE,
                    source TEXT,
                    summary TEXT,
                    content TEXT,
                    image_url TEXT,
                    published_date TEXT,
                    category TEXT,
                    commodities TEXT,
                    region TEXT,
                    country TEXT,
                    continent TEXT,
                    fetched_at TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_region ON articles(region)
            """)

    def store_article(self, article: dict) -> bool:
        try:
            with self.get_conn() as conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO articles
                        (title, url, source, summary, content, image_url,
                         published_date, category, commodities, region,
                         country, continent, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        article.get("title"),
                        article.get("url"),
                        article.get("source"),
                        article.get("summary"),
                        article.get("content"),
                        article.get("image_url"),
                        article.get("published_date"),
                        article.get("category"),
                        json.dumps(article.get("commodities", [])),
                        article.get("region"),
                        article.get("country"),
                        article.get("continent"),
                        datetime.now().isoformat(),
                    ),
                )
            return True
        except Exception:
            return False

    def store_articles(self, articles: list[dict]):
        for article in articles:
            self.store_article(article)

    def get_cached_articles(
        self,
        category: Optional[str] = None,
        region: Optional[str] = None,
        commodity: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict]:
        query = "SELECT * FROM articles WHERE 1=1"
        params = []

        if category and category != "All":
            query += " AND category = ?"
            params.append(category)

        if region and region != "Global":
            query += " AND (region = ? OR continent = ?)"
            params.extend([region, region])

        if commodity and commodity != "All":
            query += " AND commodities LIKE ?"
            params.append(f"%{commodity}%")

        query += " ORDER BY published_date DESC LIMIT ?"
        params.append(limit)

        with self.get_conn() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(query, params).fetchall()

        articles = []
        for row in rows:
            article = dict(row)
            try:
                article["commodities"] = json.loads(article.get("commodities") or "[]")
            except (json.JSONDecodeError, TypeError):
                article["commodities"] = []
            articles.append(article)

        return articles

    def get_cached_article_count(self) -> int:
        with self.get_conn() as conn:
            row = conn.execute("SELECT COUNT(*) as cnt FROM articles").fetchone()
            return row[0] if row else 0

    def clear_old_articles(self, days: int = 7):
        with self.get_conn() as conn:
            conn.execute(
                "DELETE FROM articles WHERE fetched_at < datetime('now', ?)",
                (f"-{days} days",),
            )

    def get_distinct_categories(self) -> list[str]:
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT DISTINCT category FROM articles WHERE category IS NOT NULL"
            ).fetchall()
            return [row[0] for row in rows if row[0]]

    def get_distinct_regions(self) -> list[str]:
        with self.get_conn() as conn:
            rows = conn.execute(
                "SELECT DISTINCT region FROM articles WHERE region IS NOT NULL"
            ).fetchall()
            return [row[0] for row in rows if row[0]]

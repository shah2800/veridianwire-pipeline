"""Orchestrates all news fetchers with fallback chain."""
import json
import logging
import os
from pathlib import Path
from typing import Dict, List

from .newsapi import NewsAPIFetcher
from .rss import RSSFetcher
from .gdelt import GDELTFetcher

logger = logging.getLogger(__name__)

CACHE_PATH = Path(__file__).resolve().parent.parent / "logs" / "fetch_cache.json"


class FetchManager:
    """NewsAPI -> RSS -> GDELT -> cached articles."""

    def __init__(self):
        self.newsapi = NewsAPIFetcher()
        self.rss = RSSFetcher()
        self.gdelt = GDELTFetcher()
        self._cache: List[Dict] = []
        self._load_cache()
        self.last_status = {
            "newsapi": "unknown",
            "rss": "unknown",
            "gdelt": "unknown",
        }

    def _load_cache(self) -> None:
        try:
            if CACHE_PATH.exists():
                self._cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning(f"Could not load fetch cache: {e}")

    def _save_cache(self, articles: List[Dict]) -> None:
        try:
            CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            CACHE_PATH.write_text(
                json.dumps(articles[:200], ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning(f"Could not save fetch cache: {e}")

    def _dedupe_urls(self, articles: List[Dict]) -> List[Dict]:
        seen = set()
        unique = []
        for article in articles:
            url = article.get("url", "")
            if url and url not in seen:
                seen.add(url)
                unique.append(article)
        return unique

    def fetch_all_sources(self, limit: int = 100) -> List[Dict]:
        """Fetch from all sources with fallback chain."""
        all_articles: List[Dict] = []

        try:
            articles = self.newsapi.fetch_latest_news(limit=limit)
            all_articles.extend(articles)
            self.last_status["newsapi"] = "ok" if articles else "empty"
        except Exception as e:
            self.last_status["newsapi"] = "failed"
            logger.error(f"NewsAPI failed: {e}")

        try:
            articles = self.rss.fetch_all_feeds(limit=limit)
            all_articles.extend(articles)
            self.last_status["rss"] = "ok" if articles else "empty"
        except Exception as e:
            self.last_status["rss"] = "failed"
            logger.error(f"RSS failed: {e}")

        try:
            articles = self.gdelt.fetch_trending(limit=min(limit, 100))
            all_articles.extend(articles)
            self.last_status["gdelt"] = "ok" if articles else "empty"
        except Exception as e:
            self.last_status["gdelt"] = "failed"
            logger.error(f"GDELT failed: {e}")

        unique = self._dedupe_urls(all_articles)

        if unique:
            self._cache = unique
            self._save_cache(unique)
            logger.info(f"Fetched {len(unique)} unique articles")
            return unique[:limit]

        if self._cache:
            logger.warning("All fetchers empty — using cached articles")
            return self._cache[:limit]

        logger.error("No articles from any source and no cache")
        return []

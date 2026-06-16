"""GDELT 2.0 news fetcher for autonomous system."""

import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import quote

logger = logging.getLogger(__name__)


class GDELTFetcher:
    """Fetch news from GDELT 2.0 (Global Database of Events, Language, and Tone)."""

    def __init__(self):
        """Initialize GDELT fetcher."""
        self.base_url = "https://api.gdeltproject.org/api/v2/doc/doc"
        self.timeout = 10

    def fetch_news(
        self,
        keywords: Optional[List[str]] = None,
        time_span: str = "1d",
        sort: str = "latest",
        limit: int = 250,
    ) -> List[Dict[str, Any]]:
        """
        Fetch news from GDELT.

        Args:
            keywords: Keywords to search for (e.g., ["AI", "technology"])
            time_span: Time span (15m, 1h, 1d, 7d, 30d)
            sort: Sort order (latest, earliest, relevance)
            limit: Number of articles to fetch (max 250)

        Returns:
            List of article dictionaries
        """
        try:
            keywords = keywords or ["news", "breaking"]
            query = " ".join(keywords)

            params = {
                "query": query,
                "mode": "artlist",
                "format": "json",
                "timespan": time_span,
                "sort": "datedesc",
                "maxrecords": min(limit, 250),
            }

            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            articles = []

            # GDELT returns articles in a specific format
            if "articles" in data:
                for article in data["articles"]:
                    articles.append(self.normalize_article(article))

            logger.info(f"✓ Fetched {len(articles)} articles from GDELT for '{query}'")
            return articles

        except requests.exceptions.Timeout:
            logger.error("GDELT request timed out")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"GDELT request error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching from GDELT: {e}")
            return []

    def fetch_trending(
        self,
        time_span: str = "1d",
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Fetch trending news from GDELT.

        Args:
            time_span: Time span for trending (1h, 4h, 1d, 7d)
            limit: Number of articles to fetch

        Returns:
            List of trending articles
        """
        try:
            # Use a broad query to catch trending topics
            params = {
                "query": "sourcelang:english",
                "mode": "artlist",
                "format": "json",
                "timespan": time_span,
                "sort": "datedesc",
                "maxrecords": min(limit, 250),
            }

            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            articles = []

            if "articles" in data:
                for article in data["articles"]:
                    articles.append(self.normalize_article(article))

            logger.info(f"✓ Fetched {len(articles)} trending articles from GDELT")
            return articles

        except Exception as e:
            logger.error(f"Error fetching trending from GDELT: {e}")
            return []

    @staticmethod
    def normalize_article(article: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize GDELT article to standard format."""
        from fetchers.media_utils import normalize_media_fields

        item = {
            "source": "gdelt",
            "url": article.get("url", ""),
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("body", article.get("description", "")),
            "image_url": article.get("socialimage") or article.get("image", ""),
            "published_at": article.get("pubdate", article.get("seendate", "")),
            "source_name": article.get("domain", ""),
            "tone": article.get("tone", 0),
            "raw": article,
        }
        return normalize_media_fields(item)

    def search_by_person(self, person_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search news by person name."""
        try:
            params = {
                "query": f'people:"{person_name}"',
                "format": "json",
                "timespan": "7d",
                "maxrecords": min(limit, 250),
            }

            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            articles = [self.normalize_article(a) for a in data.get("articles", [])]

            logger.info(f"✓ Found {len(articles)} articles about {person_name}")
            return articles

        except Exception as e:
            logger.error(f"Error searching for {person_name}: {e}")
            return []

    def search_by_location(self, location: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search news by location."""
        try:
            params = {
                "query": f'locations:"{location}"',
                "format": "json",
                "timespan": "7d",
                "maxrecords": min(limit, 250),
            }

            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            articles = [self.normalize_article(a) for a in data.get("articles", [])]

            logger.info(f"✓ Found {len(articles)} articles from {location}")
            return articles

        except Exception as e:
            logger.error(f"Error searching for {location}: {e}")
            return []

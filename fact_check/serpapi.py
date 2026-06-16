"""SerpAPI wrapper for cross-source verification (optional)."""
import logging
import os
from typing import List

import requests

logger = logging.getLogger(__name__)


class SerpAPIClient:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        self.base_url = "https://serpapi.com/search"

    def search_headline(self, title: str, num: int = 5) -> List[str]:
        """Return URLs from Google news search for headline."""
        if not self.api_key or not title:
            return []
        try:
            r = requests.get(
                self.base_url,
                params={
                    "engine": "google",
                    "q": title[:100],
                    "api_key": self.api_key,
                    "num": num,
                },
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            urls = []
            for item in data.get("organic_results", []):
                link = item.get("link")
                if link:
                    urls.append(link)
            return urls
        except Exception as e:
            logger.warning(f"SerpAPI search failed: {e}")
            return []

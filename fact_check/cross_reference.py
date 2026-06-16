"""Cross-reference articles across sources and optional SerpAPI."""
import logging
import re
from typing import Dict, List, Tuple

from .confidence import score_confidence
from .serpapi import SerpAPIClient

logger = logging.getLogger(__name__)


def _normalize_title(title: str) -> str:
    t = re.sub(r"[^\w\s]", "", (title or "").lower())
    return " ".join(t.split()[:12])


class CrossReferenceChecker:
    """Verify stories appear in multiple places before publish."""

    def __init__(self, min_confidence: float = None):
        import os

        self.min_confidence = float(
            os.getenv("CONFIDENCE_THRESHOLD_PUBLISH", 0.55)
        )
        self.serp = SerpAPIClient()

    def count_similar_in_batch(
        self, article: Dict, all_articles: List[Dict]
    ) -> int:
        """How many articles in this batch share a similar headline."""
        key = _normalize_title(article.get("title", ""))
        if not key:
            return 0
        count = 0
        for other in all_articles:
            if _normalize_title(other.get("title", "")) == key:
                count += 1
        return max(count, 1)

    def verify(
        self, article: Dict, all_articles: List[Dict]
    ) -> Tuple[bool, float, str]:
        """
        Returns (passes, confidence, reason).
        """
        title = article.get("title", "")
        batch_count = self.count_similar_in_batch(article, all_articles)
        serp_urls = self.serp.search_headline(title)
        serp_count = len(serp_urls)

        confidence = score_confidence(title, batch_count, serp_count)
        filter_score = float(article.get("score", 0) or 0)
        confidence = max(confidence, filter_score)

        if confidence >= self.min_confidence:
            return True, confidence, f"Confidence {confidence:.0%}"

        return (
            False,
            confidence,
            f"Below fact-check threshold ({confidence:.0%} < {self.min_confidence:.0%})",
        )

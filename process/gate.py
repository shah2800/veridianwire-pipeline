"""Confidence threshold gating and reputation scoring."""

import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

# Source reputation scores (0-1)
SOURCE_REPUTATION = {
    # Tier 1: High credibility
    "reuters": 0.95,
    "associated press": 0.95,
    "bbc": 0.92,
    "the new york times": 0.92,
    "the washington post": 0.92,
    "the financial times": 0.90,
    "the economist": 0.90,
    "bloomberg": 0.90,
    "cnbc": 0.88,
    "the wall street journal": 0.88,
    # Tier 2: Medium credibility
    "cnn": 0.80,
    "nbc news": 0.80,
    "abc news": 0.80,
    "foxnews": 0.78,
    "the guardian": 0.85,
    "the independent": 0.80,
    # Tier 3: Tech/specialized
    "techcrunch": 0.85,
    "wired": 0.82,
    "the verge": 0.80,
    "ars technica": 0.82,
    "hacker news": 0.75,
    # Default: assume medium credibility
    "default": 0.65,
}


class ReputationScorer:
    """Score article source reputation."""

    def get_source_reputation(self, source_name: str) -> float:
        """
        Get reputation score for news source.

        Args:
            source_name: Name of news source

        Returns:
            Reputation score (0-1)
        """
        source_lower = source_name.lower()

        # Exact match first
        if source_lower in SOURCE_REPUTATION:
            return SOURCE_REPUTATION[source_lower]

        # Substring match
        for known_source, score in SOURCE_REPUTATION.items():
            if known_source in source_lower or source_lower in known_source:
                return score

        return SOURCE_REPUTATION["default"]

    def score_article(self, article: Dict[str, Any]) -> float:
        """
        Score article credibility based on source.

        Args:
            article: Article dict

        Returns:
            Credibility score (0-1)
        """
        source_name = article.get("source_name", "")
        return self.get_source_reputation(source_name)


class ConfidenceGate:
    """Gate articles based on confidence threshold."""

    def __init__(self, threshold: float = 0.7, reputation_weight: float = 0.5):
        """
        Initialize confidence gate.

        Args:
            threshold: Confidence threshold (0-1)
            reputation_weight: Weight of source reputation in final score
        """
        self.threshold = threshold
        self.reputation_weight = reputation_weight
        self.reputation_scorer = ReputationScorer()

    def calculate_confidence(self, article: Dict[str, Any]) -> float:
        """
        Calculate confidence score for article.

        Args:
            article: Article dict

        Returns:
            Confidence score (0-1)
        """
        scores = []

        # Source reputation (weighted)
        reputation_score = self.reputation_scorer.score_article(article)
        scores.append(reputation_score * self.reputation_weight)

        # Content score (has description or content)
        content = article.get("content") or article.get("description") or ""
        content_score = 0.9 if len(content) > 200 else 0.6 if len(content) > 50 else 0.2
        scores.append(content_score * (1 - self.reputation_weight) * 0.5)

        # Has title
        title_score = 0.8 if article.get("title") else 0.2
        scores.append(title_score * (1 - self.reputation_weight) * 0.5)

        overall_confidence = sum(scores)
        return min(overall_confidence, 1.0)

    def passes_gate(self, article: Dict[str, Any]) -> Tuple[bool, float, str]:
        """
        Check if article passes confidence gate.

        Args:
            article: Article dict

        Returns:
            Tuple of (passes, confidence_score, reason)
        """
        confidence = self.calculate_confidence(article)

        if confidence >= self.threshold:
            return True, confidence, f"Confidence OK ({confidence:.2%})"
        else:
            return (
                False,
                confidence,
                f"Below threshold ({confidence:.2%} < {self.threshold:.2%})",
            )

    def filter_articles(
        self, articles: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[Tuple[Dict[str, Any], float, str]]]:
        """
        Filter articles by confidence gate.

        Args:
            articles: List of articles

        Returns:
            Tuple of (passed_articles, failed_articles_with_reasons)
        """
        passed = []
        failed = []

        for article in articles:
            passes, confidence, reason = self.passes_gate(article)
            if passes:
                passed.append(article)
            else:
                failed.append((article, confidence, reason))

        logger.info(
            f"Confidence gate: {len(passed)}/{len(articles)} articles passed "
            f"(threshold: {self.threshold:.2%})"
        )
        return passed, failed

    def set_threshold(self, threshold: float):
        """Update confidence threshold."""
        self.threshold = max(0.0, min(1.0, threshold))
        logger.info(f"Confidence gate threshold set to {self.threshold:.2%}")

    def add_source_reputation(self, source_name: str, score: float):
        """Add or update source reputation."""
        SOURCE_REPUTATION[source_name.lower()] = max(0.0, min(1.0, score))
        logger.info(f"Updated reputation for '{source_name}': {score:.2%}")

    def get_reputation_stats(self) -> Dict[str, float]:
        """Get reputation statistics."""
        return {
            "mean": sum(SOURCE_REPUTATION.values()) / len(SOURCE_REPUTATION),
            "min": min(SOURCE_REPUTATION.values()),
            "max": max(SOURCE_REPUTATION.values()),
            "num_sources": len(SOURCE_REPUTATION),
        }

"""Spam detection for news articles."""

import logging
import re
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)


class SpamFilter:
    """Detect spam and low-quality articles using heuristics."""

    def __init__(
        self,
        min_title_length: int = 10,
        min_content_length: int = 100,
        max_repeated_words: float = 0.3,
    ):
        """
        Initialize spam filter.

        Args:
            min_title_length: Minimum title length
            min_content_length: Minimum content length
            max_repeated_words: Maximum proportion of repeated words (0-1)
        """
        self.min_title_length = min_title_length
        self.min_content_length = min_content_length
        self.max_repeated_words = max_repeated_words

        # Spam keywords
        self.spam_keywords = {
            "click here",
            "buy now",
            "limited offer",
            "congratulations",
            "claim prize",
            "verify account",
            "confirm identity",
            "urgent action required",
            "dear customer",
            "nigerian prince",
        }

    def _extract_words(self, text: str) -> list:
        """Extract words from text."""
        text = text.lower()
        words = re.findall(r"\b[a-z]+\b", text)
        return words

    def _check_length(self, title: str, content: str) -> Tuple[bool, str]:
        """Check if article has minimum length."""
        if len(title) < self.min_title_length:
            return False, f"Title too short ({len(title)} < {self.min_title_length})"

        if len(content) < self.min_content_length:
            return False, f"Content too short ({len(content)} < {self.min_content_length})"

        return True, "Length OK"

    def _check_repeated_words(self, text: str) -> Tuple[bool, str]:
        """Check for excessive repeated words (keyword stuffing)."""
        words = self._extract_words(text)

        if not words:
            return False, "No words found"

        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

        max_count = max(word_counts.values())
        repetition_ratio = max_count / len(words)

        if repetition_ratio > self.max_repeated_words:
            return (
                False,
                f"Keyword stuffing detected ({repetition_ratio:.1%} repetition)",
            )

        return True, "Word distribution OK"

    def _check_spam_keywords(self, text: str) -> Tuple[bool, str]:
        """Check for common spam keywords."""
        text_lower = text.lower()

        for keyword in self.spam_keywords:
            if keyword in text_lower:
                return False, f"Spam keyword detected: '{keyword}'"

        return True, "No spam keywords"

    def _check_email_links(self, content: str) -> Tuple[bool, str]:
        """Check for suspicious email or link patterns."""
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(email_pattern, content)

        if len(emails) > 5:
            return False, f"Too many email addresses ({len(emails)})"

        # Check for suspicious URLs
        url_pattern = r"http[s]?://[^\s]+"
        urls = re.findall(url_pattern, content)

        if len(urls) > 10:
            return False, f"Too many URLs ({len(urls)})"

        return True, "Email/link distribution OK"

    def _check_readability(self, text: str) -> Tuple[bool, str]:
        """Check readability (very basic check)."""
        words = self._extract_words(text)

        if not words:
            return False, "No readable content"

        # Average word length
        avg_word_length = sum(len(w) for w in words) / len(words)

        # Suspiciously long average word length might indicate gibberish
        if avg_word_length > 15:
            return False, f"Suspiciously long words (avg: {avg_word_length:.1f})"

        return True, "Readability OK"

    def is_spam(self, article: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Check if article is spam.

        Args:
            article: Article dict with 'title' and 'content'

        Returns:
            Tuple of (is_spam, reason)
        """
        title = article.get("title") or ""
        content = article.get("content") or article.get("description") or ""

        checks = [
            self._check_length(title, content),
            self._check_repeated_words(f"{title} {content}"),
            self._check_spam_keywords(f"{title} {content}"),
            self._check_email_links(content),
            self._check_readability(content),
        ]

        for passed, reason in checks:
            if not passed:
                logger.info(f"Spam detected: {reason}")
                return True, reason

        return False, "Passed all checks"

    def get_spam_score(self, article: Dict[str, Any]) -> float:
        """
        Get spam score (0-1, higher = more likely spam).

        Args:
            article: Article dict

        Returns:
            Spam score
        """
        is_spam, _ = self.is_spam(article)
        return 1.0 if is_spam else 0.0

    def filter_articles(
        self, articles: list
    ) -> Tuple[list, list]:
        """
        Filter articles, separating spam from legitimate.

        Args:
            articles: List of article dicts

        Returns:
            Tuple of (legitimate_articles, spam_articles)
        """
        legitimate = []
        spam = []

        for article in articles:
            is_spam, reason = self.is_spam(article)
            if is_spam:
                spam.append((article, reason))
            else:
                legitimate.append(article)

        logger.info(f"Filtered {len(articles)} articles: {len(legitimate)} legitimate, {len(spam)} spam")
        return legitimate, spam

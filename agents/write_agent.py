"""WriteAgent — rewrite articles with Groq/OpenAI."""
import logging
import os
from typing import Any, Dict, List, Optional

from core.rewrite_quality import is_bad_rewrite
from fetchers.article_content import to_article_html

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class WriteAgent(BaseAgent):
    def __init__(self, db, groq, openai=None):
        super().__init__("WriteAgent", "CTO")
        self.db = db
        self.groq = groq
        self.openai = openai
        self.publish_limit = int(os.getenv("PUBLISH_LIMIT_PER_CYCLE", 10))

    def _rewrite_one(self, title: str, content: str) -> Optional[str]:
        text = self.retry_with_backoff(
            self.groq.rewrite_article, title, content, strict=False
        )
        if text and is_bad_rewrite(text):
            logger.warning("Rewrite rejected (placeholders/template), retrying strict: %s", title[:60])
            text = self.retry_with_backoff(
                self.groq.rewrite_article, title, content, strict=True
            )
        if text and is_bad_rewrite(text) and self.openai:
            text = self.retry_with_backoff(self.openai.rewrite_article, title, content)
        if text and is_bad_rewrite(text):
            logger.warning("Rewrite still bad, using source HTML fallback: %s", title[:60])
            return to_article_html(content)
        return text

    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        filtered: List[Dict] = ctx.get("filtered", [])[: self.publish_limit]
        rewritten_articles = []

        for article in filtered:
            title = article.get("title") or ""
            content = article.get("content") or ""
            try:
                text = self._rewrite_one(title, content)
                if text:
                    article["rewritten_content"] = text
                    rewritten_articles.append(article)
            except Exception as e:
                ctx.setdefault("errors", []).append(f"write: {e}")

        ctx["rewritten"] = rewritten_articles
        ctx["rewrite_count"] = len(rewritten_articles)
        self.log_event("success", f"Rewrote {len(rewritten_articles)} articles")
        return ctx

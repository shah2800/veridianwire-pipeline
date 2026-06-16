"""DataAgent — fetch news from all sources."""
from typing import Any, Dict

from .base_agent import BaseAgent


class DataAgent(BaseAgent):
    def __init__(self, db, fetcher):
        super().__init__("DataAgent", "CEO")
        self.db = db
        self.fetcher = fetcher

    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        limit = ctx.get("fetch_limit", 100)
        articles = self.retry_with_backoff(
            self.fetcher.fetch_all_sources, limit=limit
        ) or []

        ctx["articles"] = articles
        ctx["fetched"] = len(articles)
        ctx["fetch_status"] = getattr(self.fetcher, "last_status", {})

        self.log_event(
            "success" if articles else "warning",
            f"Fetched {len(articles)} articles",
            details={"count": len(articles), "sources": ctx["fetch_status"]},
        )
        return ctx

"""FilterAgent — spam filter, confidence gate, dedup, DB insert."""
import os
from typing import Any, Dict, List

from process.gate import ConfidenceGate
from process.minhash import MinHashDeduplicator
from process.spam_filter import SpamFilter

from .base_agent import BaseAgent


class FilterAgent(BaseAgent):
    def __init__(self, db, dedup: MinHashDeduplicator):
        super().__init__("FilterAgent", "DevOps")
        self.db = db
        self.dedup = dedup
        self.spam = SpamFilter()
        threshold = float(os.getenv("CONFIDENCE_THRESHOLD_FILTER", 0.7))
        self.gate = ConfidenceGate(threshold=threshold)

    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        articles: List[Dict] = ctx.get("articles", [])
        stats = {
            "skipped_spam": 0,
            "skipped_gate": 0,
            "skipped_dup": 0,
        }
        filtered_records = []

        legitimate, spam_list = self.spam.filter_articles(articles)
        stats["skipped_spam"] = len(spam_list)

        passed, failed_gate = self.gate.filter_articles(legitimate)
        stats["skipped_gate"] = len(failed_gate)

        for article in passed:
            try:
                title = article.get("title") or ""
                content = article.get("content") or article.get("description") or ""
                raw_json = {
                    k: article[k]
                    for k in ("image_url", "video_url", "source_url", "source_name", "author")
                    if article.get(k)
                }
                raw = self.db.insert_raw_news(
                    source=article.get("source", "unknown"),
                    url=article.get("url"),
                    title=title,
                    content=content,
                    published_at=article.get("published_at") or article.get("publishedAt"),
                    author=article.get("author"),
                    raw_json=raw_json,
                )

                sig = self.dedup.compute_signature(title)
                dedup_hash = str(hash(tuple(sig)))

                existing = (
                    self.db.client.table("filtered_news")
                    .select("id")
                    .eq("dedup_hash", dedup_hash)
                    .execute()
                )
                if existing.data:
                    stats["skipped_dup"] += 1
                    continue

                _, confidence, _ = self.gate.passes_gate(article)
                record = self.db.insert_filtered_news(
                    raw_news_id=raw["id"],
                    title=title,
                    content=content,
                    score=confidence,
                    dedup_hash=dedup_hash,
                )
                record["_source_article"] = {**article, "score": confidence}
                filtered_records.append(record)
            except Exception as e:
                ctx.setdefault("errors", []).append(f"filter: {e}")
                self.log_event("error", str(e), error=e)

        ctx["filtered"] = filtered_records
        ctx["filtered_count"] = len(filtered_records)
        ctx["passed_quality"] = len(passed)
        ctx.update(stats)

        self.log_event(
            "success",
            f"Filtered to {len(filtered_records)} articles",
            details=stats,
        )
        return ctx

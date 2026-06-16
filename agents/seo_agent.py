"""SEOAgent — fact-check + SEO metadata."""
from typing import Any, Dict, List

from core.seo_meta import basic_seo_meta, enrich_seo_with_media
from fact_check.cross_reference import CrossReferenceChecker

from .base_agent import BaseAgent


class SEOAgent(BaseAgent):
    def __init__(self, db, openai=None):
        super().__init__("SEOAgent", "Marketing")
        self.db = db
        self.openai = openai
        self.fact_check = CrossReferenceChecker()

    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        rewritten: List[Dict] = ctx.get("rewritten", [])
        all_articles = ctx.get("articles", [])
        ready = []
        skipped = 0

        for article in rewritten:
            src = article.get("_source_article", {})
            src["score"] = article.get("score", src.get("score", 0.7))
            passes, confidence, reason = self.fact_check.verify(src, all_articles)
            if not passes:
                skipped += 1
                continue

            title = article.get("title", "")
            content = article.get("rewritten_content", "")
            seo_meta = None
            if self.openai:
                try:
                    seo_meta = self.openai.generate_seo_meta(title, content)
                except Exception:
                    seo_meta = None
            if not seo_meta:
                seo_meta = basic_seo_meta(title, content, src.get("source", "news"))

            seo_meta = enrich_seo_with_media(seo_meta, src)
            seo_meta["fact_check_score"] = confidence
            article["seo_meta"] = seo_meta
            article["fact_check_score"] = confidence
            ready.append(article)

        ctx["seo_ready"] = ready
        ctx["skipped_fact_check"] = skipped
        self.log_event(
            "success",
            f"SEO ready: {len(ready)}, fact-check skipped: {skipped}",
        )
        return ctx

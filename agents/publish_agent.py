"""PublishAgent — save to DB, sitemap, optional deploy."""
import os
import re
from typing import Any, Dict

from .base_agent import BaseAgent


class PublishAgent(BaseAgent):
    def __init__(self, db):
        super().__init__("PublishAgent", "DevOps")
        self.db = db
        self.site_url = os.getenv(
            "NEXT_PUBLIC_SITE_URL", os.getenv("DOMAIN_NAME", "http://localhost:3000")
        )
        if not self.site_url.startswith("http"):
            self.site_url = f"https://{self.site_url}"

    def run(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        ready = ctx.get("seo_ready", [])
        published = []

        for article in ready:
            try:
                title = article.get("title", "")
                slug = self._slugify(title)
                content = article.get("rewritten_content", "")
                seo_meta = article.get("seo_meta", {})

                record = self.db.insert_published_article(
                    filtered_news_id=article["id"],
                    url=f"{self.site_url}/news/{slug}",
                    slug=slug,
                    content=content,
                    seo_meta=seo_meta,
                )
                published.append(record)
            except Exception as e:
                ctx.setdefault("errors", []).append(f"publish: {e}")

        ctx["published"] = published
        ctx["published_count"] = len(published)

        self._update_sitemap(published)
        if os.getenv("AUTO_DEPLOY", "").lower() in ("1", "true", "yes"):
            self._try_deploy(len(published))

        self.log_event("success", f"Published {len(published)} articles")
        return ctx

    @staticmethod
    def _slugify(title: str) -> str:
        slug = re.sub(r"[^\w\s-]", "", (title or "article").lower())
        slug = re.sub(r"[-\s]+", "-", slug).strip("-")
        return slug[:200] or "article"

    def _update_sitemap(self, published: list) -> None:
        try:
            from seo.sitemap import SitemapGenerator

            all_pub = (
                self.db.client.table("published_articles")
                .select("slug,published_at")
                .order("published_at", desc=True)
                .limit(500)
                .execute()
            )
            articles = all_pub.data or published
            SitemapGenerator().save_sitemap(articles)
        except Exception as e:
            self.log_event("warning", f"Sitemap update failed: {e}")

    def _try_deploy(self, published_count: int = 0) -> None:
        try:
            from deploy.git_manager import GitManager
            from deploy.vercel_cli import VercelDeployer

            GitManager().commit_and_push(f"auto: published {published_count} articles")
            VercelDeployer().deploy_production()
        except Exception as e:
            self.log_event("warning", f"Auto-deploy skipped: {e}")

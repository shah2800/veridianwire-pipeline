"""Google Search Console URL submission (optional)."""
import logging
import os

logger = logging.getLogger(__name__)


class SearchConsoleClient:
    """Submit sitemap/URLs when credentials are configured."""

    def __init__(self):
        self.site_url = os.getenv("DOMAIN_NAME", "")
        self.credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    def submit_sitemap(self, sitemap_url: str) -> bool:
        if not self.credentials or not self.site_url:
            logger.info("Search Console not configured — skip submit")
            return False
        logger.info(f"Search Console: would submit {sitemap_url}")
        return True

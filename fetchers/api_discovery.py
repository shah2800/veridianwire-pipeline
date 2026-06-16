"""
Discover RSS/API feeds from a news site (evidence-based).

Rule: only report endpoints that return real structured data.
"""
import logging
import re
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests

logger = logging.getLogger(__name__)

COMMON_FEED_PATHS = [
    "/feed",
    "/feed/",
    "/rss",
    "/rss.xml",
    "/feeds/rss.xml",
    "/atom.xml",
    "/news/rss.xml",
]


class APIDiscovery:
    """Find stable RSS/JSON feeds for a news domain."""

    def __init__(self, target_url: str, timeout: int = 15):
        self.target_url = target_url.rstrip("/")
        self.timeout = timeout
        self.endpoints: List[Dict[str, Any]] = []

    def discover(self) -> List[Dict[str, Any]]:
        """Run discovery: HTML link tags + common paths + optional Playwright."""
        parsed = urlparse(self.target_url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        self._try_html_feed_links(base)
        self._try_common_paths(base)
        self._try_playwright_xhr()

        return self._rank(self.endpoints)

    def _try_html_feed_links(self, base: str) -> None:
        try:
            r = requests.get(
                self.target_url,
                timeout=self.timeout,
                headers={"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"},
            )
            r.raise_for_status()
            for m in re.finditer(
                r'<link[^>]+type=["\']application/(rss\+xml|atom\+xml)["\'][^>]*href=["\']([^"\']+)',
                r.text,
                re.I,
            ):
                href = urljoin(base, m.group(2))
                if self._probe_feed(href, "RSS from HTML link"):
                    break
        except Exception as e:
            logger.warning(f"HTML discovery failed: {e}")

    def _try_common_paths(self, base: str) -> None:
        for path in COMMON_FEED_PATHS:
            url = urljoin(base, path)
            self._probe_feed(url, f"Common path {path}")

    def _probe_feed(self, url: str, description: str) -> bool:
        if any(e["url"] == url for e in self.endpoints):
            return True
        try:
            import feedparser

            feed = feedparser.parse(url)
            if feed.entries:
                self.endpoints.append({
                    "url": url,
                    "method": "GET",
                    "description": description,
                    "response_type": "RSS/XML",
                    "stability": "STABLE",
                    "auth_required": False,
                    "sample_count": len(feed.entries),
                    "usefulness_rank": 0,
                })
                logger.info(f"Found RSS: {url} ({len(feed.entries)} entries)")
                return True
        except Exception:
            pass

        try:
            r = requests.get(
                url,
                timeout=self.timeout,
                headers={"Accept": "application/json, application/xml"},
            )
            if r.status_code == 200 and (
                "json" in r.headers.get("content-type", "")
                or r.text.strip().startswith("{")
                or r.text.strip().startswith("[")
            ):
                self.endpoints.append({
                    "url": url,
                    "method": "GET",
                    "description": description,
                    "response_type": "JSON",
                    "stability": "SEMI-STABLE",
                    "auth_required": False,
                    "example_response": r.text[:300],
                    "usefulness_rank": 0,
                })
                return True
        except Exception:
            pass
        return False

    def _try_playwright_xhr(self) -> None:
        """Capture JSON XHR from network (optional — needs playwright installed)."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return

        seen = set()
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                def on_response(response):
                    ct = response.headers.get("content-type", "")
                    if "application/json" not in ct or response.status != 200:
                        return
                    url = response.url
                    if url in seen or "google" in url or "facebook" in url:
                        return
                    seen.add(url)
                    try:
                        body = response.text()[:300]
                    except Exception:
                        body = ""
                    if any(k in body.lower() for k in ("title", "headline", "article", "url")):
                        self.endpoints.append({
                            "url": url,
                            "method": "GET",
                            "description": "XHR JSON (observed)",
                            "response_type": "JSON",
                            "stability": "SEMI-STABLE",
                            "auth_required": False,
                            "example_response": body,
                            "usefulness_rank": 0,
                        })

                page.on("response", on_response)
                page.goto(self.target_url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(3000)
                browser.close()
        except Exception as e:
            logger.warning(f"Playwright discovery skipped: {e}")

    def _rank(self, endpoints: List[Dict]) -> List[Dict]:
        def score(ep: Dict) -> int:
            s = 0
            if ep.get("response_type") == "RSS/XML":
                s += 100
            if ep.get("stability") == "STABLE":
                s += 50
            if not ep.get("auth_required"):
                s += 30
            s += ep.get("sample_count", 0)
            return s

        ranked = sorted(endpoints, key=score, reverse=True)
        for i, ep in enumerate(ranked):
            ep["usefulness_rank"] = i + 1
        return ranked

    def print_report(self) -> None:
        ranked = self.discover()
        print(f"\n=== API Discovery: {self.target_url} ===")
        print(f"Found {len(ranked)} proven endpoints\n")
        for ep in ranked[:5]:
            print(f"#{ep['usefulness_rank']} {ep['description']}")
            print(f"   {ep['url']} ({ep['response_type']}, {ep['stability']})")
        if not ranked:
            print("No feeds found. Use NewsAPI/RSS list in fetchers/rss.py")


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.bbc.com/news"
    APIDiscovery(url).print_report()

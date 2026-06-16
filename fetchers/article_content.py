"""Extract full article body from RSS entries and source URLs."""
import logging
import re
from html import unescape
from typing import Optional

import requests

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AutonomousNewsBot/1.0; +https://autonomousnews.com)",
    "Accept": "text/html,application/xhtml+xml",
}

_STRIP_TAGS = re.compile(r"<[^>]+>")


def plain_text(html: str) -> str:
    text = _STRIP_TAGS.sub(" ", html or "")
    return re.sub(r"\s+", " ", unescape(text)).strip()


def rss_entry_content(entry) -> str:
    """Prefer RSS content:encoded (full HTML) over short summary."""
    if hasattr(entry, "content") and entry.content:
        best = ""
        for block in entry.content:
            val = block.get("value") if isinstance(block, dict) else getattr(block, "value", "")
            if val and len(plain_text(val)) > len(plain_text(best)):
                best = val
        if len(plain_text(best)) > 80:
            return best

    return entry.get("summary", "") or entry.get("description", "") or ""


def to_article_html(content: str) -> str:
    """Normalize plain text or HTML into displayable article HTML."""
    if not content:
        return "<p>No content available.</p>"
    if re.search(r"<p[\s>]", content, re.I) or re.search(r"<h[1-6][\s>]", content, re.I):
        return content
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", plain_text(content)) if p.strip()]
    if not paragraphs:
        return f"<p>{plain_text(content)}</p>"
    return "".join(f"<p>{p}</p>" for p in paragraphs)


def fetch_article_html(url: str, timeout: int = 12) -> Optional[str]:
    """Scrape main article body from the source page when RSS is too short."""
    if not url or not url.startswith("http"):
        return None
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        html = resp.text

        patterns = [
            r'<div[^>]+class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*(?:<div|<footer|<section class="related)',
            r'<div[^>]+class="[^"]*article-body[^"]*"[^>]*>(.*?)</div>',
            r'<article[^>]*>(.*?)</article>',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.I | re.S)
            if match:
                body = match.group(1)
                text_len = len(plain_text(body))
                if text_len > 200:
                    return _clean_scraped_html(body)

        return None
    except Exception as e:
        logger.debug("Article scrape failed for %s: %s", url, e)
        return None


def _clean_scraped_html(html: str) -> str:
    """Remove scripts, ads, and junk from scraped HTML."""
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.I | re.S)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.I | re.S)
    html = re.sub(r"<aside[^>]*>.*?</aside>", "", html, flags=re.I | re.S)
    html = re.sub(r'<div[^>]+class="[^"]*(?:ad|newsletter|related|share|comment)[^"]*"[^>]*>.*?</div>',
                  "", html, flags=re.I | re.S)
    return html.strip()


def resolve_article_body(entry, url: str, min_chars: int = 400) -> str:
    """Get the richest article body available: RSS full → scrape → summary."""
    rss_body = rss_entry_content(entry)
    if len(plain_text(rss_body)) >= min_chars:
        return to_article_html(rss_body)

    scraped = fetch_article_html(url)
    if scraped and len(plain_text(scraped)) >= min_chars:
        return scraped

    if rss_body:
        return to_article_html(rss_body)

    if scraped:
        return scraped

    return "<p>Full article content could not be loaded. Please read the original at the source link below.</p>"

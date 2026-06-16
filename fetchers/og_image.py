"""Fetch Open Graph / Twitter image from article URL when feed has no thumbnail."""
import logging
import re
from typing import Optional

import requests

logger = logging.getLogger(__name__)

_OG_PATTERNS = [
    re.compile(r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::secure_url)?["\']', re.I),
    re.compile(r'<meta[^>]+name=["\']twitter:image(?::src)?["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image(?::src)?["\']', re.I),
    re.compile(r'<link[^>]+rel=["\']image_src["\'][^>]+href=["\']([^"\']+)["\']', re.I),
]

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AutonomousNewsBot/1.0; +https://autonomousnews.com)",
    "Accept": "text/html,application/xhtml+xml",
}


def fetch_og_image(url: str, timeout: int = 8) -> Optional[str]:
    """Return og:image or twitter:image URL from a page, or None."""
    if not url or not url.startswith("http"):
        return None
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        html = resp.text[:150_000]
        for pattern in _OG_PATTERNS:
            match = pattern.search(html)
            if match:
                img = match.group(1).strip()
                if img.startswith("http"):
                    return img
        return None
    except Exception as e:
        logger.debug("OG image fetch failed for %s: %s", url, e)
        return None

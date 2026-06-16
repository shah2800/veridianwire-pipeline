"""Extract image and video URLs from fetched articles and HTML."""
import re
from typing import Any, Dict, Optional
from urllib.parse import urlparse

_IMG_RE = re.compile(
    r"""<img[^>]+src=["']([^"']+)["']""",
    re.IGNORECASE,
)
_VIDEO_EXT = (".mp4", ".webm", ".mov", ".m4v")
_VIDEO_HOSTS = ("youtube.com", "youtu.be", "vimeo.com", "dailymotion.com")


def _is_valid_url(url: Optional[str]) -> bool:
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return False
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc)
    except Exception:
        return False


def extract_image_from_html(html: str) -> Optional[str]:
    if not html:
        return None
    match = _IMG_RE.search(html)
    if match and _is_valid_url(match.group(1)):
        return match.group(1).strip()
    return None


def is_video_url(url: str) -> bool:
    if not _is_valid_url(url):
        return False
    lower = url.lower()
    if any(lower.endswith(ext) for ext in _VIDEO_EXT):
        return True
    return any(host in lower for host in _VIDEO_HOSTS)


def normalize_media_fields(article: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure article dict has image_url, video_url, source_url, source_name."""
    image_url = (
        article.get("image_url")
        or article.get("image")
        or article.get("urlToImage")
        or article.get("thumbnail")
    )

    video_url = article.get("video_url") or article.get("video")

    content = article.get("content") or article.get("description") or article.get("summary") or ""
    if not image_url and content:
        image_url = extract_image_from_html(content)

    if _is_valid_url(image_url):
        article["image_url"] = image_url.strip()
    else:
        article.pop("image_url", None)

    if _is_valid_url(video_url):
        article["video_url"] = video_url.strip()
    elif article.get("url") and is_video_url(article["url"]):
        article["video_url"] = article["url"]
    else:
        article.pop("video_url", None)

    if article.get("url"):
        article["source_url"] = article["url"]
    if article.get("source_name"):
        article["source_name"] = article["source_name"]
    elif article.get("source") and article["source"] not in ("rss", "newsapi", "gdelt"):
        article["source_name"] = article["source"]

    return article

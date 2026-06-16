"""RSS feed fetcher."""
import logging
from typing import List, Dict, Optional

from fetchers.media_utils import normalize_media_fields, is_video_url
from fetchers.article_content import rss_entry_content, plain_text

logger = logging.getLogger(__name__)


def _rss_image(entry) -> Optional[str]:
    if hasattr(entry, "media_content") and entry.media_content:
        for media in entry.media_content:
            url = media.get("url") if isinstance(media, dict) else getattr(media, "url", None)
            medium = (media.get("medium") if isinstance(media, dict) else getattr(media, "medium", "")) or ""
            if url and medium != "video":
                return url
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        thumb = entry.media_thumbnail[0]
        url = thumb.get("url") if isinstance(thumb, dict) else getattr(thumb, "url", None)
        if url:
            return url
    if hasattr(entry, "enclosures") and entry.enclosures:
        for enc in entry.enclosures:
            enc_type = (enc.get("type") if isinstance(enc, dict) else getattr(enc, "type", "")) or ""
            href = enc.get("href") if isinstance(enc, dict) else getattr(enc, "href", None)
            if href and enc_type.startswith("image"):
                return href
    return None


def _rss_video(entry) -> Optional[str]:
    if hasattr(entry, "media_content") and entry.media_content:
        for media in entry.media_content:
            url = media.get("url") if isinstance(media, dict) else getattr(media, "url", None)
            medium = (media.get("medium") if isinstance(media, dict) else getattr(media, "medium", "")) or ""
            mtype = (media.get("type") if isinstance(media, dict) else getattr(media, "type", "")) or ""
            if url and (medium == "video" or mtype.startswith("video")):
                return url
    if hasattr(entry, "enclosures") and entry.enclosures:
        for enc in entry.enclosures:
            enc_type = (enc.get("type") if isinstance(enc, dict) else getattr(enc, "type", "")) or ""
            href = enc.get("href") if isinstance(enc, dict) else getattr(enc, "href", None)
            if href and enc_type.startswith("video"):
                return href
    link = entry.get("link", "")
    if link and is_video_url(link):
        return link
    return None


class RSSFetcher:
    """Fetch news from RSS feeds."""
    
    def __init__(self):
        self.feeds = {
            'bbc': 'https://feeds.bbc.co.uk/news/rss.xml',
            'reuters': 'https://feeds.reuters.com/reuters/businessNews',
            'techcrunch': 'https://techcrunch.com/feed/',
        }
    
    def fetch_from_feed(self, feed_url: str, limit=50):
        """Parse RSS feed."""
        try:
            import feedparser
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:limit]:
                full_content = rss_entry_content(entry)
                item = {
                    'source': 'rss',
                    'source_name': feed.feed.get('title', feed_url),
                    'title': entry.get('title', ''),
                    'content': full_content,
                    'summary': entry.get('summary', '') or entry.get('description', ''),
                    'url': entry.get('link', ''),
                    'author': entry.get('author'),
                    'published_at': entry.get('published'),
                    'image_url': _rss_image(entry),
                    'video_url': _rss_video(entry),
                }
                articles.append(normalize_media_fields(item))
            return articles
        except Exception as e:
            logger.error(f"RSS error: {e}")
            return []
    
    def fetch_all_feeds(self, limit=20):
        """Fetch from all configured feeds."""
        all_articles = []
        for feed_name, feed_url in self.feeds.items():
            articles = self.fetch_from_feed(feed_url, limit)
            for a in articles:
                a['source'] = feed_name
            all_articles.extend(articles)
        return all_articles

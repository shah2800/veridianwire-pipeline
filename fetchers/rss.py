"""RSS feed fetcher."""
import calendar
import logging
import time
from typing import List, Dict, Optional

from fetchers.media_utils import normalize_media_fields, is_video_url
from fetchers.article_content import rss_entry_content, plain_text

logger = logging.getLogger(__name__)

# Articles older than this (hours) are skipped at fetch time so the site stays fresh.
MAX_AGE_HOURS = 24


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


def _entry_age_hours(entry) -> Optional[float]:
    """Age of an entry in hours using its parsed publish time (UTC). None if unknown."""
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return None
    try:
        published_epoch = calendar.timegm(parsed)
        return (time.time() - published_epoch) / 3600.0
    except Exception:
        return None


class RSSFetcher:
    """Fetch fresh news from a wide set of real-time RSS feeds.

    Google News RSS feeds each aggregate hundreds of publishers and update in
    near real time, so the effective source count is in the hundreds.
    """

    def __init__(self):
        self.feeds = {
            # ---- Google News (each aggregates 100s of publishers, near real-time) ----
            "google_top": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
            "google_world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
            "google_business": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
            "google_technology": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
            "google_science": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",
            "google_health": "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=en-US&gl=US&ceid=US:en",
            "google_sports": "https://news.google.com/rss/headlines/section/topic/SPORTS?hl=en-US&gl=US&ceid=US:en",
            "google_entertainment": "https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=en-US&gl=US&ceid=US:en",
            "google_ai": "https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-US&gl=US&ceid=US:en",
            "google_politics": "https://news.google.com/rss/search?q=politics+when:1d&hl=en-US&gl=US&ceid=US:en",
            "google_crypto": "https://news.google.com/rss/search?q=cryptocurrency+when:1d&hl=en-US&gl=US&ceid=US:en",

            # ---- World / General ----
            "bbc": "https://feeds.bbc.co.uk/news/rss.xml",
            "bbc_world": "https://feeds.bbc.co.uk/news/world/rss.xml",
            "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
            "guardian_world": "https://www.theguardian.com/world/rss",
            "npr": "https://feeds.npr.org/1001/rss.xml",
            "cbs": "https://www.cbsnews.com/latest/rss/main",
            "abc": "https://abcnews.go.com/abcnews/topstories",
            "skynews_world": "https://feeds.skynews.com/feeds/rss/world.xml",
            "dw": "https://rss.dw.com/rdf/rss-en-all",
            "france24": "https://www.france24.com/en/rss",
            "yahoonews": "https://www.yahoo.com/news/rss",

            # ---- Business / Finance ----
            "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "marketwatch": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
            "fortune": "https://fortune.com/feed/",
            "businessinsider": "https://www.businessinsider.com/rss",
            "guardian_business": "https://www.theguardian.com/uk/business/rss",

            # ---- Technology ----
            "techcrunch": "https://techcrunch.com/feed/",
            "theverge": "https://www.theverge.com/rss/index.xml",
            "arstechnica": "https://feeds.arstechnica.com/arstechnica/index",
            "engadget": "https://www.engadget.com/rss.xml",
            "wired": "https://www.wired.com/feed/rss",
            "venturebeat": "https://venturebeat.com/feed/",
            "zdnet": "https://www.zdnet.com/news/rss.xml",
            "techradar": "https://www.techradar.com/rss",
            "mashable_tech": "https://mashable.com/feeds/rss/tech",

            # ---- Politics ----
            "politico": "https://rss.politico.com/politics-news.xml",
            "thehill": "https://thehill.com/news/feed/",
            "guardian_us_politics": "https://www.theguardian.com/us-news/us-politics/rss",

            # ---- Science ----
            "sciencedaily": "https://www.sciencedaily.com/rss/all.xml",
            "physorg": "https://phys.org/rss-feed/",
            "nasa": "https://www.nasa.gov/feed/",
            "newscientist": "https://www.newscientist.com/feed/home/",
            "livescience": "https://www.livescience.com/feeds/all",

            # ---- Health ----
            "medicalnews": "https://www.medicalnewstoday.com/rss",
            "statnews": "https://www.statnews.com/feed/",
            "guardian_health": "https://www.theguardian.com/society/health/rss",
            "who": "https://www.who.int/rss-feeds/news-english.xml",

            # ---- Sports ----
            "espn": "https://www.espn.com/espn/rss/news",
            "bbc_sport": "https://feeds.bbc.co.uk/sport/rss.xml",
            "skysports": "https://www.skysports.com/rss/12040",
            "cbssports": "https://www.cbssports.com/rss/headlines/",

            # ---- Entertainment ----
            "variety": "https://variety.com/feed/",
            "hollywoodreporter": "https://www.hollywoodreporter.com/feed/",
            "ew": "https://ew.com/feed/",
        }

    def fetch_from_feed(self, feed_url: str, limit=50):
        """Parse RSS feed, skipping stale entries."""
        try:
            import feedparser
            feed = feedparser.parse(feed_url)
            articles = []
            skipped_old = 0

            for entry in feed.entries[:limit]:
                age = _entry_age_hours(entry)
                if age is not None and age > MAX_AGE_HOURS:
                    skipped_old += 1
                    continue

                full_content = rss_entry_content(entry)
                item = {
                    'source': 'rss',
                    'source_name': feed.feed.get('title', feed_url),
                    'title': entry.get('title', ''),
                    'content': full_content,
                    'summary': entry.get('summary', '') or entry.get('description', ''),
                    'url': entry.get('link', ''),
                    'author': entry.get('author'),
                    'published_at': entry.get('published') or entry.get('updated'),
                    'image_url': _rss_image(entry),
                    'video_url': _rss_video(entry),
                }
                articles.append(normalize_media_fields(item))

            if skipped_old:
                logger.info(f"RSS {feed_url}: skipped {skipped_old} stale entries (> {MAX_AGE_HOURS}h)")
            return articles
        except Exception as e:
            logger.error(f"RSS error for {feed_url}: {e}")
            return []

    def fetch_all_feeds(self, limit=20):
        """Fetch from all configured feeds. Per-feed limit kept modest since there are many feeds."""
        all_articles = []
        per_feed = max(5, min(limit, 15))
        for feed_name, feed_url in self.feeds.items():
            articles = self.fetch_from_feed(feed_url, per_feed)
            for a in articles:
                a['source'] = feed_name
            all_articles.extend(articles)
        logger.info(f"RSS fetched {len(all_articles)} fresh articles from {len(self.feeds)} feeds")
        return all_articles

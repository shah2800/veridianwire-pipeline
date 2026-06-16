"""Tests for fetchers."""
import pytest
from fetchers.newsapi import NewsAPIFetcher
from fetchers.rss import RSSFetcher

def test_newsapi_fetcher():
    """Test NewsAPI fetcher."""
    fetcher = NewsAPIFetcher()
    # Will fail without API key, so just check it initializes
    assert fetcher.base_url == 'https://newsapi.org/v2'

def test_rss_fetcher():
    """Test RSS fetcher."""
    fetcher = RSSFetcher()
    feeds = list(fetcher.feeds.keys())
    assert len(feeds) > 0
    assert 'bbc' in feeds

@pytest.mark.asyncio
async def test_fetch_manager():
    """Test fetch manager."""
    from fetchers.fetch_manager import FetchManager
    manager = FetchManager()
    # Don't test actual fetch without mocking APIs
    assert manager.newsapi is not None
    assert manager.rss is not None

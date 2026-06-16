"""NewsAPI.org fetcher for news collection."""
import os, logging, requests
from typing import List, Dict

from fetchers.media_utils import normalize_media_fields

logger = logging.getLogger(__name__)

class NewsAPIFetcher:
    """Fetch news from NewsAPI.org."""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_API_KEY')
        self.base_url = 'https://newsapi.org/v2'
        self.session = requests.Session()
    
    def fetch_latest_news(self, category='general', limit=50):
        """Fetch latest news from NewsAPI."""
        if not self.api_key:
            return []
        
        try:
            url = f'{self.base_url}/top-headlines'
            params = {
                'apiKey': self.api_key,
                'category': category,
                'pageSize': min(limit, 100),
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', []):
                item = {
                    'source': 'newsapi',
                    'source_name': (article.get('source') or {}).get('name', 'NewsAPI'),
                    'title': article.get('title'),
                    'content': article.get('description') or article.get('content'),
                    'url': article.get('url'),
                    'author': article.get('author'),
                    'published_at': article.get('publishedAt'),
                    'image_url': article.get('urlToImage'),
                }
                articles.append(normalize_media_fields(item))
            return articles
        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return []

"""Sitemap generation for SEO."""
import logging, os
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class SitemapGenerator:
    """Generate sitemap.xml for search engines."""
    
    def __init__(self):
        self.base_url = os.getenv('NEXT_PUBLIC_SITE_URL', 'https://example.com')
    
    def generate_sitemap(self, articles: List[Dict]) -> str:
        """Generate XML sitemap."""
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
        
        # Add homepage
        xml += f'''  <url>
    <loc>{self.base_url}</loc>
    <lastmod>{datetime.utcnow().isoformat()}</lastmod>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>
'''
        
        # Add articles
        for article in articles:
            slug = article.get('slug', '')
            url = f"{self.base_url}/news/{slug}"
            published_at = article.get('published_at', datetime.utcnow().isoformat())
            
            xml += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{published_at}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
        
        xml += '</urlset>'
        return xml
    
    def save_sitemap(self, articles: List[Dict], path: str = 'website/public/sitemap.xml'):
        """Save sitemap to file."""
        try:
            xml = self.generate_sitemap(articles)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(xml)
            logger.info(f"Saved sitemap with {len(articles)} URLs to {path}")
        except Exception as e:
            logger.error(f"Failed to save sitemap: {e}")

class JSONLDGenerator:
    """Generate JSON-LD structured data."""
    
    @staticmethod
    def article_schema(title: str, content: str, author: str, published_at: str, image_url: str = None) -> Dict:
        """Generate NewsArticle schema."""
        return {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": title,
            "description": content[:160],
            "author": {
                "@type": "Person",
                "name": author or "AI News"
            },
            "datePublished": published_at,
            "image": image_url or "",
            "articleBody": content
        }

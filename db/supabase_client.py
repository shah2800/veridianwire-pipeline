"""Supabase database client wrapper for autonomous news system."""
import os, json, logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Production-ready Supabase client with error handling."""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_KEY")
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY required")
        try:
            from supabase import create_client
            self.client = create_client(self.url, self.key)
            logger.info(f"Supabase connected: {self.url}")
        except ImportError:
            raise ImportError("pip install supabase")
    
    def _truncate(self, value: Optional[str], max_len: int) -> Optional[str]:
        if value is None:
            return None
        return value[:max_len] if len(value) > max_len else value

    def get_raw_news_by_url(self, url: str) -> Optional[Dict]:
        try:
            response = (
                self.client.table("raw_news")
                .select("*")
                .eq("url", url)
                .limit(1)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to lookup raw news by url: {e}")
            return None

    def insert_raw_news(self, source: str, url: str, title: str, content: str,
                       published_at=None, author=None, raw_json=None):
        media = raw_json or {}
        record = {
            "source": self._truncate(source, 500),
            "url": url,
            "title": self._truncate(title, 500),
            "content": content,
            "published_at": published_at or datetime.utcnow().isoformat(),
            "author": self._truncate(author, 255),
            "raw_json": media,
            "fetched_at": datetime.utcnow().isoformat(),
        }
        try:
            response = self.client.table("raw_news").insert(record).execute()
            return response.data[0] if response.data else record
        except Exception as e:
            err = str(e)
            if "23505" in err or "duplicate key" in err.lower():
                existing = self.get_raw_news_by_url(url)
                if existing:
                    return existing
            logger.error(f"Failed to insert raw news: {e}")
            raise
    
    def get_raw_news(self, limit: int = 100):
        try:
            return self.client.table("raw_news").select("*").limit(limit).execute().data or []
        except Exception as e:
            logger.error(f"Failed to get raw news: {e}")
            return []
    
    def insert_filtered_news(self, raw_news_id: int, title: str, content: str, score: float, dedup_hash: str):
        try:
            record = {
                "raw_news_id": raw_news_id, "title": title, "content": content,
                "score": score, "dedup_hash": dedup_hash,
                "processed_at": datetime.utcnow().isoformat(),
            }
            response = self.client.table("filtered_news").insert(record).execute()
            return response.data[0] if response.data else record
        except Exception as e:
            logger.error(f"Failed to insert filtered news: {e}")
            raise
    
    def insert_published_article(self, filtered_news_id: int, url: str, slug: str, content: str, seo_meta=None):
        try:
            record = {
                "filtered_news_id": filtered_news_id, "url": url, "slug": slug,
                "content": content, "seo_meta": seo_meta or {},
                "published_at": datetime.utcnow().isoformat(),
            }
            response = self.client.table("published_articles").insert(record).execute()
            return response.data[0] if response.data else record
        except Exception as e:
            logger.error(f"Failed to insert published article: {e}")
            raise
    
    def log_pipeline_event(self, stage: str, status: str, message: str, error=None, details=None):
        try:
            record = {
                "stage": stage, "status": status, "message": message, "error": error,
                "details": details or {}, "logged_at": datetime.utcnow().isoformat(),
            }
            response = self.client.table("pipeline_logs").insert(record).execute()
            return response.data[0] if response.data else record
        except Exception as e:
            logger.error(f"Failed to log: {e}")
            return {}
    
    def health_check(self):
        try:
            self.client.table("raw_news").select("id").limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

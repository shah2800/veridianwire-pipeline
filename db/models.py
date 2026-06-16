"""Database models for autonomous news system."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict

@dataclass
class RawNews:
    id: int
    source: str
    url: str
    title: str
    content: str
    published_at: datetime
    author: Optional[str]
    raw_json: Dict
    fetched_at: datetime

@dataclass
class FilteredNews:
    id: int
    raw_news_id: int
    title: str
    content: str
    score: float
    dedup_hash: str
    embedding: Optional[List[float]]
    processed_at: datetime

@dataclass
class PublishedArticle:
    id: int
    filtered_news_id: int
    url: str
    slug: str
    content: str
    seo_meta: Dict
    published_at: datetime

@dataclass
class PipelineLog:
    id: int
    stage: str
    status: str
    message: str
    error: Optional[str]
    details: Dict
    timestamp: datetime

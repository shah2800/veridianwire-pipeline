"""
Database layer for autonomous news system.
Handles Supabase connections, migrations, and ORM models.
"""
from .supabase_client import SupabaseClient
from .models import RawNews, FilteredNews, PublishedArticle, PipelineLog

__all__ = [
    'SupabaseClient',
    'RawNews',
    'FilteredNews', 
    'PublishedArticle',
    'PipelineLog'
]

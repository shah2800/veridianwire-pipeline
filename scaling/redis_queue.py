"""Optional Redis queue for parallel workers."""
import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class RedisQueue:
    def __init__(self, queue_name: str = "news_pipeline"):
        self.queue_name = queue_name
        self.redis_url = os.getenv("REDIS_URL")
        self._client = None
        if self.redis_url:
            try:
                import redis

                self._client = redis.from_url(self.redis_url)
            except Exception as e:
                logger.warning(f"Redis unavailable: {e}")

    def enqueue(self, item: Dict[str, Any]) -> bool:
        if not self._client:
            return False
        self._client.rpush(self.queue_name, json.dumps(item))
        return True

    def dequeue(self) -> Optional[Dict[str, Any]]:
        if not self._client:
            return None
        raw = self._client.lpop(self.queue_name)
        return json.loads(raw) if raw else None

    def size(self) -> int:
        if not self._client:
            return 0
        return int(self._client.llen(self.queue_name))

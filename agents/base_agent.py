"""Base agent class for autonomous news system."""
import logging, os
from typing import Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all pipeline agents."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.db = None
        self.max_retries = 3
        self.retry_delay = 1
    
    def log_event(self, status: str, message: str, error=None, details=None):
        """Log pipeline event."""
        if self.db:
            self.db.log_pipeline_event(
                stage=self.name,
                status=status,
                message=message,
                error=str(error) if error else None,
                details=details
            )
        logger.info(f"{self.name}: {status} - {message}")
    
    def retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff."""
        import time
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = self.retry_delay ** attempt
                logger.warning(f"Retry {attempt+1}/{self.max_retries} in {wait_time}s: {e}")
                time.sleep(wait_time)
        return None
    
    def process(self, data: Dict) -> Dict:
        """Process data. Override in subclasses."""
        raise NotImplementedError

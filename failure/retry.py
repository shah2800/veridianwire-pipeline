"""Exponential backoff retry logic."""
import time, logging, random

logger = logging.getLogger(__name__)

class RetryConfig:
    def __init__(self, max_retries=3, initial_delay=1, max_delay=60, backoff_factor=2):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

def retry_with_backoff(func, args=(), kwargs=None, config=None):
    """Execute function with exponential backoff."""
    if config is None:
        config = RetryConfig()
    if kwargs is None:
        kwargs = {}
    
    for attempt in range(config.max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == config.max_retries - 1:
                logger.error(f"Failed after {config.max_retries} attempts: {e}")
                raise
            
            delay = min(
                config.initial_delay * (config.backoff_factor ** attempt),
                config.max_delay
            )
            jitter = random.uniform(0, delay * 0.1)
            actual_delay = delay + jitter
            
            logger.warning(f"Attempt {attempt+1} failed, retrying in {actual_delay:.1f}s: {e}")
            time.sleep(actual_delay)
    
    return None

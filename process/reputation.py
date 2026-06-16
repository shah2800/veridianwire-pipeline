"""Source reputation scoring."""
import logging

logger = logging.getLogger(__name__)

class ReputationScorer:
    """Score news sources by reliability."""
    
    # Base trust scores for known sources
    TRUSTED_SOURCES = {
        'bbc': 0.95,
        'reuters': 0.95,
        'guardian': 0.90,
        'ap': 0.95,
        'cnn': 0.85,
        'techcrunch': 0.85,
        'newsapi': 0.70,
    }
    
    def __init__(self):
        self.scores = self.TRUSTED_SOURCES.copy()
    
    def get_source_score(self, source: str) -> float:
        """Get trust score for source (0-1)."""
        source_lower = source.lower()
        return self.scores.get(source_lower, 0.5)
    
    def penalize_source(self, source: str, amount: float = 0.05):
        """Penalize source for inaccuracy."""
        source_lower = source.lower()
        if source_lower in self.scores:
            self.scores[source_lower] = max(0.1, self.scores[source_lower] - amount)
            logger.info(f"Penalized {source}: {self.scores[source_lower]}")
    
    def reward_source(self, source: str, amount: float = 0.05):
        """Reward source for accuracy."""
        source_lower = source.lower()
        if source_lower in self.scores:
            self.scores[source_lower] = min(1.0, self.scores[source_lower] + amount)
            logger.info(f"Rewarded {source}: {self.scores[source_lower]}")

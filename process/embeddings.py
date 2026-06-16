"""Text embeddings for article clustering."""
import os, logging
from typing import List

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Generate embeddings using OpenAI."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
            self.model = os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
        except ImportError:
            logger.error("openai not installed")
            self.client = None
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        if not self.client:
            return []
        
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text[:8000]  # Limit input length
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            return []
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity."""
        import math
        if not vec1 or not vec2:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a * a for a in vec1))
        mag2 = math.sqrt(sum(b * b for b in vec2))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)

"""MinHash-based deduplication for news articles."""
import hashlib
import logging
import os
from typing import List

logger = logging.getLogger(__name__)

class MinHashDeduplicator:
    """Dedup articles using MinHash signatures."""
    
    def __init__(self, num_hashes=128):
        self.num_hashes = num_hashes
        self.dedup_threshold = float(os.getenv('DEDUP_THRESHOLD', 0.85))
    
    def _tokenize(self, text: str):
        """Split text into tokens."""
        import re
        words = re.findall(r'\w+', text.lower())
        return [w for w in words if len(w) > 2]
    
    def _hash_token(self, token: str, seed: int):
        """Hash a token with seed."""
        h = hashlib.md5((str(seed) + token).encode())
        return int(h.hexdigest(), 16)
    
    def compute_signature(self, text: str):
        """Compute MinHash signature."""
        tokens = self._tokenize(text)
        if not tokens:
            return [0] * self.num_hashes
        
        signature = []
        for i in range(self.num_hashes):
            hashes = [self._hash_token(token, i) for token in tokens]
            signature.append(min(hashes))
        return signature
    
    def jaccard_similarity(self, sig1: List[int], sig2: List[int]):
        """Estimate Jaccard similarity from signatures."""
        if len(sig1) != len(sig2):
            return 0.0
        matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
        return matches / len(sig1)
    
    def is_duplicate(self, text1: str, text2: str):
        """Check if two articles are duplicates."""
        sig1 = self.compute_signature(text1)
        sig2 = self.compute_signature(text2)
        similarity = self.jaccard_similarity(sig1, sig2)
        return similarity >= self.dedup_threshold

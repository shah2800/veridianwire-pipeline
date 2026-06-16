"""MinHash deduplication tests."""
from process.minhash import MinHashDeduplicator


def test_identical_articles_are_duplicates():
    d = MinHashDeduplicator()
    t = "Breaking news: major tech company announces new AI product today"
    assert d.is_duplicate(t, t)


def test_different_articles_not_duplicates():
    d = MinHashDeduplicator()
    a = "Football team wins championship in dramatic final"
    b = "Stock market reaches record high amid inflation data"
    assert not d.is_duplicate(a, b)


def test_similar_headlines_may_duplicate():
    d = MinHashDeduplicator(num_hashes=128)
    a = "Apple releases new iPhone with improved camera system"
    b = "Apple releases new iPhone with better camera features"
    sig1 = d.compute_signature(a)
    sig2 = d.compute_signature(b)
    sim = d.jaccard_similarity(sig1, sig2)
    assert sim > 0.3


def test_empty_text_signature():
    d = MinHashDeduplicator()
    sig = d.compute_signature("")
    assert len(sig) == 128


def test_signature_length():
    d = MinHashDeduplicator(num_hashes=64)
    sig = d.compute_signature("hello world news article")
    assert len(sig) == 64

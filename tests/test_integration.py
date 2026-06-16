"""Light integration tests (no live API calls)."""
from process.spam_filter import SpamFilter
from process.gate import ConfidenceGate


def test_spam_filter_rejects_short_title():
    sf = SpamFilter(min_title_length=10, min_content_length=50)
    is_spam, _ = sf.is_spam({"title": "Hi", "content": "x" * 20})
    assert is_spam


def test_confidence_gate_passes_good_article():
    gate = ConfidenceGate(threshold=0.5)
    article = {
        "title": "Major policy change announced by government officials today",
        "content": "A" * 300,
        "source_name": "reuters",
    }
    passes, score, _ = gate.passes_gate(article)
    assert passes
    assert score >= 0.5

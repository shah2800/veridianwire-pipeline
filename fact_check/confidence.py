"""Fact-check confidence scoring."""
from typing import Dict, List


def score_confidence(
    title: str,
    source_count: int,
    serp_matches: int = 0,
) -> float:
    """
    Score 0-1: higher = more likely accurate.
    source_count: how many fetchers had similar headlines this cycle.
    serp_matches: optional SerpAPI corroboration count.
    """
    base = 0.5
    if source_count >= 2:
        base += 0.25
    elif source_count >= 1:
        base += 0.1
    if serp_matches >= 2:
        base += 0.2
    elif serp_matches >= 1:
        base += 0.1
    if len(title or "") > 20:
        base += 0.05
    return min(base, 1.0)

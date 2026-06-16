"""Fetcher fallback chain helpers."""
import logging
from typing import Callable, List, TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T")


def run_fallback_chain(steps: List[tuple], default: T = None) -> T:
    """
    Run named fetch steps until one returns a non-empty result.
    steps: [(name, callable), ...]
    """
    for name, fn in steps:
        try:
            result = fn()
            if result:
                logger.info(f"Fallback chain: {name} succeeded")
                return result
        except Exception as e:
            logger.warning(f"Fallback chain: {name} failed: {e}")
    return default

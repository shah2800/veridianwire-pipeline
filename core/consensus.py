"""Update consensus.md after each pipeline cycle."""
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

CONSENSUS_PATH = Path(__file__).resolve().parent.parent / "consensus.md"


def update_consensus(stats: Dict[str, Any], errors: Optional[list] = None) -> None:
    """Write pipeline state to consensus.md."""
    errors = errors or []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    err_block = "\n".join(f"- {e}" for e in errors[:10]) if errors else "None"

    content = f"""# Consensus Memory - Autonomous News System State

This file is auto-updated each daemon cycle.

## Last Successful Cycle

- Timestamp: {ts}
- Articles Fetched: {stats.get('fetched', 0)}
- Articles After Spam/Gate: {stats.get('passed_quality', 0)}
- Articles Filtered (DB): {stats.get('filtered', 0)}
- Articles Published: {stats.get('published', 0)}
- Skipped (duplicate): {stats.get('skipped_dup', 0)}
- Skipped (spam): {stats.get('skipped_spam', 0)}
- Skipped (low confidence): {stats.get('skipped_gate', 0)}
- Skipped (fact-check): {stats.get('skipped_fact_check', 0)}

## Recent Errors

{err_block}

## API Status

- OpenAI: {stats.get('openai_status', 'unknown')}
- Groq: {stats.get('groq_status', 'unknown')}
- NewsAPI: {stats.get('newsapi_status', 'unknown')}
- GDELT: {stats.get('gdelt_status', 'unknown')}

## Sources Active

{stats.get('sources', 'NewsAPI, RSS, GDELT')}

## Next Cycle

- Interval: {os.getenv('DAEMON_INTERVAL_MINUTES', '10')} minutes
- Publish limit per cycle: {stats.get('publish_limit', 10)}
"""
    CONSENSUS_PATH.write_text(content, encoding="utf-8")

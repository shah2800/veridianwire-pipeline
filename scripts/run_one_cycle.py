"""Run a single daemon pipeline cycle (fetch, filter, publish)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from daemon import NewsDaemon

if __name__ == "__main__":
    NewsDaemon().run_cycle()

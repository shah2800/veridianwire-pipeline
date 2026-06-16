"""Git commit and push for published content."""
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent.parent


class GitManager:
    def __init__(self, repo_path: Path = ROOT):
        self.repo_path = repo_path

    def commit_and_push(self, message: str = None) -> bool:
        if not os.getenv("GITHUB_TOKEN") and not self._is_git_repo():
            logger.info("Git push skipped (no repo or token)")
            return False

        msg = message or f"auto: publish articles {datetime.utcnow().isoformat()}"
        cmds = [
            ["git", "add", "website/public/sitemap.xml", "logs/"],
            ["git", "commit", "-m", msg],
            ["git", "push"],
        ]
        for cmd in cmds:
            try:
                subprocess.run(
                    cmd,
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                logger.warning(f"Git step failed ({cmd[1]}): {e.stderr or e}")
                return False
        logger.info("Git commit and push OK")
        return True

    def _is_git_repo(self) -> bool:
        return (self.repo_path / ".git").exists()

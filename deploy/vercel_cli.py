"""Deploy website to Vercel."""
import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent.parent


class VercelDeployer:
    def deploy_production(self) -> bool:
        token = os.getenv("VERCEL_TOKEN")
        if not token:
            logger.info("VERCEL_TOKEN not set — skip deploy")
            return False
        env = {**os.environ, "VERCEL_TOKEN": token}
        try:
            subprocess.run(
                ["npx", "vercel", "--prod", "--yes"],
                cwd=ROOT / "website",
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info("Vercel deploy OK")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Vercel deploy failed: {e.stderr or e}")
            return False

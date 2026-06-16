"""
Autonomous news business daemon — 24/7 agent orchestrator.
DataAgent -> FilterAgent -> WriteAgent -> SEOAgent -> PublishAgent
"""
import logging
import logging.handlers
import os
import signal
import time

from dotenv import load_dotenv

load_dotenv()

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.handlers.RotatingFileHandler(
        f"{log_dir}/daemon.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

from agents.data_agent import DataAgent
from agents.filter_agent import FilterAgent
from agents.publish_agent import PublishAgent
from agents.seo_agent import SEOAgent
from agents.write_agent import WriteAgent
from core.consensus import update_consensus
from db.supabase_client import SupabaseClient
from failure.alerting import AlertingSystem
from fetchers.fetch_manager import FetchManager
from llm.fallback import GroqClient
from llm.primary import OpenAIClient
from process.minhash import MinHashDeduplicator


class NewsDaemon:
    """Autonomous news pipeline using five agents."""

    def __init__(self):
        self.running = True
        self.interval = int(os.getenv("DAEMON_INTERVAL_MINUTES", 10)) * 60
        self.alerts = AlertingSystem()
        self.db = SupabaseClient()
        self.fetcher = FetchManager()
        self.dedup = MinHashDeduplicator()
        self.groq = GroqClient()
        self.openai = None
        try:
            self.openai = OpenAIClient()
            logger.info("OpenAI available")
        except ValueError:
            logger.warning("OpenAI not configured — using Groq + basic SEO")

        self.data_agent = DataAgent(self.db, self.fetcher)
        self.filter_agent = FilterAgent(self.db, self.dedup)
        self.write_agent = WriteAgent(self.db, self.groq, self.openai)
        self.seo_agent = SEOAgent(self.db, self.openai)
        self.publish_agent = PublishAgent(self.db)
        logger.info("Daemon initialized (5-agent pipeline)")

    def signal_handler(self, sig, frame):
        logger.info("Shutdown signal received")
        self.running = False

    def run_cycle(self):
        logger.info("Starting pipeline cycle...")
        ctx = {"errors": [], "publish_limit": int(os.getenv("PUBLISH_LIMIT_PER_CYCLE", 10))}
        failure_rate = 0.0

        try:
            ctx = self.data_agent.run(ctx)
            if not ctx.get("articles"):
                self.alerts.alert_error("DataAgent", "No articles fetched")
            ctx = self.filter_agent.run(ctx)
            ctx = self.write_agent.run(ctx)
            ctx = self.seo_agent.run(ctx)
            ctx = self.publish_agent.run(ctx)

            published = ctx.get("published_count", 0)
            fetched = ctx.get("fetched", 0)
            if fetched:
                failure_rate = 1 - (published / max(fetched, 1))

            stats = {
                "fetched": fetched,
                "passed_quality": ctx.get("passed_quality", 0),
                "filtered": ctx.get("filtered_count", 0),
                "published": published,
                "skipped_dup": ctx.get("skipped_dup", 0),
                "skipped_spam": ctx.get("skipped_spam", 0),
                "skipped_gate": ctx.get("skipped_gate", 0),
                "skipped_fact_check": ctx.get("skipped_fact_check", 0),
                "publish_limit": ctx.get("publish_limit", 10),
                "openai_status": "ok" if self.openai else "disabled",
                "groq_status": "ok" if self.groq.client else "disabled",
                "newsapi_status": ctx.get("fetch_status", {}).get("newsapi", "unknown"),
                "gdelt_status": ctx.get("fetch_status", {}).get("gdelt", "unknown"),
                "sources": "NewsAPI, RSS, GDELT",
            }
            update_consensus(stats, ctx.get("errors"))

            self.db.log_pipeline_event(
                stage="daemon",
                status="success",
                message=f"Cycle done: fetched {fetched}, published {published}",
                details=stats,
            )
            self.db.cleanup_old_logs(retention_days=30)

            if failure_rate > 0.1 and fetched > 5:
                self.alerts.alert_error(
                    "daemon",
                    f"High failure rate: {failure_rate:.0%}",
                    details=f"published {published}/{fetched}",
                )
            elif published:
                self.alerts.alert_success("daemon", f"Published {published} articles")

            logger.info(f"Published {published} articles")

        except Exception as e:
            logger.error(f"Pipeline cycle failed: {e}")
            ctx.setdefault("errors", []).append(str(e))
            self.db.log_pipeline_event(
                stage="daemon",
                status="failed",
                message="Pipeline cycle failed",
                error=str(e),
            )
            self.alerts.alert_error("daemon", str(e))

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        logger.info(f"Daemon starting (interval: {self.interval}s)")

        while self.running:
            try:
                self.run_cycle()
            except Exception as e:
                logger.error(f"Cycle error: {e}")
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)
        logger.info("Daemon stopped")


if __name__ == "__main__":
    NewsDaemon().run()

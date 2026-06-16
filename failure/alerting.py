"""Alerting system for errors and important events."""
import os, logging, requests
from typing import Optional

logger = logging.getLogger(__name__)

class AlertingSystem:
    """Send alerts to Discord, Email, etc."""
    
    def __init__(self):
        self.discord_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.email = os.getenv('EMAIL_ALERTS')
    
    def alert_error(self, stage: str, error: str, details: Optional[str] = None):
        """Alert about pipeline error."""
        message = f"ERROR in {stage}: {error}"
        if details:
            message += f"\n{details}"
        
        if self.discord_url:
            self._send_discord(message, color=16711680)
        
        logger.error(message)
    
    def alert_success(self, stage: str, message: str):
        """Alert about successful operation."""
        full_message = f"SUCCESS in {stage}: {message}"
        
        if self.discord_url:
            self._send_discord(full_message, color=65280)
        
        logger.info(full_message)
    
    def _send_discord(self, message: str, color: int = 3447003):
        """Send message to Discord webhook."""
        try:
            payload = {
                "embeds": [{
                    "title": "News Daemon Alert",
                    "description": message,
                    "color": color,
                }]
            }
            requests.post(self.discord_url, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")

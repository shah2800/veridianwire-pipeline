"""Groq Llama fallback wrapper."""
import logging
import os

from core.rewrite_quality import build_rewrite_prompt

logger = logging.getLogger(__name__)


class GroqClient:
    """Groq Llama wrapper for fallback."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama-3.1-8b-instant"

        try:
            from groq import Groq

            self.client = Groq(api_key=self.api_key) if self.api_key else None
        except ImportError:
            logger.warning("groq not installed")
            self.client = None

    def rewrite_article(self, title: str, content: str, *, strict: bool = False):
        """Rewrite article using Groq."""
        if not self.client:
            return None

        try:
            prompt = build_rewrite_prompt(title, content, strict=strict)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000,
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq rewrite failed: {e}")
            return None

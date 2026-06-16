"""OpenAI GPT-4o-mini wrapper."""
import os, logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class OpenAIClient:
    """OpenAI wrapper with error handling."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY required")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("pip install openai")
    
    def rewrite_article(self, title: str, content: str, temperature=0.3):
        """Rewrite article for SEO."""
        try:
            from core.rewrite_quality import build_rewrite_prompt

            prompt = (
                build_rewrite_prompt(title, content)
                + "\n\nReturn JSON with keys: title, content, summary, keywords. "
                "The content field must be HTML paragraphs only, with no bracket placeholders."
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI rewrite failed: {e}")
            return None
    
    def generate_seo_meta(self, title: str, content: str):
        """Generate SEO metadata."""
        try:
            prompt = f"""Generate SEO metadata for this article:
Title: {title}
Content: {content}

Provide JSON with: meta_description (max 160 chars), keywords (list), og_title, og_description"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI meta generation failed: {e}")
            return None

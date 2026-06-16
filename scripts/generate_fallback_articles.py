"""Generate local fallback articles JSON with full article bodies for the website."""
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import feedparser
from dotenv import load_dotenv

load_dotenv()

from fetchers.article_content import plain_text, resolve_article_body, rss_entry_content
from fetchers.media_utils import normalize_media_fields
from fetchers.og_image import fetch_og_image
from fetchers.rss import RSSFetcher, _rss_image, _rss_video

FEEDS = {
    "techcrunch": "https://techcrunch.com/feed/",
    "bbc": "https://feeds.bbc.co.uk/news/rss.xml",
}


def slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", (title or "article").lower())
    return re.sub(r"[-\s]+", "-", slug).strip("-")[:200] or "article"


def maybe_rewrite(title: str, content_html: str) -> str:
    """Optional Groq rewrite when API key is available."""
    from core.rewrite_quality import is_bad_rewrite, build_rewrite_prompt

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return content_html
    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        text = plain_text(content_html)[:4000]
        prompt = build_rewrite_prompt(title, text)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000,
        )
        rewritten = response.choices[0].message.content or ""
        if is_bad_rewrite(rewritten):
            prompt = build_rewrite_prompt(title, text, strict=True)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000,
            )
            rewritten = response.choices[0].message.content or ""
        if is_bad_rewrite(rewritten):
            return content_html
        if len(plain_text(rewritten)) > 200:
            return rewritten if "<p" in rewritten else f"<p>{rewritten}</p>"
    except Exception as e:
        print(f"  Groq rewrite skipped: {e}")
    return content_html


def main():
    limit = int(os.getenv("FALLBACK_ARTICLE_LIMIT", "10"))
    out = []

    for source_name, feed_url in FEEDS.items():
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:limit]:
            title = entry.get("title", "")
            url = entry.get("link", "")
            if not title or not url:
                continue

            print(f"  Fetching: {title[:55]}...")
            body = resolve_article_body(entry, url)
            body = maybe_rewrite(title, body)
            word_count = len(plain_text(body).split())

            image_url = _rss_image(entry)
            if not image_url:
                image_url = fetch_og_image(url)

            summary = entry.get("summary") or entry.get("description") or plain_text(body)[:300]

            out.append(
                {
                    "slug": slugify(title),
                    "content": body,
                    "published_at": entry.get("published") or datetime.now(timezone.utc).isoformat(),
                    "seo_meta": {
                        "meta_title": title[:70],
                        "meta_description": plain_text(summary)[:300],
                        "category": "technology" if source_name == "techcrunch" else "news",
                        "image_url": image_url,
                        "video_url": _rss_video(entry),
                        "source_url": url,
                        "source_name": feed.feed.get("title", source_name),
                    },
                }
            )
            print(f"    -> {word_count} words, image={'yes' if image_url else 'no'}")

        if len(out) >= limit:
            break

    dest = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "website",
        "public",
        "fallback-articles.json",
    )
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out[:limit], f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(out[:limit])} full articles to {dest}")


if __name__ == "__main__":
    main()

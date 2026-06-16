"""Generate SEO metadata without OpenAI (fallback)."""
import re
from typing import Dict


def _slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", (title or "article").lower())
    return re.sub(r"[-\s]+", "-", slug).strip("-")[:200] or "article"


def basic_seo_meta(title: str, content: str, source: str = "news") -> Dict:
    """Build SEO meta from title and content when LLM is unavailable."""
    from core.rewrite_quality import extract_clean_summary

    desc = extract_clean_summary(content, max_len=160)
    if not desc:
        desc = (content or "")[:300].strip()
        if len(desc) > 297:
            desc = desc[:297] + "..."
    category = _guess_category(title, content)
    return {
        "meta_title": (title or "News Article")[:70],
        "meta_description": desc or "Latest news and analysis.",
        "keywords": ", ".join(_extract_keywords(title, content)[:8]),
        "category": category,
        "source": source,
    }


def enrich_seo_with_media(seo_meta: Dict, source_article: Dict) -> Dict:
    """Attach image, video, and source attribution from the original fetch."""
    out = dict(seo_meta or {})
    for key in ("image_url", "video_url", "source_url", "source_name"):
        val = source_article.get(key)
        if val and not out.get(key):
            out[key] = val

    if not out.get("image_url"):
        from fetchers.media_utils import extract_image_from_html
        html = source_article.get("content") or source_article.get("description") or ""
        img = extract_image_from_html(html)
        if img:
            out["image_url"] = img

    if not out.get("image_url") and source_article.get("url"):
        try:
            from fetchers.og_image import fetch_og_image
            og = fetch_og_image(source_article["url"])
            if og:
                out["image_url"] = og
        except Exception:
            pass

    if not out.get("source_url") and source_article.get("url"):
        out["source_url"] = source_article["url"]
    if not out.get("source_name"):
        out["source_name"] = source_article.get("source_name") or source_article.get("source", "")

    return out


def _guess_category(title: str, content: str) -> str:
    """Classify by title-first keyword scoring (avoids 'ai' false positives in body)."""
    title_l = (title or "").lower()
    body_l = (content or "")[:2000].lower()

    rules = [
        (
            "politics",
            [
                "trump", "biden", "election", "congress", "senate", "gop", "democrat",
                "republican", "president", "white house", "politico", "policy", "vote",
                "iran", "macron", "g7", "versailles", "immigration", "pride month", "ogles",
            ],
        ),
        (
            "business",
            [
                "stock market", "stock", "market", "dow", "nasdaq", "economy", "ceo",
                "earnings", "ipo", "finance", "mortgage", "wsj", "business",
            ],
        ),
        (
            "sports",
            ["ufc", "mma", "nfl", "nba", "soccer", "football", "championship", "jersey", "sports"],
        ),
        (
            "health",
            ["health", "hospital", "medical", "adhd", "chronic pain", "virus", "covid", "wellness"],
        ),
        (
            "science",
            ["research", "space", "nasa", "scientists", "study finds", "satellite"],
        ),
        (
            "world",
            ["swiss", "colombia", "international", "global", "migration", "europe", "world"],
        ),
        (
            "technology",
            [
                "microsoft", "openai", "apple", "google", "software", "startup",
                "techcrunch", "verge", "tech", "ai assistant", "build 2026", "llm",
            ],
        ),
    ]

    def score(keywords: list) -> int:
        total = 0
        for kw in keywords:
            if kw in title_l:
                total += 4
            elif kw in body_l:
                total += 1
        return total

    best_cat, best_score = "world", 0
    for cat, keywords in rules:
        s = score(keywords)
        if s > best_score:
            best_cat, best_score = cat, s
    return best_cat


def _extract_keywords(title: str, content: str) -> list:
    words = re.findall(r"\b[a-z]{4,}\b", f"{title} {content}".lower())
    stop = {"that", "this", "with", "from", "have", "been", "will", "their", "about", "after"}
    seen = set()
    out = []
    for w in words:
        if w not in stop and w not in seen:
            seen.add(w)
            out.append(w)
        if len(out) >= 10:
            break
    return out or ["news", "breaking"]

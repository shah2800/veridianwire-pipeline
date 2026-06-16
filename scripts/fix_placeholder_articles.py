"""Re-rewrite published articles that contain AI placeholder text."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from core.rewrite_quality import find_bracket_placeholders, is_bad_rewrite
from core.seo_meta import basic_seo_meta, enrich_seo_with_media
from db.supabase_client import SupabaseClient
from fetchers.article_content import to_article_html
from llm.fallback import GroqClient


def _source_for_row(db: SupabaseClient, row: dict) -> dict:
    source = {"title": "", "content": "", "url": "", "source": "news"}
    fid = row.get("filtered_news_id")
    if not fid:
        return source

    filtered = (
        db.client.table("filtered_news")
        .select("title, content, raw_news_id")
        .eq("id", fid)
        .single()
        .execute()
    )
    if not filtered.data:
        return source

    source["title"] = filtered.data.get("title") or ""
    source["content"] = filtered.data.get("content") or ""

    raw_id = filtered.data.get("raw_news_id")
    if raw_id:
        raw = (
            db.client.table("raw_news")
            .select("url, raw_json, source")
            .eq("id", raw_id)
            .single()
            .execute()
        )
        if raw.data:
            source["url"] = raw.data.get("url") or ""
            source["source"] = raw.data.get("source") or "news"
            rj = raw.data.get("raw_json") or {}
            if isinstance(rj, str):
                try:
                    rj = json.loads(rj)
                except json.JSONDecodeError:
                    rj = {}
            source.update(rj)
    return source


def _rewrite(groq: GroqClient, title: str, content: str) -> str:
    text = groq.rewrite_article(title, content, strict=False)
    if text and is_bad_rewrite(text):
        text = groq.rewrite_article(title, content, strict=True)
    if text and is_bad_rewrite(text):
        return to_article_html(content)
    return text or to_article_html(content)


def main():
    db = SupabaseClient()
    groq = GroqClient()
    if not groq.client:
        print("GROQ_API_KEY required to re-rewrite articles.")
        sys.exit(1)

    rows = (
        db.client.table("published_articles")
        .select("id, slug, content, seo_meta, filtered_news_id")
        .order("published_at", desc=True)
        .limit(500)
        .execute()
        .data
        or []
    )

    fixed = 0
    for row in rows:
        content = row.get("content") or ""
        seo = row.get("seo_meta") or {}
        if isinstance(seo, str):
            seo = json.loads(seo)
        meta_desc = seo.get("meta_description") or ""

        if not is_bad_rewrite(content) and not is_bad_rewrite(meta_desc):
            continue

        source = _source_for_row(db, row)
        title = source.get("title") or row.get("slug", "").replace("-", " ")
        src_content = source.get("content") or content
        placeholders = find_bracket_placeholders(content)
        print(f"Fixing: {row['slug']}")
        if placeholders:
            print(f"  placeholders: {sorted(set(placeholders))[:5]}")

        new_content = _rewrite(groq, title, src_content)
        new_seo = basic_seo_meta(title, new_content, source.get("source", "news"))
        new_seo = enrich_seo_with_media({**seo, **new_seo}, source)

        db.client.table("published_articles").update(
            {"content": new_content, "seo_meta": new_seo}
        ).eq("id", row["id"]).execute()
        fixed += 1

    print(f"Done. Fixed {fixed} articles.")


if __name__ == "__main__":
    main()

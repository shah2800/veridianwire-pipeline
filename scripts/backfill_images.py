"""Backfill image_url and video_url on published articles missing media in seo_meta."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from core.seo_meta import enrich_seo_with_media
from db.supabase_client import SupabaseClient
from fetchers.og_image import fetch_og_image


def main():
    db = SupabaseClient()
    rows = (
        db.client.table("published_articles")
        .select("id, slug, seo_meta, filtered_news_id")
        .order("published_at", desc=True)
        .limit(500)
        .execute()
    )
    updated = 0
    for row in rows.data or []:
        seo = row.get("seo_meta") or {}
        if seo.get("image_url"):
            continue

        source = {}
        fid = row.get("filtered_news_id")
        if fid:
            filtered = (
                db.client.table("filtered_news")
                .select("raw_news_id")
                .eq("id", fid)
                .single()
                .execute()
            )
            if filtered.data:
                raw = (
                    db.client.table("raw_news")
                    .select("url, raw_json")
                    .eq("id", filtered.data["raw_news_id"])
                    .single()
                    .execute()
                )
                if raw.data:
                    source["url"] = raw.data.get("url")
                    rj = raw.data.get("raw_json") or {}
                    source.update(rj)

        if not source.get("image_url") and source.get("url"):
            og = fetch_og_image(source["url"])
            if og:
                source["image_url"] = og

        new_seo = enrich_seo_with_media(seo, source)
        if new_seo.get("image_url") or new_seo.get("video_url"):
            db.client.table("published_articles").update({"seo_meta": new_seo}).eq(
                "id", row["id"]
            ).execute()
            updated += 1
            print(f"Updated: {row['slug']}")

    print(f"Done. Updated {updated} articles.")


if __name__ == "__main__":
    main()

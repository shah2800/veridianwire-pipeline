"""Re-classify article categories in seo_meta from titles."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from core.seo_meta import _guess_category
from db.supabase_client import SupabaseClient


def main():
    db = SupabaseClient()
    rows = (
        db.client.table("published_articles")
        .select("id, slug, content, seo_meta")
        .order("published_at", desc=True)
        .limit(500)
        .execute()
        .data
        or []
    )
    updated = 0
    for row in rows:
        seo = row.get("seo_meta") or {}
        if isinstance(seo, str):
            seo = json.loads(seo)
        title = seo.get("meta_title") or row.get("slug", "").replace("-", " ")
        content = row.get("content") or ""
        new_cat = _guess_category(title, content)
        if seo.get("category") == new_cat:
            continue
        seo["category"] = new_cat
        db.client.table("published_articles").update({"seo_meta": seo}).eq(
            "id", row["id"]
        ).execute()
        updated += 1
        print(f"  {new_cat:12} {row['slug'][:60]}")

    print(f"Done. Updated {updated} articles.")


if __name__ == "__main__":
    main()

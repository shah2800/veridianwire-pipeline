#!/usr/bin/env python3
"""Test Supabase connection and required tables."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

load_dotenv()

REQUIRED_TABLES = ("raw_news", "filtered_news", "published_articles", "pipeline_logs")
OPTIONAL_TABLES = ("profiles", "newsletter_subscribers")


def main():
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

    print("=" * 60)
    print("Supabase Connection Test")
    print("=" * 60)

    if not url or not key:
        print("FAIL: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
        sys.exit(1)

    print(f"URL: {url}")

    try:
        from supabase import create_client

        client = create_client(url, key)
        client.table("published_articles").select("id", count="exact").limit(1).execute()
        print("OK: Connected to Supabase")
    except Exception as e:
        err = str(e)
        if "getaddrinfo" in err or "ENOTFOUND" in err or "11001" in err:
            print("\nFAIL: Cannot resolve Supabase hostname.")
            print("  -> Project may be deleted, paused, or URL is wrong.")
            print("  -> Create a new project at https://supabase.com/dashboard")
            print("  -> Update SUPABASE_URL in .env and website/.env.local")
        elif "Invalid API key" in err or "401" in err:
            print("\nFAIL: Invalid API key.")
            print("  -> Copy service_role key from Project Settings -> API")
        else:
            print(f"\nFAIL: {e}")
        sys.exit(1)

    print("\nTables:")
    missing = []
    for table in REQUIRED_TABLES:
        try:
            client.table(table).select("id").limit(1).execute()
            print(f"  OK  {table}")
        except Exception as e:
            print(f"  MISSING  {table} ({e})")
            missing.append(table)

    for table in OPTIONAL_TABLES:
        try:
            client.table(table).select("id").limit(1).execute()
            print(f"  OK  {table} (optional)")
        except Exception:
            print(f"  SKIP {table} (optional — run scripts/website_auth_schema.sql)")

    if missing:
        print("\nRun DATABASE_SCHEMA.sql in Supabase SQL Editor, then:")
        print("  scripts/website_auth_schema.sql")
        sys.exit(2)

    count = client.table("published_articles").select("id", count="exact").execute()
    total = count.count if count.count is not None else 0
    print(f"\nPublished articles in DB: {total}")
    print("\nAll checks passed. Run: python scripts/run_one_cycle.py")
    sys.exit(0)


if __name__ == "__main__":
    main()

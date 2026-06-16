#!/usr/bin/env python3
"""Apply Supabase setup via Management API (requires SUPABASE_ACCESS_TOKEN in .env)."""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_REF = "awzukqmkmnucoxlkyeqs"
API_BASE = "https://api.supabase.com/v1"
ROOT = Path(__file__).resolve().parent.parent


def _headers() -> dict:
    token = os.getenv("SUPABASE_ACCESS_TOKEN", "").strip()
    if not token:
        raise SystemExit(
            "SUPABASE_ACCESS_TOKEN missing.\n"
            "Create one at https://supabase.com/dashboard/account/tokens\n"
            "Add to .env: SUPABASE_ACCESS_TOKEN=sbp_...\n"
            "Or connect Supabase MCP in Cursor (Settings → Tools & MCP) and sign in with OAuth."
        )
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def run_sql(query: str) -> dict:
    url = f"{API_BASE}/projects/{PROJECT_REF}/database/query"
    resp = requests.post(url, headers=_headers(), json={"query": query}, timeout=120)
    if resp.status_code >= 400:
        raise RuntimeError(f"SQL failed ({resp.status_code}): {resp.text[:500]}")
    return resp.json()


def fetch_anon_key() -> str:
    url = f"{API_BASE}/projects/{PROJECT_REF}/api-keys"
    resp = requests.get(url, headers=_headers(), timeout=30)
    if resp.status_code >= 400:
        raise RuntimeError(f"api-keys failed ({resp.status_code}): {resp.text[:300]}")
    data = resp.json()
    keys = data if isinstance(data, list) else data.get("data") or []
    for item in keys:
        name = (item.get("name") or item.get("type") or "").lower()
        if "anon" in name or "publishable" in name:
            return item.get("api_key") or item.get("key") or ""
    for item in keys:
        key = item.get("api_key") or item.get("key")
        if key and "service_role" not in (item.get("name") or "").lower():
            return key
    raise RuntimeError("Could not find anon/publishable key in API response")


def update_env_files(anon_key: str) -> None:
    env_path = ROOT / ".env"
    website_env = ROOT / "website" / ".env.local"
    supabase_url = f"https://{PROJECT_REF}.supabase.co"

    if env_path.exists():
        text = env_path.read_text(encoding="utf-8")
        if "SUPABASE_ANON_KEY=" in text:
            text = re.sub(
                r"^SUPABASE_ANON_KEY=.*$",
                f"SUPABASE_ANON_KEY={anon_key}",
                text,
                flags=re.M,
            )
        else:
            text += f"\nSUPABASE_ANON_KEY={anon_key}\n"
        env_path.write_text(text, encoding="utf-8")

    if website_env.exists():
        text = website_env.read_text(encoding="utf-8")
        text = re.sub(
            r"^NEXT_PUBLIC_SUPABASE_ANON_KEY=.*$",
            f"NEXT_PUBLIC_SUPABASE_ANON_KEY={anon_key}",
            text,
            flags=re.M,
        )
        if "NEXT_PUBLIC_SUPABASE_URL=" not in text:
            text += f"\nNEXT_PUBLIC_SUPABASE_URL={supabase_url}\n"
        website_env.write_text(text, encoding="utf-8")


def apply_auth_schema() -> None:
    sql_path = ROOT / "scripts" / "website_auth_schema.sql"
    sql = sql_path.read_text(encoding="utf-8")
    # Split on semicolons outside function bodies (simple split for our migration file)
    statements = []
    buf = []
    in_dollar = False
    for line in sql.splitlines():
        if "$$" in line:
            in_dollar = not in_dollar
        buf.append(line)
        if not in_dollar and line.rstrip().endswith(";"):
            chunk = "\n".join(buf).strip()
            if chunk and not chunk.startswith("--"):
                statements.append(chunk)
            buf = []
    if buf:
        chunk = "\n".join(buf).strip()
        if chunk and not chunk.startswith("--"):
            statements.append(chunk)

    for i, stmt in enumerate(statements, 1):
        preview = stmt.replace("\n", " ")[:80]
        print(f"  [{i}/{len(statements)}] {preview}...")
        run_sql(stmt)


def main():
    print("=" * 60)
    print("Supabase Management API Setup")
    print("=" * 60)

    print("\n1. Fetching anon/publishable API key...")
    anon = fetch_anon_key()
    print("   OK: anon key retrieved")

    print("\n2. Updating .env and website/.env.local...")
    update_env_files(anon)
    print("   OK: env files updated (service_role removed from NEXT_PUBLIC)")

    print("\n3. Applying website_auth_schema.sql...")
    apply_auth_schema()
    print("   OK: auth schema applied")

    print("\n4. Verifying tables...")
    from scripts.test_supabase import main as test_main

    test_main()
    print("\nDone.")


if __name__ == "__main__":
    main()

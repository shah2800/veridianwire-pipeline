# Supabase Setup Guide (End-to-End)

Your current project URL `awzukqmkmnucoxlkyeqs.supabase.co` does not resolve (DNS failure).
You need a **live Supabase project** and updated keys in `.env` + `website/.env.local`.

---

## Step 1 — Create or restore Supabase project

1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. **New project** (or open an existing active project)
3. Wait until status is **Active** (green)
4. Open **Project Settings → API** and copy:
   - **Project URL** → `https://YOUR-REF.supabase.co`
   - **anon public** key
   - **service_role** key (keep secret — server only)

---

## Step 2 — Update environment files

### Root `.env` (pipeline / Python)

```env
SUPABASE_URL=https://YOUR-REF.supabase.co
SUPABASE_SERVICE_KEY=eyJ...service_role...
SUPABASE_ANON_KEY=eyJ...anon...
```

### `website/.env.local` (Next.js)

```env
SUPABASE_URL=https://YOUR-REF.supabase.co
SUPABASE_SERVICE_KEY=eyJ...service_role...
NEXT_PUBLIC_SUPABASE_URL=https://YOUR-REF.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...anon...
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

**Important:** Never put `service_role` in `NEXT_PUBLIC_*` variables.

---

## Step 3 — Create database tables

In Supabase dashboard → **SQL Editor**, run in order:

1. `DATABASE_SCHEMA.sql` (core pipeline tables)
2. `scripts/website_auth_schema.sql` (profiles, newsletter, RLS)

---

## Step 4 — Test connection

```powershell
cd "d:\my ai projects 01.2\completly auto ai which upload news and gethere news"
python scripts\test_supabase.py
```

Expected: `All checks passed`

---

## Step 5 — Run one pipeline cycle

```powershell
python scripts\run_one_cycle.py
```

This will: fetch → filter → rewrite → SEO → publish to `published_articles`.

---

## Step 6 — Start full system

```powershell
# Terminal 1 — pipeline 24/7
python start_daemon.py

# Terminal 2 — website
npm run dev
```

Open http://localhost:3000 — articles come from Supabase (not fallback JSON).

---

## Step 7 — Backfill images on old articles (optional)

```powershell
python scripts\backfill_images.py
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ENOTFOUND` / DNS | Wrong or deleted project URL — create new project |
| `Invalid API key` | Re-copy keys from Supabase API settings |
| `relation does not exist` | Run `DATABASE_SCHEMA.sql` |
| Website empty but pipeline works | Check `website/.env.local` URL matches `.env` |
| RLS blocks reads | Run `scripts/website_auth_schema.sql` public read policy |

---

## Verify live data

```powershell
python scripts\test_supabase.py
python scripts\run_one_cycle.py
```

Then refresh the website. Articles should show full AI-rewritten content from `published_articles`.

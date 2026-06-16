# System Completion Status

Updated after full pipeline integration.

## Autonomy Level: ~75% (semi-autonomous → near-production)

### Fully working (no code changes needed from you)

| Feature | How to use |
|---------|------------|
| 5-agent pipeline | `python start_daemon.py` or `python daemon.py` |
| Fetch chain | NewsAPI → RSS → GDELT → cache |
| Spam + confidence gate | Automatic in FilterAgent |
| MinHash dedup | Automatic |
| Groq rewrite + basic SEO | Automatic (OpenAI optional) |
| Fact-check (batch + optional SerpAPI) | Automatic in SEOAgent |
| Supabase publish | Automatic |
| consensus.md | Auto-updated each cycle |
| Local website | `START_WEBSITE.bat` or `npm run dev` |
| Sitemap / robots | `/api/sitemap`, `/api/robots` |
| Category pages | `/category/technology`, etc. |
| API discovery CLI | `python -m fetchers.api_discovery https://www.bbc.com/news` |

### Optional (set in `.env`)

| Variable | Effect |
|----------|--------|
| `SERPAPI_API_KEY` | Stronger fact-check via Google search |
| `AUTO_DEPLOY=true` | Git commit + Vercel after publish |
| `VERCEL_TOKEN` | Required for deploy |
| `DISCORD_WEBHOOK_URL` | Alerts on errors/success |
| `REDIS_URL` | Enable queue (`scaling/redis_queue.py`) |
| `PUBLISH_LIMIT_PER_CYCLE=10` | Articles rewritten per cycle |

### Still manual / not cloud-autonomous

- Daemon must run on your PC or a VPS (not serverless by default)
- First-time Supabase SQL migrations
- Vercel production deploy (set `AUTO_DEPLOY` or run `npx vercel --prod` in `website/`)
- GitHub secrets for CI (`.github/workflows/deploy.yml`)

## Agent flow

```
DataAgent → FilterAgent → WriteAgent → SEOAgent → PublishAgent
   fetch      spam/gate/dedup    Groq      fact+SEO      DB+sitemap
```

## Quick commands

```powershell
cd "D:\my ai projects\completly auto ai which upload news and gethere news"
python start_daemon.py          # 24/7 pipeline
python scripts\run_one_cycle.py # single cycle
python -m fetchers.api_discovery https://techcrunch.com
START_WEBSITE.bat               # local site
```

# Autonomous AI News Business System

A fully automated, production-ready AI-powered news content business system that:

- Collects trending news from 100+ sources (NewsAPI, RSS, GDELT, discovered APIs)
- Filters, deduplicates, and ranks articles using MinHash + embeddings
- Rewrites news into SEO-optimized articles using GPT-4o-mini (with Groq fallback)
- Fact-checks claims by cross-referencing 2+ sources via SerpAPI
- Auto-publishes to a Next.js website via Git commit + Vercel deploy
- Runs 24/7 autonomously with circuit breakers, fallback chains, and auto-rollback
- Scales with Redis queues, parallel workers, and backpressure management
- Costs ~$10-15/month to operate

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (Supabase)
- API keys: OpenAI, Groq, NewsAPI, SerpAPI

### 1. Clone and Setup

```bash
git clone <repo>
cd autonomous-news-business
cp .env.example .env
# Fill in your API keys in .env
pip install -r requirements.txt
npm install
```

### 2. Initialize Database

```bash
# Create Supabase project at https://supabase.com
# Copy your Supabase URL and service key to .env

python scripts/seed_data.py
```

### 3. Deploy Website

```bash
bash scripts/deploy.sh
```

### 4. Start Daemon

```bash
python daemon.py
```

The daemon will run 24/7, fetching articles every 10 minutes.

## Architecture

```
Fetchers (NewsAPI, RSS, GDELT)
    |
    v
Process (MinHash dedup, embeddings, filtering)
    |
    v
Agents (Data, Filter, Write, SEO, Publish)
    |
    v
LLM (OpenAI gpt-4o-mini + Groq fallback)
    |
    v
Fact-Check (SerpAPI cross-reference)
    |
    v
Publish (Markdown -> Git -> Vercel)
    |
    v
SEO (Sitemap, Search Console, JSON-LD)
```

## File Structure

- `daemon.py` - Main 24/7 orchestrator
- `fetchers/` - Data collection (NewsAPI, RSS, API discovery)
- `process/` - Filtering and deduplication (MinHash, embeddings)
- `agents/` - AI pipeline agents (Data, Filter, Write, SEO, Publish)
- `llm/` - LLM wrappers (OpenAI, Groq)
- `fact_check/` - Fact verification via SerpAPI
- `website/` - Next.js frontend (Next.js 14, TailwindCSS)
- `db/` - Database layer (Supabase)
- `deploy/` - Deployment automation (Vercel, GitHub Actions)
- `seo/` - SEO optimization (sitemap, Search Console)
- `scaling/` - Performance scaling (Redis, workers, backpressure)
- `failure/` - Error handling (retries, fallbacks, alerts)
- `tests/` - Test suite

## Configuration

All configuration via environment variables in `.env`:

- `OPENAI_API_KEY` - OpenAI API key for gpt-4o-mini
- `GROQ_API_KEY` - Groq API key for Llama fallback
- `NEWSAPI_API_KEY` - NewsAPI.org key
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_SERVICE_KEY` - Supabase service key
- `VERCEL_TOKEN` - Vercel deployment token
- `DAEMON_INTERVAL_MINUTES` - How often daemon runs (default: 10)
- `DEDUP_THRESHOLD` - Similarity threshold for dedup (default: 0.85)
- `CONFIDENCE_THRESHOLD_PUBLISH` - Min score to publish (default: 0.8)

## Monitoring

Check daemon health and logs:

```bash
tail -f logs/daemon.log                    # View daemon logs
curl http://localhost:3000/api/health       # Website health
python scripts/monitor.py                  # Monitor API costs
```

## Cost Breakdown

- OpenAI gpt-4o-mini: ~$0.01 per article ($10/month for 1000 articles)
- Groq Llama: Free
- NewsAPI: Free (500 requests/month)
- Supabase: Free (500MB database)
- Vercel: Free (100GB bandwidth)
- Redis: $5/month (small instance)
- Total: ~$10-15/month

## License

MIT

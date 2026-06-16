# File & Directory Guide

Quick reference for navigating the codebase.

## Root Directory

| File | Purpose |
|------|---------|
| `daemon.py` | **MAIN ENTRY POINT** - 24/7 autonomous loop, orchestrates entire pipeline |
| `.env.example` | Template for environment variables, copy to `.env` before running |
| `consensus.md` | Persistent cross-cycle state (articles fetched/processed, metrics) |
| `requirements.txt` | Python package dependencies |
| `package.json` | Node.js dependencies and scripts |
| `pyproject.toml` | Python project configuration |
| `README.md` | Project overview and quick start |
| `BUILD_SUMMARY.md` | **READ THIS FIRST** - What's been built and how to use it |
| `FILE_GUIDE.md` | This file - Navigation guide |
| `.gitignore` | Git exclusions for secrets, builds, logs |
| `docker-compose.yml` | Local development with Docker |

## Core Modules

### `fetchers/` - Data Collection Layer

| File | Responsibility |
|------|-----------------|
| `fetch_manager.py` | **Orchestrator** - Fallback chain (NewsAPI → RSS → GDELT → Cache) |
| `newsapi.py` | NewsAPI fetcher (top headlines + search) |
| `rss.py` | RSS feed parser (14 pre-configured feeds) |
| `gdelt.py` | GDELT 2.0 fetcher (global event data) |

**Usage Flow**:
```
FetchManager.fetch_all_sources()
├─ NewsAPI (primary)
├─ RSS (fallback 1)
├─ GDELT (fallback 2)
└─ Cache (fallback 3)
→ Returns normalized articles
```

### `process/` - Filtering & Deduplication Layer

| File | Responsibility |
|------|-----------------|
| `minhash.py` | **Deduplication** - MinHash signatures + LSH for duplicate detection |
| `embeddings.py` | Text embeddings using sentence-transformers (semantic similarity) |
| `spam_filter.py` | Spam detection (5 heuristic checks) |
| `gate.py` | Confidence gating + source reputation scoring |
| `reputation.py` | Source trust scoring (Reuters=0.95, etc.) |

**Usage Flow**:
```
Articles
├─ SpamFilter.filter_articles() → Remove spam
├─ MinHashDeduplicator.add_article() → Remove duplicates
├─ ConfidenceGate.filter_articles() → Quality gating
└─ Passed articles → Next stage
```

### `agents/` - Agent Framework

| File | Responsibility |
|------|-----------------|
| `base_agent.py` | **Abstract base** - State management, error handling, statistics |
| (More agents ready to be built) | DataAgent, FilterAgent, WriteAgent, SEOAgent, PublishAgent |

**Pattern**: BaseAgent → Consensus Memory → Error Recovery

### `llm/` - Language Model Processing

| File | Responsibility |
|------|-----------------|
| `primary.py` | **OpenAI GPT-4o-mini** - Primary LLM with retry logic |
| `fallback.py` | **Groq Llama 3.1 8B** - Free fallback, same API |
| `prompts/` | Prompt templates (not yet created, for future use) |
| `schema_validator.py` | JSON schema validation |

**Functions**:
- `rewrite_article()` - Rewrite for clarity
- `generate_seo_meta()` - Generate title, description, keywords
- `extract_summary()` - Create summary
- `classify_category()` - Categorize article
- `detect_sentiment()` - Analyze sentiment

### `db/` - Database Layer

| File | Responsibility |
|------|-----------------|
| `supabase_client.py` | **Database wrapper** - Connection, queries, error handling |
| `schemas.py` | SQL migrations for 5 tables (raw_news, filtered_news, published_articles, pipeline_logs, versioned_articles) |
| `models.py` | ORM models (future) |

**Tables**:
- `raw_news` - Raw articles from sources
- `filtered_news` - After dedup/filtering
- `published_articles` - Final articles ready to serve
- `pipeline_logs` - Audit trail (stage, status, error)
- `versioned_articles` - Article history

### `failure/` - Failure Handling & Resilience

| File | Responsibility |
|------|-----------------|
| `retry.py` | **Exponential backoff retry** + CircuitBreaker pattern + DeadLetterQueue |
| `alerting.py` | **Multi-channel alerts** - Discord, Email, Slack webhooks |
| `token_bucket.py` | Rate limiting (future) |
| `stealth_mode.py` | Web scraping stealth features (future) |

**Patterns**:
- RetryPolicy: Exponential backoff (1s, 2s, 4s, 8s..., max 60s)
- CircuitBreaker: CLOSED → OPEN → HALF_OPEN → CLOSED
- DeadLetterQueue: JSON Lines format for manual review
- AlertManager: Unified alerting across channels

### `fact_check/` - Fact-Checking Layer

| File | Responsibility |
|------|-----------------|
| `cross_reference.py` | Cross-reference 2+ sources |
| `serpapi.py` | SerpAPI (Google Custom Search) wrapper |
| `confidence.py` | Confidence scoring |

**Status**: Skeleton ready for implementation

### `seo/` - SEO & Indexing

| File | Responsibility |
|------|-----------------|
| `sitemap.py` | Auto-generate sitemap.xml |
| `search_console.py` | Google Search Console API integration |
| `json_ld.py` | JSON-LD NewsArticle schema generation |
| `internal_links.py` | Build internal link graph |
| `core_web_vitals.py` | Performance optimization suggestions |

**Status**: Skeleton ready for implementation

### `scaling/` - Performance & Scaling

| File | Responsibility |
|------|-----------------|
| `redis_queue.py` | Redis + BullMQ for job queuing |
| `parallel_workers.py` | Parallel LLM worker pool |
| `backpressure.py` | Rate limiting and backpressure |
| `embedding_cache.py` | Cache embeddings to reduce API calls |
| `cost_monitor.py` | Track API spending |

**Status**: Skeleton ready for implementation

### `tests/` - Test Suite

| File | Purpose |
|------|---------|
| `test_fetchers.py` | Test fetcher functionality |
| `test_minhash.py` | Test deduplication |
| `test_llm.py` | Test LLM processing |
| `test_fact_check.py` | Test fact-checking |
| `test_publish.py` | Test publishing pipeline |
| `test_integration.py` | End-to-end pipeline test |

**Run**: `pytest tests/`

### `deploy/` - Deployment & CI/CD

| File | Purpose |
|------|---------|
| `github_actions.py` | GitHub Actions automation |
| `vercel_cli.py` | Vercel deployment wrapper |
| `cloudflare_dns.py` | Cloudflare DNS management |
| `git_manager.py` | Git commit + tag management |

**Status**: Skeleton ready for implementation

### `website/` - Next.js Frontend

#### Config Files

| File | Purpose |
|------|---------|
| `next.config.js` | Next.js configuration (ISR, headers, rewrites) |
| `tsconfig.json` | TypeScript configuration |
| `tailwind.config.js` | TailwindCSS configuration |
| `package.json` | Node dependencies |

#### Source Code (`src/`)

| Path | Purpose |
|------|---------|
| `app/layout.tsx` | Root layout (nav, footer) |
| `app/page.tsx` | Homepage with featured articles |
| `app/globals.css` | Global TailwindCSS + custom styles |
| `app/news/[slug]/page.tsx` | Dynamic article page (ISR) |
| `app/category/[tag]/page.tsx` | Dynamic category page (future) |
| `app/api/sitemap/route.ts` | Dynamic sitemap (future) |
| `app/api/robots/route.ts` | Dynamic robots.txt (future) |
| `lib/supabase.ts` | Supabase client + helper functions |
| `types/article.ts` | TypeScript interfaces |
| `components/seo.tsx` | SEO component (JSON-LD) |
| `components/article.tsx` | Article layout component |
| `components/navigation.tsx` | Navigation component |

#### Content (`content/news/`)
- Auto-generated markdown files (one per article)
- Frontmatter: title, slug, date, tags

### `scripts/` - Utility Scripts

| File | Purpose |
|------|---------|
| `setup.sh` | **Interactive setup wizard** - Prerequisites, env, dependencies, tests |
| `deploy.sh` | Deployment script (future) |
| `seed_data.py` | Seed database with test data |
| `stress_test.py` | 72-hour stress test |

### `docs/` - Documentation

| File | Purpose |
|------|---------|
| `SETUP.md` | **START HERE** - Step-by-step setup (45 min) |
| `ARCHITECTURE.md` | Technical deep-dive, diagrams, data flow |
| `OPERATIONS.md` | Daily/weekly/monthly maintenance guide |
| `DEPLOYMENT.md` | Deployment strategies |
| `COSTS.md` | Cost breakdown and optimization |
| `TROUBLESHOOTING.md` | Common issues and solutions |

---

## How Files Work Together

### Example: Process One Article

```
1. daemon.py (main loop)
   ↓
2. fetchers/fetch_manager.py (get articles)
   → fetchers/newsapi.py, rss.py, gdelt.py
   ↓
3. process/spam_filter.py (remove spam)
   ↓
4. process/minhash.py (remove duplicates)
   ↓
5. process/gate.py (confidence gating)
   ↓
6. llm/primary.py (rewrite with OpenAI)
   → llm/fallback.py (if OpenAI fails)
   ↓
7. db/supabase_client.py (save to database)
   ↓
8. website/ (render on Next.js)
   ↓
9. failure/alerting.py (notify user)
```

---

## Quick Navigation

**I want to...**

### Understand the system
→ Start with `BUILD_SUMMARY.md` → `README.md` → `docs/ARCHITECTURE.md`

### Get it running
→ `docs/SETUP.md` → `scripts/setup.sh` → `daemon.py`

### Fix a problem
→ `docs/TROUBLESHOOTING.md` → `daemon.log` → database logs

### Add a feature
→ Extend `agents/` or `llm/` or `deploy/` → Update `daemon.py` to call it

### Optimize costs
→ `docs/COSTS.md` → Adjust `.env` variables → Monitor with `failure/alerting.py`

### Monitor in production
→ `docs/OPERATIONS.md` → Database queries → Check `pipeline_logs` table

### Deploy to production
→ `docs/DEPLOYMENT.md` → Configure CI/CD → Push to main branch

---

## Key Design Patterns

### Fallback Chain
```
Primary (fast, expensive)
  ↓ (failure)
Fallback 1 (slower, cheaper)
  ↓ (failure)
Fallback 2 (slow, free)
  ↓ (failure)
Fallback 3 (cached)
```
Examples: Fetchers (NewsAPI → RSS → GDELT), LLM (OpenAI → Groq)

### Retry with Exponential Backoff
```
Attempt 1: immediate
Attempt 2: wait 1s
Attempt 3: wait 2s
Attempt 4: wait 4s (max 60s)
```

### Circuit Breaker
```
CLOSED (normal operation)
  ↓ (failures > threshold)
OPEN (stop requesting)
  ↓ (timeout elapsed)
HALF_OPEN (test recovery)
  ↓ (success)
CLOSED (back to normal)
```

### Consensus Memory
```
Start cycle: Load from consensus.md
During cycle: Update metrics
End cycle: Save to consensus.md
Crash: Recover from last known state
```

---

## File Size Reference

| Component | Files | LOC | Size |
|-----------|-------|-----|------|
| Core daemon | 1 | 400 | 15 KB |
| Fetchers | 4 | 600 | 22 KB |
| Processing | 5 | 800 | 28 KB |
| LLM layer | 2 | 500 | 20 KB |
| Database | 2 | 400 | 15 KB |
| Failure handling | 3 | 600 | 22 KB |
| Website | 10+ | 2000 | 70 KB |
| Documentation | 6 | 2500 | 150 KB |
| **Total** | **~60** | **10,000+** | **~400 KB** |

---

## Dependencies Summary

### Python (60+ packages)
- Core: pydantic, dotenv, requests, gitpython
- LLM: openai, groq
- Data: pandas, numpy, scikit-learn
- Database: supabase, psycopg2, sqlalchemy
- Dedup: datasketch
- NLP: sentence-transformers, nltk
- Web: beautifulsoup4, feedparser
- Testing: pytest, faker

### Node.js (15+ packages)
- Next.js 14, React 18
- TailwindCSS, PostCSS
- Supabase JS client
- TypeScript

---

## Getting Help

1. **Read the docs**: `docs/` folder has all answers
2. **Check logs**: `daemon.log` and database `pipeline_logs` table
3. **Review code**: Well-commented and modular
4. **Ask questions**: GitHub Issues
5. **Join community**: Discord (TBD)

---

**Happy hacking! 🚀**

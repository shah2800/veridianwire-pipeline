# Autonomous News System - Architecture

## System Overview

```
News Sources (100+)
    |
    +-- NewsAPI.org (official API)
    +-- RSS Feeds (BBC, Reuters, TechCrunch)
    +-- GDELT Project (global events)
    +-- Discovered APIs (reverse-engineered)
    |
    v
[Fetch Manager] - Parallel fetching with fallback chain
    |
    v
[Database] - Store raw_news
    |
    v
[Filter Agent] - MinHash deduplication
    |              + Embeddings clustering
    |              + Quality scoring
    |
    v
[Write Agent] - LLM rewriting
    |             + OpenAI gpt-4o-mini (primary)
    |             + Groq Llama (fallback)
    |
    v
[SEO Agent] - Metadata generation
    |           + Keywords
    |           + Meta descriptions
    |           + Open Graph tags
    |
    v
[Fact-Check Agent] - SerpAPI cross-reference
    |                  + Verify claims
    |                  + Confidence scoring
    |
    v
[Publish Agent] - Git + Vercel deploy
    |              + Create markdown files
    |              + Commit to GitHub
    |              + Deploy to Vercel
    |
    v
[Website] - Next.js frontend
    |
    v
[User Sees]: Auto-generated news articles, SEO-optimized, fact-checked
```

## Data Flow

1. **Fetch** (10 min interval)
   - Pull from 10+ news sources
   - Store raw content in Supabase
   - Time: ~45 seconds

2. **Filter** (sequential)
   - Deduplicate using MinHash
   - Score quality/confidence
   - Keep top 50%
   - Time: ~30 seconds

3. **Process** (sequential)
   - Rewrite for SEO using LLM
   - Generate metadata
   - Fact-check key claims
   - Time: ~2-5 minutes (LLM cost)

4. **Publish** (sequential)
   - Create markdown files
   - Commit to GitHub
   - Deploy to Vercel
   - Submit to Google Search Console
   - Time: ~15 seconds

Total cycle: ~5-10 minutes

## Scaling

**Parallel Fetching**: Fetch from multiple sources simultaneously
**Worker Pool**: 4 parallel LLM workers for rewriting
**Queue System**: Redis + BullMQ for job queue
**Backpressure**: Stop processing if queue > 100 articles

## Reliability

**Fallback Chain**:
```
NewsAPI.org (primary)
    |
    +--> RSS feeds (backup)
    |
    +--> GDELT (last resort)
    |
    +--> Cached articles (emergency)
```

**Circuit Breaker**:
- If API fails 3x in a row, skip for 1 hour
- Gradually retry with exponential backoff
- Alert after 10 failures

**Error Handling**:
- Transient errors: Retry with backoff
- Permanent errors: Skip article, log, continue
- Critical errors: Stop, alert, manual intervention

## Monitoring

**Pipeline Logs**:
- Every stage logged to database
- Alert if any stage has >10% failure rate
- Alert if cycle takes >15 minutes

**Cost Tracking**:
- Monitor OpenAI API usage
- Alert if monthly cost >$50

**Health Checks**:
- Database connectivity
- API key validity
- Disk space (for logs, content)

## Security

- No API keys in logs
- All HTTPS for external APIs
- Database credentials in environment
- Rate limiting on all APIs
- Input validation on all user data

# Agent Instructions for Autonomous News System

This file defines how agents should behave in the autonomous news system.

## Agent Roles

### DataAgent (CEO)
- Responsibility: Fetch news from all sources
- Success criteria: 50+ unique articles per cycle
- Fallback: RSS if NewsAPI fails, cached data if both fail

### FilterAgent (DevOps)
- Responsibility: Deduplicate and score articles
- Success criteria: 80% of fetched articles retained
- Fallback: Skip low-confidence articles instead of publishing

### WriteAgent (CTO)
- Responsibility: Rewrite articles for SEO
- Success criteria: Rewrite 90%+ of filtered articles
- Fallback: Use Groq if OpenAI fails, use original if both fail

### SEOAgent (Marketing)
- Responsibility: Generate SEO metadata
- Success criteria: All published articles have metadata
- Fallback: Generate basic metadata if LLM fails

### PublishAgent (DevOps)
- Responsibility: Commit and deploy to Vercel
- Success criteria: 100% of articles reach production
- Fallback: Queue articles, retry on next cycle

## Error Handling

- Transient errors (network, timeout): Retry with exponential backoff
- Permanent errors (auth, missing data): Skip and log
- Critical errors (database down): Stop and alert

## Monitoring

- Log all pipeline stages to database
- Alert if any stage has >10% failure rate
- Alert if cycle takes >15 minutes
- Alert if no articles published in 24 hours

## Security

- Never log API keys or secrets
- Validate all external input
- Use HTTPS only for external APIs
- Rotate API keys monthly

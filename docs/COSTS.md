# Cost Breakdown - Autonomous News System

## Monthly Operating Costs (Production)

### AI Models
- **OpenAI gpt-4o-mini**: $0.15 per 1M input tokens, $0.60 per 1M output tokens
  - Average: 300 tokens per article × 1000 articles/month = 300k tokens
  - Cost: ~$5-10/month
  - **Budget**: $20/month (safety margin)

- **Groq Llama (Fallback)**: FREE
  - Used only when OpenAI fails
  - No cost
  - **Budget**: $0

### News APIs
- **NewsAPI.org**: 
  - Free tier: 500 requests/month
  - We use ~150 requests/month
  - Cost: **$0** (free tier sufficient)

- **SerpAPI (Fact-checking)**:
  - $0.005 per search
  - We fact-check ~100 articles/month = 100 searches
  - Cost: **$0.50/month**

### Database
- **Supabase (PostgreSQL)**:
  - Free tier: 500MB database, 1GB bandwidth
  - We store ~50MB/month of articles
  - Cost: **$0** (free tier sufficient)
  - Paid tier (if needed): $25/month for 8GB

### Hosting
- **Vercel (Next.js website)**:
  - Free tier: 100GB bandwidth, unlimited functions
  - Our traffic: ~10GB/month (low traffic)
  - Cost: **$0** (free tier sufficient)
  - Paid tier (if needed): $20/month per deployment

- **Redis (Queue system)**:
  - If self-hosted: $0
  - If using Redis Cloud (small): $5-10/month
  - We use self-hosted (free)
  - Cost: **$0**

### Domain & SSL
- **.com Domain**: $10-15/year = ~$1/month
- **SSL Certificate**: FREE (Vercel provides)
- Cost: **$1/month**

### Optional: Monitoring
- **Datadog**: $15+/month (optional)
- **Grafana Cloud**: $0-20/month (optional)
- **New Relic**: $0-50/month (optional)
- Cost: **$0-20/month** (optional)

## Total Monthly Cost

```
OpenAI:           $10
NewsAPI:          $0
SerpAPI:          $0.50
Supabase:         $0
Vercel:           $0
Redis:            $0
Domain:           $1
Monitoring:       $0 (optional)
─────────────────
TOTAL:            $11.50/month
```

**Range: $10-15/month** (without monitoring)
**Range: $25-35/month** (with monitoring)

## Cost Optimization

### 1. Use Groq for Drafts
- Use Groq (free) to generate article drafts
- Use OpenAI (paid) only for final version
- Saves: 50% of LLM costs

### 2. Cache Embeddings
- Cache article embeddings for 7 days
- Reuse instead of regenerating
- Saves: 30-50% of embedding costs

### 3. Batch Processing
- Process articles in batches (10 at a time)
- Batch APIs offer 50% discount
- Saves: 20-30% of API costs

### 4. Reduce Article Volume
- Instead of 1000 articles/month
- Publish only top 500 (by quality)
- Saves: 50% of LLM costs

### 5. Use Cheaper Models
- Replace gpt-4o-mini with gpt-3.5-turbo
- Cost: $0.002/$0.002 per 1M tokens (vs $0.15/$0.60)
- Saves: 90% of LLM costs (but lower quality)

## Revenue Potential

### Ad Revenue
- Google AdSense: $1-5 per 1000 page views
- Target: 100k page views/month = $100-500/month
- Profit: $85-490/month

### Affiliate Links
- Amazon Associates: 4-10% commission
- Target: 10 click-through sales/month = $50-200/month
- Profit: $50-200/month

### Premium Content
- Premium newsletters: $5-20/month per subscriber
- Target: 100 subscribers = $500-2000/month
- Profit: $500-2000/month

### Sponsorships
- Article sponsorships: $50-200 per article
- Target: 5 sponsor articles/month = $250-1000/month
- Profit: $250-1000/month

### Total Revenue Potential: $1000-3700/month

**Profit: $965-3690/month** (after $11.50 costs)

## Scaling Costs

| Articles/Month | OpenAI Cost | Total Cost | Revenue (100k views/m) | Profit |
|---|---|---|---|---|
| 500 | $3 | $15 | $100-500 | $85-485 |
| 1000 | $7 | $19 | $200-1000 | $181-981 |
| 5000 | $35 | $47 | $1000-5000 | $953-4953 |
| 10000 | $70 | $82 | $2000-10000 | $1918-9918 |

## Recommendation

1. Start with 1000 articles/month (~$20 cost)
2. Monitor traffic and profitability
3. Scale to 5000+ articles/month at $10k+ revenue
4. Use Groq + OpenAI hybrid to reduce costs
5. Eventually self-host everything to cut costs to $5/month

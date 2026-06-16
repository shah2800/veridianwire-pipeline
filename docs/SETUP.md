# Setup Guide - Autonomous News System

## Step-by-Step Setup (10 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/your-username/autonomous-news-business
cd autonomous-news-business
```

### 2. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
npm install
cd website && npm install && cd ..
```

### 3. Create Environment File

```bash
cp .env.example .env
```

### 4. Get API Keys

#### OpenAI (Free $5 credit)
1. Go to https://platform.openai.com
2. Sign up / log in
3. Create API key in Settings > API keys
4. Add to .env: `OPENAI_API_KEY=sk-...`

#### Groq (Free)
1. Go to https://console.groq.com
2. Sign up
3. Get API key
4. Add to .env: `GROQ_API_KEY=...`

#### NewsAPI (Free tier)
1. Go to https://newsapi.org
2. Sign up
3. Get API key
4. Add to .env: `NEWSAPI_API_KEY=...`

#### Supabase (Free tier)
1. Go to https://supabase.com
2. Sign up
3. Create new project
4. Copy URL and service key
5. Add to .env:
   - `SUPABASE_URL=https://...supabase.co`
   - `SUPABASE_SERVICE_KEY=eyJ...`

#### Vercel (Free)
1. Go to https://vercel.com
2. Sign up with GitHub
3. Create token in Settings > Tokens
4. Add to .env: `VERCEL_TOKEN=...`

### 5. Initialize Database

```bash
# Create tables in Supabase
python3 scripts/seed_data.py
```

### 6. Test Setup

```bash
# Test database connection
python3 -c "from db.supabase_client import SupabaseClient; db = SupabaseClient(); print(db.health_check())"

# Should print: True
```

### 7. Deploy Website

```bash
bash scripts/deploy.sh
```

This will:
- Build Next.js website
- Deploy to Vercel
- Set up domain

### 8. Start Daemon

```bash
# In one terminal
python daemon.py

# In another terminal
cd website && npm run dev
```

### 9. Check Logs

```bash
tail -f logs/daemon.log
```

You should see:
```
Starting pipeline cycle...
Fetched 50 articles
Filtered to 25 unique articles
Published 5 articles
```

### 10. Verify It Works

```bash
# Check website
curl http://localhost:3000

# Check database has articles
python3 << 'EOF'
from db.supabase_client import SupabaseClient
db = SupabaseClient()
articles = db.get_raw_news(limit=5)
print(f"Found {len(articles)} articles")
for a in articles[:2]:
    print(f"  - {a['title']}")
EOF
```

## Next Steps

- Set up Cloudflare DNS (optional, for custom domain)
- Set up Google Search Console (for SEO tracking)
- Set up Discord alerts (for monitoring)
- Review consensus.md and ARCHITECTURE.md

## Troubleshooting

### "ModuleNotFoundError: No module named 'supabase'"

```bash
pip install supabase
```

### "SUPABASE_URL not found"

Make sure .env file exists and has SUPABASE_URL=...

### "API rate limit exceeded"

Add delays in fetchers/fetch_manager.py or upgrade API plan

### "Daemon stops immediately"

Check logs/daemon.log for error details

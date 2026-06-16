# FREE Setup Guide - No Credit Card Required!

**You can run this entire system completely FREE!**

Here's how to get all the API keys you need without paying a single dollar.

---

## 🟢 REQUIRED Keys (All FREE)

### 1. GROQ API Key (FREE - Unlimited)

**Why:** Free LLM for article rewriting
**Speed:** Actually FASTER than OpenAI
**Cost:** $0 forever

**Get it:**
1. Go to: https://console.groq.com/keys
2. Click "Create API Key"
3. Copy the key (starts with `gsk-`)
4. Paste in `.env`: `GROQ_API_KEY=gsk-...`

**That's it!** No credit card needed. Groq is completely free.

---

### 2. NewsAPI Key (FREE - 500 requests/month)

**Why:** Fetches news from 10,000+ sources
**Cost:** $0 forever (free tier)

**Get it:**
1. Go to: https://newsapi.org/register
2. Sign up with email
3. Copy your API key
4. Paste in `.env`: `NEWSAPI_API_KEY=...`

---

### 3. Supabase (FREE - 500MB database)

**Why:** Database for articles + logs
**Cost:** $0 forever (free tier)

**Get it:**
1. Go to: https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub/Google
4. Create new project (free tier)
5. Go to Settings > API > Copy:
   - `Project URL` → `SUPABASE_URL`
   - `Service Key` (under "service_role") → `SUPABASE_SERVICE_KEY`
6. Paste in `.env`

---

## 🔵 OPTIONAL Keys (Enhanced Features)

### OpenAI Key (OPTIONAL - Paid if you use it)

**Why:** Better article rewriting (optional fallback)
**Cost:** Pay-as-you-go (only if you use it)

**Get it (if interested):**
1. Go to: https://platform.openai.com/api-keys
2. You get **$5 free credit** on signup
3. Can process ~1000 articles with $5
4. Paste in `.env`: `OPENAI_API_KEY=sk-...`

**But:** You DON'T need this! Groq is free and works fine.

---

### Other Optional Keys (For Features, Not Required)

| Key | Purpose | Cost | Required? |
|-----|---------|------|-----------|
| NEWSAPI_API_KEY | Trending news | $0 (free) | ✅ YES |
| SUPABASE_URL | Database | $0 (free) | ✅ YES |
| SUPABASE_SERVICE_KEY | Database auth | $0 (free) | ✅ YES |
| OPENAI_API_KEY | Better rewrites | $ (optional) | ❌ NO |
| VERCEL_TOKEN | Deploy website | $0 (free) | ❌ NO |
| DISCORD_WEBHOOK | Error alerts | $0 (free) | ❌ NO |

---

## ✅ Minimal .env (Bare Minimum - Works!)

```bash
# Copy this into your .env file - that's ALL you need!

# GROQ (free)
GROQ_API_KEY=gsk-your-key-from-https://console.groq.com/keys

# NewsAPI (free)
NEWSAPI_API_KEY=your-key-from-https://newsapi.org/register

# Supabase (free)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-from-https://supabase.com

# System
DAEMON_INTERVAL_MINUTES=10
```

That's it! With just these 4 variables, the system will:
- ✅ Fetch articles from 10,000+ sources
- ✅ Deduplicate and filter articles
- ✅ Rewrite for SEO (FREE via Groq)
- ✅ Store everything in database
- ✅ Run 24/7

---

## 🚀 Quick Free Setup (5 minutes)

```powershell
# 1. Get Groq key (1 min)
# Go to https://console.groq.com/keys → Create Key

# 2. Get NewsAPI key (1 min)
# Go to https://newsapi.org/register → Get key

# 3. Create Supabase project (2 min)
# Go to https://supabase.com → Create project → Copy keys

# 4. Update .env (1 min)
# Edit .env file with the 4 keys above

# 5. Start daemon (done!)
python start_daemon.py
```

---

## 💰 Total Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| **Groq** (LLM) | $0 | Free forever |
| **NewsAPI** | $0 | Free tier: 500 req/month |
| **Supabase** | $0 | Free tier: 500MB database |
| **Vercel** (optional) | $0 | Free tier for hosting |
| **Domain** (optional) | ~$10/year | Not needed for local use |
| **TOTAL** | **$0** | Fully free! |

---

## ✨ What You Get (Completely FREE)

- ✅ AI news fetching from 10,000+ sources
- ✅ AI article rewriting (via free Groq)
- ✅ Automatic deduplication
- ✅ 24/7 autonomous operation
- ✅ Website to display articles
- ✅ Database for storage
- ✅ Full SEO optimization
- ✅ Error logging and monitoring

---

## 🎯 No Credit Card. No Limits. Completely Free.

This system runs entirely on free tiers. You can run a full news business for $0/month if you stay within free tier limits.

---

## 🆘 Troubleshooting

**"GROQ_API_KEY not set"**
- Get key from https://console.groq.com/keys
- Copy the `gsk-...` key to .env

**"NEWSAPI_API_KEY not set"**
- Sign up at https://newsapi.org/register
- Copy your API key to .env

**"Supabase connection failed"**
- Make sure you:
  1. Created a Supabase project
  2. Copied the Project URL (not just the host)
  3. Copied the Service Key (NOT the anon key)
  4. Pasted both into .env

---

## ✅ Ready to Start?

1. Update your `.env` file with the 4 FREE keys
2. Run: `python start_daemon.py`
3. Open: `http://localhost:3000`
4. Watch articles get published automatically!

**That's it. You're running an AI news business. For free.**

---

If you have any issues, check the logs:
```powershell
Get-Content logs/daemon.log -Tail 50
```

Enjoy! 🚀

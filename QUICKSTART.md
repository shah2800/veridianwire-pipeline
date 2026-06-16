# QUICK START - Get Running in 30 Minutes

## Step 1: Download API Keys (10 minutes)

1. OpenAI: https://platform.openai.com/api-keys
   - Copy your API key

2. Groq: https://console.groq.com/keys
   - Copy your API key

3. NewsAPI: https://newsapi.org/register
   - Copy your API key

4. Supabase: https://supabase.com
   - Create new project
   - Copy Project URL from Settings > API
   - Copy Service Key from Settings > API

5. Vercel: https://vercel.com/account/tokens
   - Create new token
   - Copy token

## Step 2: Update .env (2 minutes)

```bash
cp .env.example .env
```

Edit .env and add your API keys:
```
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk-...
NEWSAPI_API_KEY=...
SUPABASE_URL=https://....supabase.co
SUPABASE_SERVICE_KEY=eyJ...
VERCEL_TOKEN=...
```

## Step 3: Install Dependencies (5 minutes)

```bash
pip install -r requirements.txt
npm install
```

## Step 4: Start the System (2 minutes)

Terminal 1 - Start daemon:
```bash
python daemon.py
```

Terminal 2 - Start website:
```bash
cd website && npm run dev
```

## Step 5: Test It (5 minutes)

Website: http://localhost:3000
Daemon logs: tail logs/daemon.log

You should see:
```
Starting pipeline cycle...
Fetched 50 articles
Filtered to 25 unique articles
Published 5 articles
```

## DONE! 

Your autonomous news system is now running 24/7.

Next:
- Monitor logs: tail -f logs/daemon.log
- Check dashboard: http://localhost:3000
- Update prompts: Edit PROMPT.md
- Add more sources: Edit fetchers/

For help:
- docs/SETUP.md - Detailed setup
- docs/ARCHITECTURE.md - How it works
- docs/TROUBLESHOOTING.md - Common issues

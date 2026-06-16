# Windows Quick Start Guide

This guide will get your autonomous news system running on Windows in 30 minutes.

## Prerequisites

- Windows 10 or later
- Python 3.11+ (download from https://www.python.org/downloads/)
- Node.js 18+ (download from https://nodejs.org/)
- Internet connection

## Step 1: Run Windows Setup Script (5 minutes)

Open PowerShell in this directory and run:

```powershell
.\WINDOWS_SETUP.bat
```

This will automatically:
- ✅ Check Python installation
- ✅ Install all Python packages
- ✅ Create .env file
- ✅ Install Node.js packages

## Step 2: Add Your API Keys (5 minutes)

Open `.env` file in this directory with Notepad:

```powershell
notepad .env
```

Add these API keys (get them from the links below):

```
OPENAI_API_KEY=sk-your-key-here
GROQ_API_KEY=gsk-your-key-here
NEWSAPI_API_KEY=your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-here
```

### Where to get API keys:

1. **OpenAI** (for GPT-4o-mini):
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key to .env

2. **Groq** (free LLM fallback):
   - Go to: https://console.groq.com/keys
   - Click "Create API Key"
   - Copy to .env

3. **NewsAPI** (news sources):
   - Go to: https://newsapi.org/register
   - Sign up (free tier is fine)
   - Copy API key to .env

4. **Supabase** (database):
   - Go to: https://supabase.com
   - Create new project (free tier)
   - Go to Settings > API
   - Copy "Project URL" and "Service Key" to .env

Save the file (Ctrl+S) and close Notepad.

## Step 3: Start the Daemon (2 minutes)

Open a PowerShell window and run:

```powershell
cd "D:\my ai projects\completly auto ai which upload news and gethere news"
python start_daemon.py
```

You should see:
```
============================================================
Autonomous News Business Daemon - Pre-flight Check
============================================================
[INFO] Checking required files...
[INFO] Files OK
[INFO] Checking environment variables...
[INFO] Environment variables OK
[INFO] Checking Python imports...
[INFO] All Python imports OK
============================================================
[INFO] All checks passed! Starting daemon...
============================================================
[INFO] Starting pipeline cycle...
[INFO] Fetched XX articles
[INFO] Filtered to XX unique articles
[INFO] Published X articles
```

**The daemon is now running!** It will fetch, process, and publish articles every 10 minutes.

## Step 4: Start Website (in new terminal)

Open another PowerShell window and run:

```powershell
cd "D:\my ai projects\completly auto ai which upload news and gethere news\website"
npm run dev
```

You should see:
```
> autonomous-news-business@1.0.0 dev
> next dev

  ▲ Next.js 14.0.0
  - ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

## Step 5: Check It Works

Open your browser and go to:

```
http://localhost:3000
```

You should see the homepage. The daemon is fetching and publishing articles in the background.

## Checking Logs

See what the daemon is doing:

```powershell
Get-Content logs/daemon.log -Tail 50
```

Or watch in real-time:

```powershell
Get-Content logs/daemon.log -Tail 50 -Wait
```

## Stop the System

**To stop the daemon:** Press Ctrl+C in the terminal running `python start_daemon.py`

**To stop the website:** Press Ctrl+C in the terminal running `npm run dev`

## Troubleshooting

### "Python not found"
Install Python from https://www.python.org/downloads/
Make sure to check "Add Python to PATH"

### "npm not found"
Install Node.js from https://nodejs.org/

### "Missing environment variables"
Edit .env and make sure all 5 API keys are filled in

### "Module not found" errors
Run: `pip install -r requirements.txt --user`

### "Next command not found"
Run: `cd website && npm install`

## What Happens Next

1. **Every 10 minutes:** Daemon fetches news from 10+ sources
2. **Filters articles:** Removes duplicates, low-quality content
3. **Rewrites content:** Uses AI to optimize for SEO
4. **Publishes to website:** Creates new markdown files
5. **Updates database:** Stores everything in Supabase

Check the logs to see progress:
```powershell
Get-Content logs/daemon.log -Tail 50
```

## Next Steps

Once it's running:

1. **Monitor logs:** Watch `logs/daemon.log` for activity
2. **Deploy website:** Push to GitHub and deploy on Vercel
3. **Add Google Analytics:** Track traffic
4. **Set up cron jobs:** Keep daemon running 24/7
5. **Add monetization:** Google AdSense, affiliates, sponsorships

## Getting Help

- Check `docs/TROUBLESHOOTING.md` for common issues
- Check `docs/SETUP.md` for detailed setup
- Check `docs/ARCHITECTURE.md` to understand how it works

---

**Everything is ready! Just follow the 5 steps above and you'll have a working autonomous news system.** 🚀

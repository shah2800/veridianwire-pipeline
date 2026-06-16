# Troubleshooting Guide

## Common Issues & Solutions

### Python/Environment Issues

**"ModuleNotFoundError: No module named 'xxx'"**
- Solution: `pip install -r requirements.txt`
- Also check: `python3 --version` (need 3.11+)

**"python: command not found"**
- Use `python3` instead of `python`
- Or add Python to PATH

**"Permission denied: daemon.py"**
```bash
chmod +x daemon.py
python3 daemon.py
```

### Database Issues

**"SUPABASE_URL not found in .env"**
- Solution: Copy .env.example to .env
- Add your Supabase credentials

**"Connection refused localhost:5432"**
- You're using local PostgreSQL (wrong)
- Use Supabase URL instead
- Update DATABASE_URL in .env

**"rel "raw_news" does not exist"**
- Database tables not created
- Solution: `python3 scripts/seed_data.py`

**"Database size exceeds limit"**
- Delete old articles:
```sql
DELETE FROM raw_news WHERE fetched_at < NOW() - INTERVAL '30 days';
```

### API Issues

**"Unauthorized" from OpenAI**
- Check OPENAI_API_KEY is correct
- Verify key has API access (not just web access)
- Check key isn't revoked

**"API rate limit exceeded"**
- NewsAPI: Upgrade plan
- OpenAI: Reduce article volume or spread cycles
- SerpAPI: Reduce fact-checking

**"Connection timeout"**
- Check internet connection
- Try again (might be temporary)
- Add timeout retry logic

### Daemon Issues

**"Daemon stops immediately"**
1. Check logs: `tail logs/daemon.log`
2. Look for error messages
3. Fix the issue (usually missing .env var)
4. Restart: `python3 daemon.py`

**"Daemon running but not publishing articles"**
1. Check if fetching works:
   ```python
   python3 -c "from fetchers.fetch_manager import FetchManager; \
   fm = FetchManager(); print(fm.fetch_all_sources()[:2])"
   ```

2. Check if database works:
   ```python
   from db.supabase_client import SupabaseClient
   db = SupabaseClient()
   print(db.health_check())
   ```

3. Check confidence threshold:
   ```bash
   grep CONFIDENCE_THRESHOLD .env
   ```
   If too high (>0.9), no articles pass filter

**"High memory usage"**
- Daemon might have memory leak
- Solution: Restart daemon daily with cron
  ```bash
  0 2 * * * pkill -f daemon.py; python3 /path/daemon.py
  ```

**"Daemon CPU at 100%"**
- LLM processing is CPU-intensive
- Normal during article rewriting
- If continuous, might be stuck loop
- Check logs for infinite retry

### Website Issues

**"Website won't build"**
```bash
cd website
npm install
npm run build
```

**"Website shows 404 for articles"**
- Articles not generated/committed
- Check if daemon published any articles
- Check Vercel deployment logs

**"Website slow to load**
- Images taking time to load
- Use smaller image sizes
- Enable caching headers
- Check Vercel analytics

### Git/Deployment Issues

**"Git commit fails"**
- Check git is installed: `git --version`
- Check GITHUB_TOKEN is valid
- Check repo exists

**"Vercel deploy fails"**
- Check VERCEL_TOKEN is valid
- Check build command in vercel.json
- Check Node version compatibility

**"Cannot push to GitHub**
- Check SSH keys configured
- Or use HTTPS with token
- Check branch protection rules

### Performance Issues

**"Pipeline takes >15 minutes"**
- LLM rewriting is slow
- Options:
  1. Reduce articles per cycle
  2. Use Groq (faster than OpenAI)
  3. Use cheaper model (gpt-3.5-turbo)
  4. Increase interval between cycles

**"API costs too high"**
- Check article volume
- Use Groq for drafts, OpenAI for final
- Cache embeddings
- Reduce fact-checking

## Debug Mode

Enable debug logging:
```bash
LOG_LEVEL=DEBUG python3 daemon.py
```

This will show:
- All API calls
- All database operations
- All LLM requests
- Helpful for troubleshooting

## Getting Help

1. Check logs: `tail logs/daemon.log`
2. Check consensus.md for recent errors
3. Search GitHub issues
4. Create new issue with:
   - Python version
   - Error message
   - Steps to reproduce
   - Relevant log lines

## Emergency Reset

If everything is broken:

```bash
# Stop daemon
pkill -f daemon.py

# Clear cache
rm -rf .cache/

# Clear logs (keep one backup)
cp logs/daemon.log logs/daemon.log.backup
rm logs/daemon.log

# Restart
python3 daemon.py
```

**WARNING**: This doesn't delete data, just clears temporary files.

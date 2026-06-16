# Operations Runbook

## Daily Tasks

### Morning (8 AM)
1. Check daemon is running
   ```bash
   ps aux | grep daemon.py
   ```

2. Check recent logs
   ```bash
   tail -50 logs/daemon.log | grep -i error
   ```

3. Verify website is up
   ```bash
   curl -I https://your-domain.com
   ```

4. Check database size
   ```sql
   SELECT pg_size_pretty(pg_database_size('postgres'));
   ```

### Throughout Day
- Monitor Discord alerts for errors
- Check article quality in Google Analytics
- Monitor API costs (stay under $50/month)

### Evening (5 PM)
1. Review consensus.md
   - Check articles published today
   - Check error count
   - Update metrics

2. Check API status
   - OpenAI status at https://status.openai.com
   - Supabase status at https://status.supabase.com

## Weekly Tasks

### Monday
1. SEO Performance Review
   ```bash
   python3 scripts/seo_report.py
   ```
   - Check CTR, impressions, average position
   - Find low-ranking articles

2. Prompt Tuning
   - Review failed rewrites
   - Update prompts in PROMPT.md
   - Test with sample articles

3. Source Reputation Updates
   ```bash
   python3 scripts/update_reputation.py
   ```
   - Adjust scoring for unreliable sources
   - Add new sources if needed

### Wednesday
- Check disk usage
  ```bash
  du -sh *
  ```

### Friday
- Backup database
  ```bash
  pg_dump $DATABASE_URL > backup-$(date +%Y%m%d).sql
  ```

## Monthly Tasks

### Cost Audit
```bash
python3 scripts/cost_report.py
```

Review spending:
- OpenAI: Target <$20
- Groq: Should be $0 (free)
- Supabase: Should be $0 (free tier)
- Vercel: Should be $0 (free tier)
- Total: <$50

### Model Version Upgrades
- Check for GPT-4o-mini updates
- Check for Groq Llama updates
- Test with latest versions

### Infrastructure Patching
- Update Python dependencies
  ```bash
  pip install --upgrade -r requirements.txt
  ```
- Update Node packages
  ```bash
  npm update
  ```

### Backup Verification
- Test restore from latest backup
- Verify all articles restored
- Check database integrity

## Incident Response

### Daemon Not Running
1. Check if process exists
   ```bash
   ps aux | grep daemon
   ```

2. Check logs
   ```bash
   tail -100 logs/daemon.log
   ```

3. Restart
   ```bash
   python daemon.py
   ```

### API Rate Limit
1. Check which API is rate-limited
   ```bash
   grep -i "rate limit" logs/daemon.log
   ```

2. Options:
   - Upgrade API plan
   - Reduce fetch frequency (increase DAEMON_INTERVAL_MINUTES)
   - Add delays between requests

### Database Connection Error
1. Check Supabase status
2. Verify SUPABASE_URL and SUPABASE_SERVICE_KEY in .env
3. Check network connectivity
4. Restart daemon

### High API Costs
1. Run cost report
   ```bash
   python3 scripts/cost_report.py
   ```

2. Identify expensive operations:
   - OpenAI rewriting (check token usage)
   - SerpAPI fact-checking (high per-call cost)

3. Optimization:
   - Reduce article volume
   - Implement caching
   - Use cheaper LLM for drafts

## Monitoring Dashboards

### Database Dashboard
```sql
-- Articles published per day
SELECT DATE(published_at) as day, COUNT(*) as count
FROM published_articles
GROUP BY DATE(published_at)
ORDER BY day DESC
LIMIT 30;

-- Average article quality
SELECT AVG(score) as avg_quality
FROM filtered_news;

-- Error rate by stage
SELECT stage, COUNT(*) as count
FROM pipeline_logs
WHERE status = 'failed'
GROUP BY stage;
```

### API Usage
```bash
python3 scripts/cost_report.py
```

### Traffic (Google Analytics)
- Pages per session
- Bounce rate
- Top articles
- Referral sources

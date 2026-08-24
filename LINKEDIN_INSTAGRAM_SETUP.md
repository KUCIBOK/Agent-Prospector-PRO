# LinkedIn + Instagram Setup Guide

## 🔗 Part 1: LinkedIn Curator Monitoring (via Proxycurl)

### What it does:
- Discovers curators, art advisors, gallery directors on LinkedIn
- Monitors their profiles for changes (title, company, endorsements)
- Generates signals when they change roles or move to important institutions

### Setup (5 min):

#### Step 1: Get Proxycurl API Key (Free)
1. Go to https://proxycurl.com
2. Sign up (free account)
3. Get your API key from Dashboard
4. Free tier: 100 API calls/month

#### Step 2: Set Environment Variable
```bash
# Option A: In .env file
echo "PROXYCURL_API_KEY=your_api_key_here" >> .env

# Option B: Set directly in shell
export PROXYCURL_API_KEY=your_api_key_here

# Option C: Docker - add to docker-compose.yml
environment:
  - PROXYCURL_API_KEY=your_api_key_here
```

#### Step 3: Restart Services
```bash
docker-compose restart app worker scheduler
```

#### Step 4: Test
```bash
# Trigger LinkedIn monitoring
curl -X POST http://localhost:8000/api/monitoring/jobs/monitor-linkedin

# Check job status
curl http://localhost:8000/api/monitoring/jobs
```

### What Proxycurl provides:
```json
{
  "name": "Jane Doe",
  "headline": "Head of Contemporary Art at Gallery X",
  "country": "France",
  "city": "Paris",
  "current_company": {
    "name": "Galerie XYZ",
    "followers_count": 5000
  },
  "connections_count": 852,
  "summary": "15+ years curating contemporary African art"
}
```

### Costs:
- **Free tier**: 100 calls/month = ~3 profiles/day monitored
- **Paid**: $50/month = 10K calls/month

---

## 📱 Part 2: Instagram Artist Analysis

### What it does:
- Analyzes artists' Instagram profiles
- Classifies as EMERGING vs ESTABLISHED
- Scores based on:
  - Followers count
  - Engagement rate (likes + comments / followers)
  - Post frequency
  - Bio keywords ("artist", "contemporary", "studio", etc.)
  - Verification status

### Setup Option A: Public Scraping (FREE, Recommended for V1)

#### Step 1: Install instagrapi
```bash
pip install instagrapi

# OR in Docker, add to Dockerfile:
RUN pip install instagrapi>=2.0.0
```

#### Step 2: Restart
```bash
docker-compose restart app worker
```

#### Step 3: Test
```bash
# Trigger Instagram analysis
curl -X POST http://localhost:8000/api/monitoring/jobs/analyze-instagram

# Check results
curl "http://localhost:8000/api/monitoring/signals/recent?days=1"
```

### What you get:
```python
{
  "instagram": "@artist_handle",
  "followers": 15420,
  "engagement_rate": 6.2,  # HIGH = >5% is VERY good
  "maturity_level": "ESTABLISHED",
  "quality_score": 82,
  "post_frequency": "weekly",
  "is_artist": True,
  "bio_keywords": ["contemporary", "painting", "studio"]
}
```

### Setup Option B: Instagram Business API (For scaling)

#### Step 1: Create Instagram Business Account
1. Convert personal Instagram to Business Account
2. Link to Facebook Page
3. Go to https://developers.facebook.com
4. Create app > Instagram API

#### Step 2: Get Access Token
```bash
# Get 60-day token via Graph API Explorer
# Or set up long-lived token (365 days)

# Add to .env
INSTAGRAM_ACCESS_TOKEN=your_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id
```

#### Step 3: In Code
The `instagram_artist_analyzer.py` will automatically use API if token is set.

### Limits:
- **Free scraping (instagrapi)**: Unlimited but slower, Instagram may rate-limit
- **API**: 200 API calls/hour = ~4,800 artists/day

---

## ⏰ Automated Schedule

Once configured, the system runs automatically:

```
3:00 AM - Discover new curators (LinkedIn search)
5:00 AM - Monitor curator changes (LinkedIn monitoring) 🔗
7:00 AM - Analyze all artists (Instagram analysis) 📱
9:00 AM - Send outreach messages
6:00 PM - Update analytics
```

### Manual Triggers:

```bash
# Analyze Instagram artists
curl -X POST http://localhost:8000/api/monitoring/jobs/analyze-instagram

# Monitor LinkedIn curators
curl -X POST http://localhost:8000/api/monitoring/jobs/monitor-linkedin

# View recent signals
curl http://localhost:8000/api/monitoring/signals/recent?limit=20&days=7
```

---

## 📊 What Signals Look Like

### LinkedIn Curator Signal:
```json
{
  "id": 42,
  "prospect_id": 15,
  "signal_type": "CAREER_CHANGE",
  "description": "Title updated: Director of African Contemporary Acquisitions",
  "source_url": "https://linkedin.com/in/jane-doe",
  "signal_date": "2026-08-24T05:15:00",
  "importance": "HIGH",
  "confidence": "HIGH"
}
```

### Instagram Artist Signal:
```json
{
  "id": 43,
  "prospect_id": 78,
  "signal_type": "NEW_PUBLICATION",
  "description": "Instagram: 25000 followers, 8.2% engagement",
  "source_url": "https://instagram.com/artist_name",
  "signal_date": "2026-08-24T07:30:00",
  "importance": "HIGH",
  "confidence": "HIGH"
}
```

---

## 🎯 KPIs to Track

### LinkedIn Curator Metrics:
- Curators discovered / month: target 50+
- Signals detected / week: target 10+
- Upgrade P3→P1 rate: target 20%

### Instagram Artist Metrics:
- Artists analyzed / week: target 100+
- ESTABLISHED found (>10K followers): target 30/week
- Quality score avg: target 65+

---

## ⚠️ Rate Limiting

### Instagram (instagrapi):
- Rate limit: ~1 profile per 2 seconds (respectful)
- Delays built-in, won't get blocked

### LinkedIn (Proxycurl):
- Free: 100/month (use sparingly)
- Pay as you go: $0.01-0.10 per call

---

## 🔐 Environment Variables Summary

```bash
# LinkedIn (Proxycurl)
PROXYCURL_API_KEY=pk_xxx_yyyy

# Instagram (optional - only if using API)
INSTAGRAM_ACCESS_TOKEN=IGQWRf...
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841401234567

# Scheduler enable/disable
SCHEDULER_ENABLED=true
```

---

## ✅ Verification Checklist

- [ ] Proxycurl API key set (or left empty for manual search)
- [ ] instagrapi installed OR Instagram API token set
- [ ] Services restarted: `docker-compose restart app worker scheduler`
- [ ] API test: `curl http://localhost:8000/api/monitoring/jobs/monitor-linkedin`
- [ ] Dashboard shows new signals in stats

---

## 🆘 Troubleshooting

### "PROXYCURL_API_KEY not set"
→ Set it in .env or docker-compose.yml, restart services

### "instagrapi not found"
→ Run: `pip install instagrapi` or add to Dockerfile

### "Instagram rate limited"
→ Normal, system will retry. Wait 1 hour.

### "LinkedIn signals not detected"
→ Proxycurl free tier = 100 calls/month only. Check usage at proxycurl.com

---

## Next Steps

1. **This week**: Set up Proxycurl + instagrapi (both free)
2. **Week 2**: Monitor first signals coming in
3. **Week 3**: Refine scoring based on signals
4. **Week 4+**: Evaluate upgrade to paid plans if needed

Questions? Check the dashboard at http://localhost:3000

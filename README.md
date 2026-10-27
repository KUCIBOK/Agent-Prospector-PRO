# 🎨 Kucibok Prospector V1.1

**Autonomous agent for discovering African artists and sourcing international curators for the art market.**

> Kucibok Prospector is an open-source, self-hosted system that automatically discovers and qualifies:
> - **Artists**: African contemporary artists (emerging & established)
> - **Clients**: International curators, art advisors, galleries interested in African art
> 
> All with zero external paid services — built to run on your own infrastructure with local AI.

---

## 📋 Overview

Kucibok Prospector powers the client and artist discovery pipeline for Kucibok's SaaS platform. It discovers, documents, enriches, scores, and prioritizes both sides of the market:

- **Client Discovery** → finds curators & art advisors → generates outreach messages
- **Artist Discovery** → finds African artists → auto-enrolls them via Instagram

All fully automated, running 24/7 on your infrastructure.

---

## ⚠️ Known limitations

- **Prototype, not production-ready.** `docker-compose.yml` is not in the repository yet, so the Quick Start below cannot be run as written.
- **Deep Source discovery is a placeholder.** `scrape_google_search()` returns no results until a search provider (SearxNG, SerpAPI, ...) is connected.
- **No measured funnel results.** Figures such as reply rates or revenue per batch were hypotheses and have been removed. Do not rely on them.
- **Authentication:** all `/api` routes require an `X-API-Key` header matching the `API_KEY` environment variable. Set it before exposing the service.
- **Secrets:** never commit `.env*` files. Only `.env.example` is tracked.

---

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (≥ 20.10)
- **Python 3.10+** (for local development)
- **Git**

### Installation

1. **Clone & Setup**
   ```bash
   git clone <repo-url>
   cd kucibok-prospector
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Build & Run**
   ```bash
   docker-compose up -d
   ```

3. **Initialize Database**
   ```bash
   docker-compose exec app alembic upgrade head
   ```

4. **Access Dashboard**
   - **API**: http://localhost:8000
   - **Dashboard**: http://localhost:3000
   - **API Docs**: http://localhost:8000/docs

### Development (Local)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Run with uvicorn
uvicorn app.main:app --reload

# In another terminal, run worker
celery -A app.workers.tasks worker --loglevel=info

# In another terminal, run scheduler
python -m app.scheduler.main
```

---

## 📦 Architecture

### Services (Docker Compose)

| Service | Role | Port |
|---------|------|------|
| **app** | FastAPI backend & API | 8000 |
| **worker** | Async job processing (Celery) | — |
| **scheduler** | Scheduled jobs (APScheduler) | — |
| **database** | PostgreSQL | 5432 |
| **redis** | Cache & job queue | 6379 |
| **ai** | Ollama (local LLM) | 11434 |
| **dashboard** | React frontend | 3000 |

### Modules

```
app/
├── api/                    # FastAPI routes
├── models/                 # Database models (SQLModel)
├── schemas/                # Pydantic schemas
├── services/
│   ├── discovery/          # Client & Artist Discovery
│   ├── crawler/            # Web scraping
│   ├── enrichment/         # Data enrichment
│   ├── scoring/            # Fit Score calculation
│   ├── outreach/           # Message generation
│   └── onboarding/         # Artist Instagram onboarding
├── ai/
│   ├── providers/          # AIProvider (Ollama, etc.)
│   └── prompts/            # LLM prompt templates
├── workers/                # Celery tasks
├── scheduler/              # Scheduled jobs
└── main.py                 # FastAPI app entry point
```

---

## 🔧 Configuration

### Environment Variables (`.env`)

Key variables:
- `MODEL_NAME` — Ollama model (default: `llama2`)
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection
- `OLLAMA_HOST` — Ollama service URL
- `INSTAGRAM_ACCESS_TOKEN` — Meta Graph API token (for artist onboarding)

See [.env.example](.env.example) for full list.

### Scheduler (Cron Jobs)

Edit `.env` to configure daily pipeline timing:
```bash
DISCOVERY_SCHEDULE_HOUR=8
CRAWLING_SCHEDULE_HOUR=9
ENRICHMENT_SCHEDULE_HOUR=10
ANALYSIS_SCHEDULE_HOUR=11
SCORING_SCHEDULE_HOUR=12
```

---

## 🎯 Core Pipelines

### Client Discovery (Curators, Art Advisors)

```
DISCOVER → ENRICH → VERIFY → SCORE → CLASSIFY → STORE → PRIORITIZE
           ↓
      OUTREACH ENGINE (message generation)
           ↓
      MANUAL LinkedIn SEND (copy-paste)
```

**Output**: SaaS Fit Score, Confidence, Priority (P1–P4), Reason to Contact, Recommended Angle

### Artist Discovery

```
DISCOVER → ENRICH → VERIFY → SCORE → PREQUALIFY → STORE
           ↓
      ARTIST DATABASE (internal)
           ↓
      INSTAGRAM ONBOARDING (auto-enrollment on first contact)
```

**Output**: Artist Fit Score, Status, Contact info, Portfolio

---

## 📊 Dashboard

The dashboard (React, port 3000) provides:

- **Overview**: counters by type, status, priority
- **Filtered List**: search, sort, export
- **Prospect Detail**: full profile, scores, sources, signals, actions
- **Outreach Queue**: messages ready to send on LinkedIn (manual)
- **Monitoring**: jobs, errors, performance, system health

---

## 🛡️ Safety & Guardrails

### Non-Negotiable Rules (PRD §7)

✅ **ALWAYS**
- Link every important claim to a source URL
- Use `UNKNOWN` for missing data (never invent)
- Respect `robots.txt` and crawl rate limits
- Store all analysis & decisions with audit trail

❌ **NEVER**
- Declare an artist "Verified Kucibok" (human-only)
- Automate LinkedIn DM sending (manual only)
- Send unsolicited Instagram DMs (first contact = artist-initiated)
- Bypass login, CAPTCHA, paywall, or technical protection
- Invent information (emails, galleries, exhibitions, relationships)

---

## 📈 Scoring Models

### Artist Fit Score (/100)

| Component | Points |
|-----------|--------|
| Profile Quality | 20 |
| International Potential | 20 |
| Digital Presence | 15 |
| Commercial Potential | 20 |
| Work Documentation | 15 |
| Kucibok Fit | 10 |

**Classification**: PRIORITY (80–100) → PROMISING (65–79) → WATCHLIST (50–64) → LOW (0–49)

### SaaS Fit Score (/100)

| Component | Points |
|-----------|--------|
| African Sourcing Need | 30 |
| Operational Need | 20 |
| International Activity | 15 |
| Commercial Capacity | 15 |
| Digital Maturity | 10 |
| Intent Signal | 10 |

**Classification**: HOT (80–100) → WARM (65–79) → WATCHLIST (50–64) → LOW (0–49)

---

## 🚢 Deployment

### Docker Compose (Recommended for V1)

```bash
docker-compose up -d
```

For production:
1. Set `DEBUG=false`
2. Configure HTTPS (reverse proxy + SSL cert)
3. Use strong DB & Redis passwords
4. Enable automated backups
5. Monitor logs & system health

### Manual / Kubernetes

Not recommended for V1 — use Docker Compose. Future versions may support Kubernetes if needed.

---

## 📚 Documentation

- **[PRD](PRD.md)** — Product requirements & use cases
- **[TECHSPEC](TECHSPEC.md)** — Technical architecture & stack
- **[LOGIC](LOGIC.md)** — Business logic, scoring, guardrails
- **[API Docs](http://localhost:8000/docs)** — Interactive Swagger docs (when running)

---

## 🔐 Security

- All config in `.env` (never in code)
- Database backups automated & encrypted
- Logs stored locally, audit-trailed
- HTTPS via reverse proxy (Nginx/Caddy)
- No external APIs required (cost control + independence)

---

## 🤝 Contributing

Contributions welcome! Please:
1. Read [PRD.md](PRD.md) & [TECHSPEC.md](TECHSPEC.md) first
2. Create a feature branch
3. Follow the guardrails in [LOGIC.md](LOGIC.md)
4. Add tests
5. Submit a pull request

---

## 📞 Support & Feedback

- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: contact@kucibok.com

---

## 📄 License

GNU Affero General Public License v3.0 (AGPL-3.0)

See [LICENSE](LICENSE) for details.

---

## 🎯 Roadmap

**V1.1** (Current)
- ✅ Client Discovery (Curators, Art Advisors)
- ✅ Artist Discovery & Prequalification
- ✅ Outreach Engine (message generation, manual send)
- ✅ Artist Onboarding via Instagram (auto-enrollment on first contact)

**V2** (Planned)
- Enhanced feedback loop & scoring refinement
- B2B Qualifier agent (deeper qualification)
- Meeting Booker agent (calendar integration)
- Deal Assistant (pipeline tracking)
- Learn from outcomes (non-auto-learning, manual rule updates)

**V3+**
- Predictive scoring (self-learning)
- Advanced segmentation & propensity models
- Multi-channel outreach (email, Twitter, etc.)
- White-label SaaS for other markets

---

**Built with ❤️ for the African art market.**

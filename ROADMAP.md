# Kucibok Prospector — Product Roadmap & Definition of Done

---

## Version 1.1 (Current)

### Overview
V1.1 focuses on **Client Discovery as the primary pipeline** (monetization driver: curators & art advisors), with supporting **Artist Discovery** and an automated **Outreach Engine** for message generation + manual LinkedIn send.

### Scope

#### 1. Core Discovery Pipeline
- ✅ **Client Discovery**: curateurs, art advisors, galleries
- ✅ **Artist Discovery**: African contemporary artists (emerging & established)
- ✅ **Intent Signals**: detection of public events (expositions, calls for entries, participation signals)

#### 2. Data Enrichment & Analysis
- ✅ **Web Crawler**: extract portfolio, exhibitions, representations, social media
- ✅ **AI Extraction**: named entities, professional activities, relationships
- ✅ **Enrichment Module**: fill missing data, source tracking, duplicate detection
- ✅ **Scoring Module**: Artist Fit (/100) + SaaS Fit (/100) + Confidence + Priority

#### 3. Outreach Engine (NEW in V1.1)
- ✅ **Persona Detection**: ART_ADVISOR vs CURATOR
- ✅ **Message Generation**: multiple variants per prospect, no manual approval
- ✅ **Sending Queue**: dashboard display, sorted by priority
- ✅ **Manual Send**: copy-paste via LinkedIn, no automation (zero ban risk)
- ✅ **Tracking**: status (DRAFT → SENT), outcome logging (REPLIED, MEETING, CUSTOMER, LOST, NOT_RELEVANT)

#### 4. Artist Onboarding via Instagram (NEW in V1.1)
- ✅ **Auto Discovery + Scoring**: reuses Artist Discovery module
- ✅ **Profile Pre-fill**: name, country, discipline, portfolio (internal state = IDENTIFIED)
- ✅ **Invitation Generation**: auto message, ready to send
- ✅ **First Contact Lock**: no auto-send until artist initiates contact (clic lien bio, story reply, formulaire)
- ✅ **API Official Instagram**: Graph API Business Messaging only, no scraping
- ✅ **Auto-Enrollment**: post-contact, relance, profile completion, account creation (all automatic, zero human validation)

#### 5. Dashboard
- ✅ Overview / KPI counters
- ✅ Filterable list (search, sort, export CSV/JSON)
- ✅ Detailed prospect view (profile, scores, sources, signals, actions)
- ✅ Outreach queue (messages ready to send on LinkedIn)
- ✅ Monitoring (jobs, errors, performance, system health)

#### 6. Infrastructure & Automation
- ✅ Dockerized (docker-compose)
- ✅ PostgreSQL + Redis + Ollama (local AI)
- ✅ Celery workers (async crawling, enrichment, scoring)
- ✅ Scheduler (daily pipeline, configurable times)
- ✅ Logging & monitoring
- ✅ Backup automation

### Definition of Done (DoD)

#### Code & Quality
- [ ] All modules pass unit tests (≥ 80% code coverage)
- [ ] Integration tests for discovery → crawling → enrichment → scoring pipeline
- [ ] All AI outputs validated against guardrails (no invented data, all sources linked)
- [ ] Linting & formatting (black, isort, ruff pass)
- [ ] Type hints on 100% of public functions
- [ ] Docstrings on all modules & core functions

#### Database & Migrations
- [ ] Schema complete (prospects, sources, signals, scores, messages, artist_contacts, jobs, ai_analyses, job_errors)
- [ ] Alembic migrations ready for V1 → V1.1 upgrade
- [ ] Data integrity constraints (foreign keys, unique indices on sources)
- [ ] Audit trail: every create/update timestamped with source

#### Discovery & Crawling
- [ ] Client Discovery: ≥ 100 qualified prospects/month identified
- [ ] Artist Discovery: ≥ 100 artists/month identified
- [ ] Crawler: respects robots.txt, retry logic (max 3x), timeout handling
- [ ] Deduplication: < 5% false duplicates, > 95% recall

#### AI & Scoring
- [ ] Local Ollama model configured & loaded
- [ ] AIProvider abstraction complete (analyze, extract, classify, summarize)
- [ ] Artist Fit Score: 100% rule-based breakdown + LLM analysis (no LLM-only decisions)
- [ ] SaaS Fit Score: 100% rule-based, no invented data in output
- [ ] Confidence Score: properly calibrated (LOW/MEDIUM/HIGH mapped to data quality)
- [ ] Reason to Contact generated (WHY / WHY NOW / WHAT), all data sourced
- [ ] Recommended Angle picked (SOURCING, LOGISTICS, SOURCING_AND_LOGISTICS, DISCOVERY, INTERNATIONAL_ACCESS)

#### Outreach Engine
- [ ] Persona detection (ART_ADVISOR vs CURATOR) reliable on test set
- [ ] Message generation produces ≥ 2 variants per prospect, aligned with Khalif's validated style
- [ ] No invented details in LOW-confidence messages
- [ ] Messages stored immutably (no retroactive edits)
- [ ] Dashboard queue sorted by Priority (P1 → P4)
- [ ] Manual send flow tested (copy-paste, status tracking)
- [ ] Zero LinkedIn API calls (no account connection attempted)

#### Artist Onboarding
- [ ] Artist Discovery scores candidates
- [ ] Profile pre-fill logic complete (internal IDENTIFIED state)
- [ ] Invitation message generator working
- [ ] Instagram webhook receiver implemented (receives first_contact events)
- [ ] first_contact_initiated_at only set AFTER artist action (clic lien, story reply, formulaire)
- [ ] Auto-send condition: `first_contact_initiated_at IS NOT NULL` + verified before every send
- [ ] Auto-enrollment flow: relance → profile completion → account creation
- [ ] No account/profile created without first contact confirmation

#### Dashboard
- [ ] API endpoints for all CRUD operations (prospects, messages, searches)
- [ ] Authentication on dashboard (username/password, hashed)
- [ ] List view with filters, sort, export (CSV/JSON)
- [ ] Detail view showing full prospect record + all scores + sources + signals
- [ ] Outreach queue view (priority sort, copy-paste ready)
- [ ] Monitoring dashboard (jobs, errors, system health, CPU/RAM/disk)
- [ ] Real-time refresh (WebSocket or polling)

#### Scheduling & Jobs
- [ ] Scheduler runs discovery → crawling → enrichment → analysis → scoring daily (times configurable)
- [ ] Job queue: PENDING → RUNNING → SUCCESS/FAILED (retry max 3x)
- [ ] Error logging: detailed error messages + stack traces in `job_errors` table
- [ ] Graceful shutdown: in-flight jobs resume on restart

#### Security & Backup
- [ ] `.env.example` provided, no secrets in code
- [ ] Passwords hashed (bcrypt or argon2)
- [ ] HTTPS capable (reverse proxy ready for Nginx/Caddy)
- [ ] PostgreSQL backups automated (daily, 30-day retention)
- [ ] Restore tested (backup → truncate → restore → verify)
- [ ] Logs stored locally, audit trail on all data changes

#### Guardrails & Compliance
- [ ] **No invented data**: all important claims linked to sources
- [ ] **No auto-verification**: artist "Verified Kucibok" never set automatically
- [ ] **No LinkedIn automation**: zero session/cookie logic, no LinkedIn API (message generation only)
- [ ] **No unsolicited IG DMs**: all artist contact auto-sends conditioned on `first_contact_initiated_at`
- [ ] **No technical bypasses**: no CAPTCHA solving, login automation, paywall circumvention
- [ ] **Respect robots.txt**: crawler obeys crawl delays

#### Monitoring & KPIs
- [ ] Artists identified: tracked & reported
- [ ] Prospects identified: tracked & reported
- [ ] Prospects with sources: ≥ 90%
- [ ] Prospects valid on manual review: > 70%
- [ ] Duplicate rate: < 5%
- [ ] System availability: > 95%
- [ ] Job success rate: > 90%

#### Documentation
- [ ] PRD.md complete (context, problem, objectives, scope, metrics)
- [ ] TECHSPEC.md complete (architecture, stack, database schema, security)
- [ ] LOGIC.md complete (pipelines, scoring models, AI guardrails, decisions)
- [ ] README.md with quick start, architecture overview, deployment
- [ ] API docstrings (auto-generated Swagger at `/docs`)
- [ ] Deployment guide (Docker Compose, environment setup, backup/restore)
- [ ] Troubleshooting guide (common errors, logs interpretation)

### Success Criteria (MVP)

| Metric | Target |
|--------|--------|
| **Artists discovered / month** | ≥ 100 |
| **Prospects discovered / month** | ≥ 100 |
| **Data completeness (sources)** | > 90% |
| **Human validation (relevance)** | > 70% |
| **Duplicate rate** | < 5% |
| **System uptime** | > 95% |

---

## Version 2.0 (Planned)

### New Capabilities
- **B2B Qualifier Agent**: deeper qualification, company research, contact enrichment
- **Meeting Booker**: calendar integration, scheduling automation
- **Deal Assistant**: pipeline tracking, stage management, forecasting
- **Feedback Loop**: outcome tracking (REPLIED, MEETING, CUSTOMER, LOST) → manual rule refinement (NO auto-learning yet)
- **Extended Outreach**: email, Twitter, cold calling support

### Improvements
- [ ] Enhanced scoring based on feedback (manual updates, no auto-learning)
- [ ] Refined persona detection (product fit mapping)
- [ ] Multi-channel outreach (email templates, Twitter DMs)
- [ ] Advanced filtering & segmentation
- [ ] Performance optimizations

---

## Version 3.0+ (Future)

- Predictive scoring (self-learning models)
- White-label SaaS offering
- Advanced ML-based propensity modeling
- Multi-language support
- Real-time data streaming

---

## Known Limitations (V1.1)

### Intentional
- No auto-learning (feedback → scoring changes manual only)
- No LinkedIn automation (zero ban risk)
- No unsolicited IG DMs (first contact = artist-initiated)
- No official artist verification (human-only)

### Technical Debt (OK for V1)
- Dashboard styling is minimal (functional, not polished)
- No advanced filtering (SQL-based search coming in V2)
- No workflow automation beyond daily pipeline
- No multi-language support

---

## Release Checklist

Before releasing V1.1 to production:

### Testing
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Manual smoke test: discovery → crawling → scoring → outreach on test data
- [ ] Manual test: artist onboarding flow (mock Instagram webhook)
- [ ] Manual test: dashboard (list, filter, export, monitoring)

### Deployment
- [ ] Docker images build without errors
- [ ] docker-compose up -d works end-to-end
- [ ] Database migrations applied successfully
- [ ] All environment variables documented in .env.example
- [ ] Backup & restore tested on production data

### Security
- [ ] No secrets in code or Docker images
- [ ] Passwords changed from defaults
- [ ] HTTPS configured (self-signed or CA cert)
- [ ] Firewall rules in place (postgres not exposed, redis not exposed)

### Monitoring
- [ ] Logging to file & stdout
- [ ] Dashboard monitoring page functional
- [ ] Backup runs automatically & verifies
- [ ] Alerts configured (job failures, high error rates)

### Documentation
- [ ] README.md reviewed & tested
- [ ] TECHSPEC.md deployment section reviewed
- [ ] Troubleshooting guide available
- [ ] Team trained on dashboard usage

### Stakeholder Sign-Off
- [ ] Product: PRD objectives met
- [ ] Engineering: TECHSPEC implemented
- [ ] Ops: backup, monitoring, security checklist passed
- [ ] Khalif (founder): manual outreach queue tested, approval given

---

**Version: 1.1.0**  
**Last Updated: 2024**  
**Next Review: After V1.1 production release**

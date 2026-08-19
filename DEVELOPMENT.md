# 🔧 Development Guide — Kucibok Prospector

> This guide helps you implement the remaining features.

---

## Current Status

✅ **Phase 2 Complete**: Core application layer ready  
⏳ **Phase 3 In Progress**: Discovery engine, crawler, enrichment  
⏳ **Phase 4 Next**: Integration testing, deployment prep

---

## Phase 3: Discovery & Enrichment Services

### Task 1: Implement Discovery Engine (`app/services/discovery.py`)

**Purpose**: Generate search queries for discovering new prospects

**What to implement**:
```python
class DiscoveryEngine:
    def generate_searches(self, target_type: ProspectType) -> List[Search]:
        """
        Generate discovery queries.
        
        For artists: keywords like "African contemporary artist", 
                     by country (Senegal, Nigeria, Kenya, etc.)
        For clients: keywords like "art advisor Africa", "curator contemporary"
        """
        pass
    
    def execute_search(self, search: Search) -> List[dict]:
        """Execute a search query and return results."""
        pass
```

**Data source** (free):
- Google Search (via requests + BeautifulSoup)
- LinkedIn search (public profiles)
- Instagram hashtags + profiles
- Art directories (artfacts.net, saatchiart.com, etc.)

**Store results**: Create `Search` model + `Prospect` records

---

### Task 2: Implement Crawler (`app/services/crawler.py`)

**Purpose**: Download & parse prospect websites/profiles

**What to implement**:
```python
class Crawler:
    def crawl_website(self, url: str) -> CrawlResult:
        """
        Crawl a website.
        
        Extract:
        - About page content
        - Team members
        - Artists represented
        - Exhibitions
        - Contact info
        - Social media links
        """
        pass
    
    def crawl_instagram(self, handle: str) -> InstagramProfile:
        """Get Instagram profile data (public info only)."""
        pass
    
    def crawl_linkedin(self, profile_url: str) -> LinkedInProfile:
        """Get LinkedIn profile data (public info only)."""
        pass
```

**Libraries**:
- `requests` + `BeautifulSoup` for HTML parsing
- `playwright` for JavaScript-heavy sites (optional)
- `instagrapi` for Instagram (read-only, public data)

**Guardrails**:
- Respect `robots.txt`
- Limit to 1 request/sec per domain
- Max 10 retries per URL
- Catch & log all errors

---

### Task 3: Implement Enrichment Service (`app/services/enrichment.py`)

**Purpose**: Fill missing data, normalize fields

**What to implement**:
```python
class Enrichment:
    def enrich_prospect(self, prospect: Prospect) -> Prospect:
        """
        Enrich prospect data:
        - Normalize country names (Senegal → SN)
        - Normalize email format
        - Extract domain from website
        - Deduplicate similar email variations
        - Update status based on data quality
        """
        pass
    
    def detect_signals(self, prospect: Prospect) -> List[Signal]:
        """Detect intent signals from crawled data."""
        pass
```

**Normalizations**:
- Country: `pycountry` for ISO 3166-1 codes
- Email: lowercase, remove whitespace
- URL: standardize (https, trailing slash)
- Name: title case, strip whitespace

---

### Task 4: Implement AI Analysis

**Purpose**: Use Ollama to analyze prospects

**What to implement**:

```python
# In app/services/analysis.py
def analyze_prospect_ai(prospect: Prospect, ai_provider: AIProvider) -> dict:
    """
    Use LLM to:
    1. Assess Africa interest (HIGH/MEDIUM/LOW/UNKNOWN)
    2. Assess international activity
    3. Assess digital maturity
    4. Detect intent signals
    5. Generate reason_to_contact
    """
    
    prompt = f"""Analyze this prospect profile:
    
Name: {prospect.name}
Type: {prospect.type}
Country: {prospect.country}
Website: {prospect.website}
Description: {prospect.description}

Assess:
1. Africa interest (HIGH/MEDIUM/LOW/UNKNOWN)
2. International activity (HIGH/MEDIUM/LOW/UNKNOWN)
3. Digital maturity (HIGH/MEDIUM/LOW/UNKNOWN)

Return JSON with these fields ONLY."""
    
    return ai_provider.analyze({"type": "prospect_analysis", "data": prompt})
```

---

## Phase 4: Integration Testing

### Test the Full Pipeline

```bash
# 1. Start services
make up

# 2. Initialize DB
make migrate

# 3. Create test prospects
python -m tests.manual.create_test_data

# 4. Run discovery
docker-compose exec app celery -A app.workers.tasks call run_discovery

# 5. Check results
curl http://localhost:8000/api/prospects

# 6. Run scoring
docker-compose exec app celery -A app.workers.tasks call run_scoring

# 7. Check messages
curl http://localhost:8000/api/messages/queue/draft
```

---

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/discovery-engine
```

### 2. Implement Feature
```bash
# Edit app/services/discovery.py
# Add tests in tests/test_discovery.py
# Update app/workers/tasks.py if needed
```

### 3. Test Locally
```bash
make test                    # Unit tests
make lint                    # Code quality
make format                  # Auto-format

# Or test in container
docker-compose exec app pytest tests/test_discovery.py -v
```

### 4. Commit & Push
```bash
git add -A
git commit -m "feat: Implement discovery engine

- Generate queries for artists and clients
- Execute searches via Google + LinkedIn
- Create prospects from results
- Store search history for tracking

Implements LOGIC.md section 7 (Discovery)
"
git push origin feature/discovery-engine
```

### 5. Create Pull Request

---

## File Structure for New Features

When adding a new service:

```
app/services/discovery.py
├── DiscoveryEngine class
├── Query model (local, not DB)
├── Search.execute() method
└── Result parsing

tests/test_discovery.py
├── test_generate_searches()
├── test_execute_search()
└── test_result_parsing()

tests/fixtures/
└── mock_search_results.json

app/workers/tasks.py
└── @app.task def run_discovery(self)
```

---

## Testing Checklist

For each new feature:

- [ ] Unit tests pass locally (`make test`)
- [ ] Code quality passes (`make lint`)
- [ ] No invented data (all claims sourced)
- [ ] Errors handled & logged
- [ ] Edge cases covered (empty data, malformed URLs, timeouts)
- [ ] Docstrings complete
- [ ] Type hints on all functions
- [ ] No hardcoded values (use config)

---

## Code Quality Standards

### Style
- Black formatting (`make format`)
- isort imports (`make format`)
- Ruff linting (`make lint`)
- Type hints on all public functions

### Testing
- All public functions tested
- Edge cases covered
- Test names describe what they test
- Use fixtures from `tests/conftest.py`

### Documentation
- Docstrings on all modules & classes
- Comments for complex logic
- Example usage in docstrings

### Security
- No hardcoded secrets
- No eval() or exec()
- SQL injection safe (SQLModel handles this)
- No information leakage in logs

---

## Database Changes

When modifying models:

```bash
# 1. Update model in app/models/
# 2. Create migration
docker-compose exec app alembic revision --autogenerate -m "Add field_name to Prospect"

# 3. Review generated migration
cat migrations/versions/xxx_add_field_name_to_prospect.py

# 4. Apply migration
make migrate

# 5. Commit
git add migrations/versions/xxx_add_field_name_to_prospect.py
git commit -m "db: Add field_name to Prospect model"
```

---

## Performance Considerations

### Crawling
- Use connection pooling
- Cache robots.txt per domain
- Limit concurrent requests (1 per domain)
- Timeout after 30 seconds

### Database
- Index frequently-searched fields (country, type, priority, status)
- Use pagination (default 20 items)
- Avoid N+1 queries (use `.select_in()`)

### AI
- Cache Ollama responses in Redis
- Batch requests when possible
- Max token limit per request

---

## Debugging Tips

### Enable Verbose Logging
```python
# In app/config.py or .env
LOG_LEVEL=DEBUG
```

### Database Inspection
```bash
docker-compose exec database psql -U kucibok -d kucibok_prospector

# List tables
\dt

# Query prospects
SELECT id, name, type, score, priority FROM prospect LIMIT 10;

# Check sources
SELECT prospect_id, url, source_type FROM source LIMIT 5;
```

### Celery Inspection
```bash
# Monitor tasks in real-time
docker-compose exec worker celery -A app.workers.tasks inspect active

# View task history
docker-compose logs worker | grep "Task"
```

### FastAPI Debugging
```bash
# Enable auto-reload in development
make dev  # uvicorn with --reload

# Test endpoint directly
curl -X GET "http://localhost:8000/api/prospects?page=1" -H "accept: application/json"

# View request/response in Swagger
http://localhost:8000/docs
```

---

## Common Patterns

### Adding a New Endpoint

```python
# In app/api/prospects.py (or new file)
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_session
from app.models import Prospect
from app.schemas import ProspectResponse

router = APIRouter()

@router.get("/prospects/by-country/{country}")
def get_prospects_by_country(
    country: str,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
) -> list[ProspectResponse]:
    """Get prospects from a specific country."""
    prospects = session.exec(
        select(Prospect)
        .where(Prospect.country == country)
        .offset((page - 1) * 20)
        .limit(20)
    ).all()
    return [ProspectResponse.model_validate(p) for p in prospects]
```

### Adding a New Task

```python
# In app/workers/tasks.py
@app.task(bind=True, max_retries=3)
def run_custom_task(self):
    """Custom background task."""
    session = SessionLocal()
    job = None
    
    try:
        job = Job(
            job_type=JobType.CUSTOM,
            status=JobStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        session.add(job)
        session.commit()
        session.refresh(job)
        
        logger.info(f"Running custom task (Job #{job.id})...")
        
        # Do work here
        result_count = 0
        
        job.status = JobStatus.SUCCESS
        job.result_count = result_count
        session.add(job)
        session.commit()
        
        return {"status": "SUCCESS", "result_count": result_count}
        
    except Exception as exc:
        logger.error(f"Task failed: {str(exc)}")
        if job:
            job.attempts += 1
            job.status = JobStatus.RETRYING if job.attempts < 3 else JobStatus.FAILED
            job.error_message = str(exc)
            session.add(job)
            session.commit()
        raise self.retry(exc=exc, countdown=60)
        
    finally:
        session.close()
```

---

## Before Pushing to Production

- [ ] All tests pass (`make test-cov` > 80% coverage)
- [ ] No hardcoded secrets in code
- [ ] All environment variables documented in `.env.example`
- [ ] Database backups tested (`make backup` → `make restore`)
- [ ] Logs configured properly
- [ ] Error handling complete
- [ ] Monitoring dashboard working
- [ ] Docker images built & tested
- [ ] All guardrails validated (see PRD §7)

---

## Useful Commands

```bash
# Run everything
make up logs

# Stop everything
make down

# Clean everything
make clean

# Test + lint + format
make test lint format

# Database operations
make migrate
make backup
make restore

# Development loop
make dev &        # Terminal 1: FastAPI
make worker &     # Terminal 2: Celery
make scheduler &  # Terminal 3: Scheduler
# Then make logs in Terminal 4
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLModel Docs**: https://sqlmodel.tiangolo.com/
- **Celery Docs**: https://docs.celeryproject.org/
- **APScheduler Docs**: https://apscheduler.readthedocs.io/
- **Ollama Docs**: https://github.com/ollama/ollama
- **Pydantic Docs**: https://docs.pydantic.dev/

---

## Glossary

| Term | Meaning |
|------|---------|
| **Prospect** | Artist or client (advisor, curator, gallery) being discovered |
| **Source** | URL where data about prospect came from |
| **Signal** | Intent signal (exhibition, call for artists, etc.) |
| **Score** | Fit score (Artist Fit, SaaS Fit, Confidence, Priority) |
| **Message** | LinkedIn outreach message (generated, manually sent) |
| **Worker** | Celery background task |
| **Job** | Tracked execution of a worker task |
| **AIAnalysis** | Raw output from LLM analysis (audit trail) |

---

**Happy coding! 🚀**

Questions? Check the docs or open an issue.

# 🚀 Getting Started with Kucibok Prospector

Welcome! This guide will help you set up Kucibok Prospector locally or in production.

---

## ⚡ Quick Start (Docker Compose)

**Prerequisites**: Docker & Docker Compose

### 1. Clone & Configure

```bash
# Clone the repository
git clone <repo-url>
cd kucibok-prospector

# Copy environment template
cp .env.example .env

# Edit .env with your settings (at minimum: DB password, model name)
# Use your favorite editor:
nano .env
# or
code .env
```

### 2. Start Services

```bash
# Build Docker images
make build

# Start all services
make up

# Watch logs
make logs
```

### 3. Initialize Database

```bash
# Run Alembic migrations
make migrate
```

### 4. Access the Application

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:3000 (coming soon)
- **Monitoring**: http://localhost:8000/health

✅ **You're ready to go!**

---

## 🔧 Local Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 16+
- Redis 7+
- Ollama (for local AI)

### 1. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for web scraping)
playwright install
```

### 2. Setup Database

```bash
# Create database (assumes PostgreSQL is running locally)
createdb kucibok_prospector

# Run migrations
alembic upgrade head
```

### 3. Setup Redis

```bash
# Start Redis (macOS with Homebrew)
brew services start redis

# Or Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### 4. Setup Ollama

```bash
# Download & run Ollama
# https://ollama.ai

# Pull a model (example: llama2)
ollama pull llama2

# Start Ollama server
ollama serve
```

### 5. Create `.env` File

```bash
cp .env.example .env
```

**Edit `.env` with your local settings:**

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/kucibok_prospector

# Redis
REDIS_URL=redis://localhost:6379

# Ollama
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=llama2

# Debug
DEBUG=true
```

### 6. Run Development Server

**Terminal 1 — FastAPI App**:
```bash
make dev
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Celery Worker**:
```bash
make worker
# or
celery -A app.workers.tasks worker --loglevel=info
```

**Terminal 3 — Scheduler**:
```bash
make scheduler
# or
python -m app.scheduler.main
```

✅ API is now running at http://localhost:8000

---

## 📋 Configuration Reference

### Environment Variables

Key variables in `.env`:

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pwd@localhost:5432/kucibok` |
| `REDIS_URL` | Redis connection | `redis://localhost:6379` |
| `OLLAMA_HOST` | Ollama service URL | `http://localhost:11434` |
| `MODEL_NAME` | LLM model name | `llama2` |
| `DEBUG` | Debug mode | `true` or `false` |
| `API_PORT` | API port | `8000` |

See [.env.example](.env.example) for full reference.

### Scheduler Timing

Customize when daily jobs run:

```env
DISCOVERY_SCHEDULE_HOUR=8
CRAWLING_SCHEDULE_HOUR=9
ENRICHMENT_SCHEDULE_HOUR=10
ANALYSIS_SCHEDULE_HOUR=11
SCORING_SCHEDULE_HOUR=12
```

---

## 🧪 Testing

### Unit Tests

```bash
make test
# or
pytest -v
```

### With Coverage

```bash
make test-cov
# Results in htmlcov/index.html
```

### Linting & Formatting

```bash
# Check code quality
make lint

# Auto-format
make format
```

---

## 📚 Project Structure

```
kucibok-prospector/
├── app/                      # Main application
│   ├── api/                  # FastAPI routes
│   ├── models/               # SQLModel database models
│   ├── schemas/              # Pydantic request/response schemas
│   ├── services/             # Business logic
│   │   ├── discovery/        # Client & Artist Discovery
│   │   ├── crawler/          # Web scraping
│   │   ├── enrichment/       # Data enrichment
│   │   ├── scoring/          # Fit Score calculation
│   │   ├── outreach/         # Message generation
│   │   └── onboarding/       # Artist Instagram onboarding
│   ├── ai/                   # LLM integration (Ollama)
│   ├── workers/              # Celery async tasks
│   ├── scheduler/            # Scheduled jobs
│   ├── config.py             # Configuration
│   └── main.py               # FastAPI app entry point
├── dashboard/                # React frontend (coming soon)
├── scripts/                  # Utility scripts (backup, restore, init)
├── tests/                    # Test suite
├── docker-compose.yml        # Docker orchestration
├── Dockerfile                # Docker image definition
├── pyproject.toml            # Python project config
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── README.md                 # Project documentation
├── PRD.md                    # Product requirements
├── TECHSPEC.md               # Technical specification
├── LOGIC.md                  # Business logic & scoring
└── ROADMAP.md                # Development roadmap
```

---

## 🛠️ Useful Commands

### Make Commands (see `Makefile`)

```bash
make help          # Show all available commands
make up            # Start all services
make down          # Stop all services
make logs          # Show logs
make backup        # Backup database
make test          # Run tests
make lint          # Check code quality
make format        # Auto-format code
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec app alembic upgrade head

# Stop services
docker-compose down

# Remove volumes (careful: deletes data)
docker-compose down -v
```

### Database Management

```bash
# Create a new migration
docker-compose exec app alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec app alembic upgrade head

# Rollback
docker-compose exec app alembic downgrade -1

# Backup
bash scripts/backup.sh

# Restore
bash scripts/restore.sh backups/kucibok_backup_20240101_120000.sql.gz
```

---

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs app

# Rebuild images
docker-compose build --no-cache

# Remove and recreate
docker-compose down -v && docker-compose up -d
```

### Database connection error

```bash
# Check if PostgreSQL is running
docker-compose exec database psql -U kucibok -c "SELECT 1"

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Redis connection error

```bash
# Check if Redis is running
docker-compose exec redis redis-cli ping

# Should return: PONG
```

### Ollama/AI service not responding

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Pull the model if needed
ollama pull llama2

# Restart Ollama service
docker-compose restart ai
```

### Migrations fail

```bash
# Check migration history
docker-compose exec app alembic history

# Downgrade to base
docker-compose exec app alembic downgrade base

# Re-apply all
docker-compose exec app alembic upgrade head
```

---

## 📖 Next Steps

1. **Read the documentation**:
   - [README.md](README.md) — Project overview
   - [PRD.md](PRD.md) — Product requirements
   - [TECHSPEC.md](TECHSPEC.md) — Technical architecture
   - [LOGIC.md](LOGIC.md) — Business logic

2. **Explore the API**:
   - Open http://localhost:8000/docs
   - Try the health check: `GET /health`

3. **Start developing**:
   - Create a feature branch: `git checkout -b feature/my-feature`
   - Follow the guardrails in [LOGIC.md](LOGIC.md)
   - Write tests & run linting before committing

4. **Monitor & Maintain**:
   - Check logs regularly: `make logs`
   - Run backups: `make backup`
   - Monitor system health at `/api/monitoring`

---

## 🆘 Getting Help

- **Issues?** Open a GitHub issue
- **Questions?** Use GitHub Discussions
- **Found a bug?** Submit a PR with tests
- **Feedback?** Contact kucibok@example.com

---

## 🎯 Quick Reference

| What | Command |
|------|---------|
| Start services | `make up` |
| Stop services | `make down` |
| View logs | `make logs` |
| Run tests | `make test` |
| Format code | `make format` |
| Backup database | `make backup` |
| Access API | http://localhost:8000 |
| API documentation | http://localhost:8000/docs |

---

**Happy hacking! 🚀**

.PHONY: help build up down logs clean test lint format migrate shell

help:
	@echo "🎨 Kucibok Prospector — Make Commands"
	@echo ""
	@echo "Setup & Deployment:"
	@echo "  make build          Build Docker images"
	@echo "  make up             Start all services (docker-compose up)"
	@echo "  make down           Stop all services"
	@echo "  make logs           Show logs (docker-compose logs -f)"
	@echo "  make clean          Remove containers, volumes, and cache"
	@echo ""
	@echo "Development:"
	@echo "  make dev            Run app locally with uvicorn --reload"
	@echo "  make worker         Run Celery worker"
	@echo "  make scheduler      Run APScheduler"
	@echo "  make shell          Python REPL with app context"
	@echo ""
	@echo "Database:"
	@echo "  make migrate        Run Alembic migrations (docker-compose exec)"
	@echo "  make migrate-fresh  Drop & recreate database"
	@echo "  make backup         Backup PostgreSQL database"
	@echo "  make restore        Restore from backup (prompts for file)"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test           Run pytest"
	@echo "  make test-cov       Run pytest with coverage"
	@echo "  make lint           Run linting (black, isort, ruff, mypy)"
	@echo "  make format         Auto-format with black & isort"
	@echo ""
	@echo "Utils:"
	@echo "  make status         Show service status (docker-compose ps)"
	@echo "  make ps             Alias for status"
	@echo "  make pull           Pull latest Docker images"
	@echo ""

build:
	@echo "🔨 Building Docker images..."
	docker-compose build

up:
	@echo "🚀 Starting all services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "   API: http://localhost:8000"
	@echo "   Dashboard: http://localhost:3000"
	@echo "   API Docs: http://localhost:8000/docs"

down:
	@echo "🛑 Stopping all services..."
	docker-compose down
	@echo "✅ Services stopped!"

logs:
	@echo "📋 Showing logs (Ctrl+C to exit)..."
	docker-compose logs -f

clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
	@echo "✅ Cleaned!"

dev:
	@echo "🔧 Running app locally (uvicorn --reload)..."
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

worker:
	@echo "🔄 Running Celery worker..."
	celery -A app.workers.tasks worker --loglevel=info

scheduler:
	@echo "⏰ Running APScheduler..."
	python -m app.scheduler.main

shell:
	@echo "🐍 Python REPL with app context..."
	python -c "from app.main import app; import IPython; IPython.embed()"

migrate:
	@echo "🗂️  Running Alembic migrations..."
	docker-compose exec app alembic upgrade head
	@echo "✅ Migrations complete!"

migrate-fresh:
	@echo "⚠️  Dropping & recreating database..."
	docker-compose exec app alembic downgrade base
	docker-compose exec app alembic upgrade head
	@echo "✅ Database recreated!"

backup:
	@echo "💾 Backing up database..."
	bash scripts/backup.sh

restore:
	@echo "📂 Restore from backup..."
	@read -p "Backup file path: " file && \
	bash scripts/restore.sh $$file

test:
	@echo "🧪 Running tests..."
	pytest -v

test-cov:
	@echo "📊 Running tests with coverage..."
	pytest --cov=app --cov-report=html --cov-report=term

lint:
	@echo "📝 Linting..."
	black --check app
	isort --check-only app
	ruff check app
	mypy app

format:
	@echo "✨ Auto-formatting..."
	black app
	isort app

status:
	@echo "📊 Service status:"
	docker-compose ps

ps: status

pull:
	@echo "📦 Pulling latest Docker images..."
	docker-compose pull

.DEFAULT_GOAL := help

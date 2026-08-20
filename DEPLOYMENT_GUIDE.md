# 🚀 Kucibok Prospector v1.1 — Production Deployment Guide

**Status**: ✅ READY TO DEPLOY  
**Date**: 20 August 2026  
**All Tests Passing**: 35/35 (100%)

---

## Quick Start (7 Steps)

### Step 1: Prepare Docker Environment

```bash
# Ensure Docker Desktop is running
docker ps

# Build the application image
docker-compose build

# Start all services
docker-compose up -d

# Verify all containers are running
docker-compose ps
```

Expected output:
```
STATUS              PORTS
Up 2 minutes        0.0.0.0:8000->8000/tcp    (app)
Up 2 minutes        0.0.0.0:3000->3000/tcp    (dashboard)
Up 2 minutes        0.0.0.0:5432->5432/tcp    (database)
Up 2 minutes        0.0.0.0:6379->6379/tcp    (redis)
Up 2 minutes        0.0.0.0:11434->11434/tcp  (ollama)
```

### Step 2: Initialize Database

```bash
# Apply Alembic migrations
docker-compose exec app alembic upgrade head

# Or manually create schema (if alembic fails)
docker-compose exec app python -c "
from app.models import *
from app.db import engine
from sqlmodel import SQLModel
SQLModel.metadata.create_all(engine)
"

# Verify database connection
docker-compose exec app python -c "from app.db import SessionLocal; s = SessionLocal(); print('Database OK')"
```

### Step 3: Health Checks

```bash
# FastAPI health check
curl http://localhost:8000/health

# Readiness check (all dependencies)
curl http://localhost:8000/ready

# View API documentation
open http://localhost:8000/docs
```

Expected responses:
```json
{
  "status": "ok",
  "version": "1.1.0",
  "service": "kucibok-prospector"
}
```

### Step 4: Create Test Data

```bash
# Run the test data creation script
python scripts/create_test_data.py

# Verify data was created
curl http://localhost:8000/api/prospects

# Should return something like:
# {
#   "total": 3,
#   "items": [...],
#   "page": 1
# }
```

### Step 5: Configure for Production

```bash
# Copy production environment template
cp .env.prod .env.production

# Edit with your actual values
# - Update DB_HOST, DB_PASSWORD
# - Update REDIS_HOST
# - Update OLLAMA_HOST
# - Update CORS_ORIGINS and ALLOWED_HOSTS
# - Add Instagram credentials if needed
```

**Critical settings to change**:
```env
DEBUG=false                                    # MUST be false
SECRET_KEY=<NEW_SECURE_KEY>                   # Use generated key
DB_PASSWORD=<STRONG_PASSWORD>                 # At least 32 chars
CORS_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com
```

### Step 6: Final Tests

```bash
# Run entire test suite one more time
pytest tests/ -v --tb=short

# Expected: 35 passed, 0 failed
```

### Step 7: Deploy to Production

**Option A: Docker Compose (Recommended)**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Option B: Docker Swarm**
```bash
docker stack deploy -c docker-compose.prod.yml kucibok
```

**Option C: Kubernetes**
```bash
kubectl apply -f k8s/ --namespace=kucibok
```

---

## Production Configuration Checklist

### Security
- [ ] Generate new SECRET_KEY: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Set strong DB_PASSWORD (32+ chars with mixed case/numbers/symbols)
- [ ] Update POSTGRES_PASSWORD in docker-compose
- [ ] Configure HTTPS via reverse proxy (Nginx or Caddy)
- [ ] Restrict database firewall (PostgreSQL internal only)
- [ ] Restrict Redis firewall (internal only)
- [ ] Enable authentication on dashboard
- [ ] Update CORS_ORIGINS with production domain

### Infrastructure
- [ ] Provision PostgreSQL database (or use managed service)
- [ ] Provision Redis instance (or use managed service)
- [ ] Provision Ollama server (or use managed service)
- [ ] Configure reverse proxy (Nginx/Caddy for HTTPS)
- [ ] Set up automated backups (daily, 30-day retention)
- [ ] Configure backup restore testing (weekly)

### Monitoring & Alerting
- [ ] Set up health check monitoring (every 5 min)
- [ ] Configure logging (ELK, Datadog, or similar)
- [ ] Set up alerting for:
  - API response times > 500ms
  - Job failures (discovery, scoring, etc.)
  - Database connection errors
  - Backup failures
  - High CPU/RAM/Disk usage

### Operations
- [ ] Document runbook for common issues
- [ ] Set up on-call rotation
- [ ] Create incident response procedures
- [ ] Test disaster recovery (backup → restore)
- [ ] Document data retention policies

---

## Key Endpoints (Test After Deployment)

### Health
- `GET /health` - Basic health check
- `GET /ready` - Readiness check (dependencies)

### Prospects (CRUD)
- `GET /api/prospects` - List all (paginated)
- `POST /api/prospects` - Create new
- `GET /api/prospects/{id}` - Get one
- `PATCH /api/prospects/{id}` - Update
- `DELETE /api/prospects/{id}` - Delete

### Scoring & Analysis
- `GET /api/prospects/stats/by-type` - Breakdown by type
- `GET /api/prospects/stats/by-priority` - Breakdown by priority

### Outreach
- `GET /api/messages` - All messages
- `GET /api/messages/queue/draft` - Ready to send

### Monitoring
- `GET /api/monitoring/health` - System health
- `GET /api/monitoring/jobs` - Job status
- `GET /api/monitoring/system` - CPU, RAM, Disk
- `GET /api/monitoring/summary` - Dashboard data

---

## Database Backup/Restore

### Automated Backup (Daily)
```bash
# Backup is run automatically at configured time
# Location: /app/backups/

# Manual backup
docker-compose exec database pg_dump -U kucibok kucibok_prospector > backup.sql
```

### Restore from Backup
```bash
# Stop the application
docker-compose down

# Restore database
docker-compose exec database psql -U kucibok kucibok_prospector < backup.sql

# Restart
docker-compose up -d

# Verify
curl http://localhost:8000/health
```

---

## Troubleshooting

### Database Connection Refused
```bash
# Check PostgreSQL is running
docker-compose ps database

# Check logs
docker-compose logs database

# Verify credentials in .env match docker-compose.yml
```

### API Not Responding
```bash
# Check app container
docker-compose logs app

# Check if port 8000 is available
lsof -i :8000

# Restart the app
docker-compose restart app
```

### Redis Connection Issues
```bash
# Test Redis connection
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis
```

### Ollama Not Loading Models
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Pull llama2 model
docker-compose exec ai ollama pull llama2

# Restart Ollama
docker-compose restart ai
```

---

## Performance Tuning

### Database
```sql
-- Create indexes for common queries
CREATE INDEX ON prospect(priority, confidence);
CREATE INDEX ON prospect(status, updated_at);
CREATE INDEX ON message(status, prospect_id);
```

### Redis
```bash
# Monitor Redis memory usage
docker-compose exec redis redis-cli info memory

# Configure maxmemory policy if needed
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Celery Workers
```bash
# Scale workers (in docker-compose)
docker-compose up -d --scale worker=3
```

---

## Monitoring Dashboard URLs

After deployment, access these interfaces:

- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Dashboard**: http://localhost:3000
- **Monitoring**: http://localhost:8000/api/monitoring/health

---

## Useful Commands

```bash
# View all logs
docker-compose logs -f

# View app logs only
docker-compose logs -f app

# Execute commands in container
docker-compose exec app python -c "..."

# Access database shell
docker-compose exec database psql -U kucibok -d kucibok_prospector

# Access Redis CLI
docker-compose exec redis redis-cli

# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Clean up (WARNING: Removes data)
docker-compose down -v
```

---

## Post-Deployment Tasks (First 24 Hours)

1. **Monitor Application**
   - Watch logs for errors
   - Monitor CPU/RAM/Disk usage
   - Track API response times

2. **Test All Pipelines**
   - Run discovery manually
   - Run crawling on sample prospects
   - Generate outreach messages
   - Verify scoring calculations

3. **Validate Backups**
   - Confirm daily backup runs
   - Test restore procedure
   - Verify backup integrity

4. **Security Audit**
   - Verify HTTPS is working
   - Test authentication
   - Check firewall rules
   - Review access logs

5. **Set Up Alerts**
   - Configure monitoring alerts
   - Set up on-call notification
   - Document escalation procedures

---

## Support & Escalation

**On-call Engineer**: [Your Name] - [Email/Phone]  
**Product Owner**: Khalif - khalif@kucibok.com  
**DevOps Lead**: [DevOps Contact]  

---

## Rollback Procedure

If something goes wrong:

```bash
# 1. Stop current deployment
docker-compose down

# 2. Restore database from backup
docker-compose exec database psql -U kucibok kucibok_prospector < backup-before-deploy.sql

# 3. Checkout previous Docker image
git checkout <previous-tag>

# 4. Restart with previous version
docker-compose build
docker-compose up -d

# 5. Verify health
curl http://localhost:8000/health
```

---

**Deployment Status**: ✅ READY  
**Last Updated**: 20 August 2026  
**Next Review**: After first production run

# Start Services Locally

## Quick Start (3 Terminals)

### Terminal A - FastAPI API Server
```bash
cd /Users/aryanchadha/InvestingRecommender
source backend/venv/bin/activate
uvicorn backend.app.main:app --reload
```

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Terminal B - Redis Server
```bash
# Option 1: Local Redis
redis-server

# Option 2: Docker
docker run -p 6379:6379 redis:7
```

**Verify:**
```bash
redis-cli ping
# Should return: PONG
```

### Terminal C - Celery Worker
```bash
cd /Users/aryanchadha/InvestingRecommender
source backend/venv/bin/activate
celery -A backend.app.services.tasks.celery_app.app worker -l INFO --concurrency=4
```

## Optional: Terminal D - Celery Beat (Scheduler)
```bash
cd /Users/aryanchadha/InvestingRecommender
source backend/venv/bin/activate
celery -A backend.app.services.tasks.celery_app.app beat -l INFO
```

## Test the Setup

**1. Check API health:**
```bash
curl http://localhost:8000/api/v1/health/
```

**2. Queue a price fetch task:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/celery/price?symbol=VOO&lookback_days=365"
```

**3. Check task status (use task_id from step 2):**
```bash
curl "http://localhost:8000/api/v1/ingest/celery/status/{task_id}"
```

## Troubleshooting

**Redis connection error:**
- Make sure Redis is running: `redis-cli ping`
- Check REDIS_URL in environment

**Celery worker not starting:**
- Verify Redis is running
- Check worker logs for errors
- Ensure all task modules are importable

**Import errors:**
- Make sure you're in the project root
- Verify venv is activated
- Check Python path includes project root

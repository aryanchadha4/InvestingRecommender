# Local Development Setup

## Quick Start

### 1. Start Redis (Terminal B)

**Option A: Local Redis**
```bash
redis-server
```

**Option B: Docker**
```bash
docker run -d -p 6379:6379 --name redis redis:7
```

**Verify Redis is running:**
```bash
./check_redis.sh
# or
redis-cli ping
```

### 2. Start FastAPI Server (Terminal A)

```bash
cd backend
./run_api.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 3. Start Celery Worker (Terminal C)

```bash
cd backend
./run_celery_worker.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
celery -A app.services.tasks.celery_app.app worker -l INFO --concurrency=4
```

### 4. Start Celery Beat (Terminal D - Optional)

For scheduled tasks (nightly refresh):

```bash
cd backend
./run_celery_beat.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
celery -A app.services.tasks.celery_app.app beat -l INFO
```

## Service Checklist

- [ ] Redis running (port 6379)
- [ ] FastAPI server running (port 8000)
- [ ] Celery worker running
- [ ] Celery Beat running (optional)

## Test Endpoints

**Queue a task:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/celery/price?symbol=VOO&lookback_days=365"
```

**Check task status:**
```bash
curl "http://localhost:8000/api/v1/ingest/celery/status/{task_id}"
```

**Queue orchestrated backfill:**
```bash
curl -X POST "http://localhost:8000/api/v1/ingest/celery/backfill?symbols=VOO&symbols=QQQM&lookback_days=365"
```

## Troubleshooting

**Redis not running:**
```bash
./check_redis.sh
```

**Celery worker not connecting:**
- Check Redis is running
- Verify REDIS_URL in environment

**Tasks not executing:**
- Verify Celery worker is running
- Check worker logs for errors
- Verify task modules are imported correctly

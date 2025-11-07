# Investing Recommender

AI-driven investment recommender FastAPI backend with PostgreSQL, Redis, and Celery.

## Quickstart

```bash
cp .env.example .env
docker compose up --build

# API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Migrations

```bash
cd backend
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Tests

```bash
cd backend
pytest -q
```

## Development

See `backend/README.md` for detailed setup instructions.

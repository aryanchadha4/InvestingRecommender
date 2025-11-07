# Investment Recommender Backend

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
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## Tests

```bash
pytest -q
```

## Features

- FastAPI with async/await support
- PostgreSQL database with SQLAlchemy 2.0
- Redis for caching and task queue
- Celery for background tasks
- Alembic for database migrations
- Pydantic v2 for data validation
- Comprehensive type hints
- Docker and Docker Compose setup
- pytest for testing

## Project Structure

```
backend/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core configuration
│   ├── db/            # Database models and repositories
│   ├── schemas/       # Pydantic schemas
│   └── services/      # Business logic and services
├── alembic/           # Database migrations
├── tests/             # Test suite
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)
- PostgreSQL (if not using Docker)
- Redis (if not using Docker)

### Installation

1. Clone the repository and navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -e ".[dev]"
```

4. Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run database migrations:

First, generate the initial migration:
```bash
cd backend
alembic revision --autogenerate -m "init"
```

Then apply the migration:
```bash
alembic upgrade head
```

Or use the provided script (after starting the database):
```bash
./run_migrations.sh
```

### Running with Docker

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis
- FastAPI application
- Celery worker

The API will be available at `http://localhost:8000`

### Running Locally

1. Start PostgreSQL and Redis (or use Docker Compose for just these services):

```bash
docker-compose up -d db redis
```

2. Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

3. Run Celery worker (in another terminal):

```bash
celery -A app.services.tasks.ingest.celery_app worker --loglevel=info
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
ruff check --fix .
```

### Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:

```bash
alembic upgrade head
```

## License

MIT

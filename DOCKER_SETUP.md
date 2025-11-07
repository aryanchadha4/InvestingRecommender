# Docker Database Setup Guide

## Step 1: Install Docker

### macOS
1. **Download Docker Desktop for Mac:**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Apple Silicon (M1/M2/M3) or Intel
   - Install the .dmg file
   - Launch Docker Desktop from Applications

2. **Verify Installation:**
   ```bash
   docker --version
   docker compose version
   ```

### Alternative: Install via Homebrew
```bash
brew install --cask docker
```

## Step 2: Create Environment File

Create a `.env` file in the project root (`/Users/aryanchadha/InvestingRecommender/.env`):

```bash
# Database
DATABASE_URL=postgresql+psycopg://invest:invest@localhost:5432/investdb

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ENV=dev

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

Or copy from example:
```bash
cp .env.example .env
```

## Step 3: Start the Database

From the project root directory:

```bash
cd /Users/aryanchadha/InvestingRecommender
docker compose up -d db
```

This will:
- Pull the PostgreSQL 16 image (first time only)
- Start the database container
- Create the database `investdb` with user `invest` / password `invest`
- Expose port 5432 for local connections

## Step 4: Verify Database is Running

```bash
docker compose ps db
```

You should see the container status as "Up" or "running".

## Step 5: Run Migrations

Once the database is running:

```bash
cd backend
python3 -m alembic revision --autogenerate -m "init"
python3 -m alembic upgrade head
```

## Useful Commands

**Start database:**
```bash
docker compose up -d db
```

**Stop database:**
```bash
docker compose stop db
```

**View database logs:**
```bash
docker compose logs db
```

**Restart database:**
```bash
docker compose restart db
```

**Remove database (⚠️ deletes all data):**
```bash
docker compose down -v db
```

**Connect to database directly:**
```bash
docker compose exec db psql -U invest -d investdb
```

## Troubleshooting

**Port already in use:**
- If port 5432 is already in use, you can change it in `docker-compose.yml`:
  ```yaml
  ports: ["5433:5432"]  # Change first number to available port
  ```
- Then update `DATABASE_URL` in `.env` to use the new port

**Docker daemon not running:**
- Make sure Docker Desktop is running
- Check: `docker ps` should work without errors

**Database connection refused:**
- Wait a few seconds after starting the container
- Check logs: `docker compose logs db`
- Verify container is running: `docker compose ps`


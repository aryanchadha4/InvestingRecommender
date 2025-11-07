# Quick Start: Database Container

Since Docker Desktop is running but the command line tools aren't in your PATH, here are the easiest ways to start the database:

## Method 1: Docker Desktop Terminal (Easiest)

1. In Docker Desktop, click the **">_ Terminal"** button in the bottom right
2. Run these commands:
   ```bash
   cd /Users/aryanchadha/InvestingRecommender
   docker compose up -d db
   ```
3. Wait a few seconds for the database to start
4. Then run migrations:
   ```bash
   cd backend
   python3 -m alembic revision --autogenerate -m "init"
   python3 -m alembic upgrade head
   ```

## Method 2: Add Docker to PATH

Add this to your `~/.zshrc` file:
```bash
export PATH="/usr/local/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc
```

## Method 3: Use Full Path

If Docker is installed in a non-standard location, you can use the full path:
```bash
/Applications/Docker.app/Contents/Resources/bin/docker compose up -d db
```

## Verify Database is Running

After starting the container, check it's running:
```bash
docker compose ps db
```

You should see the container status as "Up" or "running".

## Then Run Migrations

Once the database is running:
```bash
cd backend
python3 -m alembic revision --autogenerate -m "init"
python3 -m alembic upgrade head
```


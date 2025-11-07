#!/bin/bash
# Script to run Alembic migrations
# Prerequisites:
# 1. Install dependencies: pip install -e ".[dev]" (from project root)
# 2. Start database: docker compose up -d db (from project root)
# 3. Set DATABASE_URL if needed (or use default from .env)

cd "$(dirname "$0")"

echo "Generating initial migration..."
python3 -m alembic revision --autogenerate -m "init"

echo "Applying migrations..."
python3 -m alembic upgrade head

echo "Migrations complete!"


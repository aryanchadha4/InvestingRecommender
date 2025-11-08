#!/bin/bash
# Run Celery worker

cd "$(dirname "$0")/.."
source backend/venv/bin/activate

echo "⚙️  Starting Celery worker..."
echo "   Concurrency: 4"
echo "   Broker: Redis"
echo ""

celery -A backend.app.services.tasks.celery_app.app worker -l INFO --concurrency=4

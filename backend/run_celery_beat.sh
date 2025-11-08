#!/bin/bash
# Run Celery Beat for scheduled tasks

cd "$(dirname "$0")/.."
source backend/venv/bin/activate

echo "🕐 Starting Celery Beat scheduler..."
celery -A backend.app.services.tasks.celery_app.app beat -l INFO

#!/bin/bash
# Run FastAPI server

cd "$(dirname "$0")/.."
source backend/venv/bin/activate

echo "🚀 Starting FastAPI server..."
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

uvicorn backend.app.main:app --reload

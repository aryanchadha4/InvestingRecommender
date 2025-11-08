#!/bin/bash
# Start all services (helper script)

echo "📋 Investment Recommender - Service Status"
echo "=========================================="
echo ""

# Check Redis
echo "1️⃣  Checking Redis..."
if redis-cli ping > /dev/null 2>&1; then
    echo "   ✅ Redis is running"
else
    echo "   ❌ Redis is not running"
    echo "   Start with: redis-server"
    echo "   Or Docker: docker run -d -p 6379:6379 --name redis redis:7"
fi

echo ""
echo "2️⃣  To start all services, run in separate terminals:"
echo ""
echo "   Terminal A (API):"
echo "     cd backend && ./run_api.sh"
echo ""
echo "   Terminal B (Redis - if not running):"
echo "     redis-server"
echo "     # or: docker run -d -p 6379:6379 --name redis redis:7"
echo ""
echo "   Terminal C (Celery Worker):"
echo "     cd backend && ./run_celery_worker.sh"
echo ""
echo "   Terminal D (Celery Beat - optional):"
echo "     cd backend && ./run_celery_beat.sh"
echo ""
echo "📝 Services:"
echo "   - FastAPI: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Redis: localhost:6379"
echo "   - Celery Worker: Running in Terminal C"
echo ""

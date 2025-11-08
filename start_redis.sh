#!/bin/bash
# Start Redis server

echo "🔴 Starting Redis..."

# Check if Redis is already running
if command -v redis-cli > /dev/null 2>&1; then
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis is already running"
        redis-cli ping
        exit 0
    fi
fi

# Try to start local Redis
if command -v redis-server > /dev/null 2>&1; then
    echo "📦 Starting local Redis server..."
    redis-server --daemonize yes
    sleep 2
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis started successfully"
        redis-cli ping
        exit 0
    fi
fi

# Try Docker
if command -v docker > /dev/null 2>&1; then
    echo "🐳 Trying Docker..."
    if docker ps -a | grep -q redis; then
        docker start redis 2>/dev/null || docker run -d -p 6379:6379 --name redis redis:7
    else
        docker run -d -p 6379:6379 --name redis redis:7
    fi
    sleep 3
    if command -v redis-cli > /dev/null 2>&1 && redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis started with Docker"
        exit 0
    fi
fi

echo "❌ Could not start Redis automatically"
echo ""
echo "Please install Redis:"
echo "  macOS: brew install redis"
echo "  Then: brew services start redis"
echo ""
echo "Or use Docker:"
echo "  docker run -d -p 6379:6379 --name redis redis:7"
exit 1

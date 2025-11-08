#!/bin/bash
# Check if Redis is running

if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is running"
    redis-cli ping
else
    echo "❌ Redis is not running"
    echo ""
    echo "Start Redis with one of:"
    echo "  1. redis-server (if installed locally)"
    echo "  2. docker run -d -p 6379:6379 --name redis redis:7"
    echo ""
    exit 1
fi

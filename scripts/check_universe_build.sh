#!/bin/bash
# Check universe build status

if [ -f /tmp/universe_build.pid ]; then
    PID=$(cat /tmp/universe_build.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "🔄 Universe build is still running (PID: $PID)"
        echo "📊 Recent logs:"
        tail -5 /tmp/universe_build.log 2>/dev/null || echo "  No logs yet..."
    else
        echo "✅ Universe build completed!"
        echo "📋 Final result:"
        tail -20 /tmp/universe_build.log 2>/dev/null
    fi
else
    echo "ℹ️  No universe build process found"
fi

echo ""
echo "Current universe size:"
curl -s "http://localhost:8000/api/v1/universe/list" | python3 -m json.tool 2>/dev/null | head -5 || echo "  Error fetching universe list"

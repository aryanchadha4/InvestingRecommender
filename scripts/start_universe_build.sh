#!/bin/bash
# Start universe build in background

COUNT=${1:-100}
LOOKBACK_DAYS=${2:-1095}

echo "🚀 Starting universe build in background..."
echo "   Count: $COUNT symbols"
echo "   Lookback: $LOOKBACK_DAYS days"
echo ""

nohup curl -X POST "http://localhost:8000/api/v1/universe/build?count=$COUNT&lookback_days=$LOOKBACK_DAYS" > /tmp/universe_build.log 2>&1 &
echo $! > /tmp/universe_build.pid

echo "✅ Build started (PID: $(cat /tmp/universe_build.pid))"
echo "📝 Monitor: tail -f /tmp/universe_build.log"
echo "📊 Check status: ./scripts/check_universe_build.sh"

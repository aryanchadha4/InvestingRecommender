#!/bin/bash

# API Smoke Tests for Investment Recommender
# Make sure the API is running on http://localhost:8000

set -e

# Check if API is running
if ! curl -s -f "http://localhost:8000/api/v1/health/" > /dev/null 2>&1; then
    echo "❌ API server is not running on http://localhost:8000"
    echo "   Start it with: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    exit 1
fi

API_URL="http://localhost:8000/api/v1"

echo "🧪 Starting API Smoke Tests"
echo "================================"
echo ""

# (A) Backfill and compute signals
echo "📊 (A) Backfilling prices and computing signals"
echo "--------------------------------"

echo "1. Backfilling ~3y of prices for default symbols..."
curl -X POST "${API_URL}/signals/backfill?symbols=VOO&symbols=QQQM&symbols=IWM&symbols=EFA&symbols=EMB&symbols=AGG" \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n" \
  -s | (jq '.' 2>/dev/null || python3 -m json.tool 2>/dev/null || cat)

echo ""
echo "2. Computing & persisting today's momentum + sentiment..."
curl -X POST "${API_URL}/signals/compute?symbols=VOO&symbols=QQQM&symbols=IWM&symbols=EFA&symbols=EMB&symbols=AGG" \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n" \
  -s | (jq '.' 2>/dev/null || python3 -m json.tool 2>/dev/null || cat)

echo ""
echo ""

# (B) Recommendation sanity checks
echo "💡 (B) Recommendation sanity checks"
echo "--------------------------------"

echo "3. Balanced, \$10k, default symbols..."
curl "${API_URL}/recommend/?risk=balanced&amount=10000" \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n" \
  -s | (jq '.' 2>/dev/null || python3 -m json.tool 2>/dev/null || cat)

echo ""
echo "4. Conservative, \$5k..."
curl "${API_URL}/recommend/?risk=conservative&amount=5000" \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n" \
  -s | (jq '.' 2>/dev/null || python3 -m json.tool 2>/dev/null || cat)

echo ""
echo "5. Aggressive, \$50k, subset of symbols..."
curl "${API_URL}/recommend/?risk=aggressive&amount=50000&symbols=VOO&symbols=QQQM&symbols=IWM" \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n" \
  -s | (jq '.' 2>/dev/null || python3 -m json.tool 2>/dev/null || cat)

echo ""
echo "6. Aggressive, \$2k, bonds tilted (include AGG, EMB explicitly)..."
curl "${API_URL}/recommend/?risk=aggressive&amount=2000&symbols=VOO&symbols=QQQM&symbols=AGG&symbols=EMB" \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n" \
  -s | (jq '.' 2>/dev/null || python3 -m json.tool 2>/dev/null || cat)

echo ""
echo "================================"
echo "✅ Smoke tests completed!"


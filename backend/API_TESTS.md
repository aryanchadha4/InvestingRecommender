# API Smoke Tests

Quick API testing commands for the Investment Recommender API.

**Prerequisites**: Make sure the API is running on `http://localhost:8000`

## (A) Backfill and Compute Signals

### 1. Backfill ~3y of prices

```bash
curl -X POST "http://localhost:8000/api/v1/signals/backfill?symbols=VOO&symbols=QQQM&symbols=IWM&symbols=EFA&symbols=EMB&symbols=AGG"
```

### 2. Compute & persist today's momentum + sentiment

```bash
curl -X POST "http://localhost:8000/api/v1/signals/compute?symbols=VOO&symbols=QQQM&symbols=IWM&symbols=EFA&symbols=EMB&symbols=AGG"
```

## (B) Recommendation Sanity Checks

### 3. Balanced, $10k, default symbols

```bash
curl "http://localhost:8000/api/v1/recommend/?risk=balanced&amount=10000"
```

### 4. Conservative, $5k

```bash
curl "http://localhost:8000/api/v1/recommend/?risk=conservative&amount=5000"
```

### 5. Aggressive, $50k, subset of symbols

```bash
curl "http://localhost:8000/api/v1/recommend/?risk=aggressive&amount=50000&symbols=VOO&symbols=QQQM&symbols=IWM"
```

### 6. Aggressive, $2k, bonds tilted (include AGG, EMB explicitly)

```bash
curl "http://localhost:8000/api/v1/recommend/?risk=aggressive&amount=2000&symbols=VOO&symbols=QQQM&symbols=AGG&symbols=EMB"
```

## Running All Tests

Use the test script to run all tests at once:

```bash
cd backend
./test_api.sh
```

Or run the script with formatted output (requires `jq`):

```bash
./test_api.sh | jq '.'
```

## Expected Responses

### Backfill Response
```json
{
  "inserted_or_updated_rows": {
    "VOO": 756,
    "QQQM": 755,
    ...
  }
}
```

### Compute Response
```json
{
  "signals": [
    {
      "symbol": "VOO",
      "date": "2025-01-07",
      "momentum": 0.05,
      "sentiment": 0.02,
      "score": 0.041
    },
    ...
  ]
}
```

### Recommendation Response
```json
{
  "inputs": {
    "risk": "balanced",
    "amount": 10000.0,
    "symbols": ["VOO", "QQQM", "IWM", "EFA", "EMB", "AGG"]
  },
  "signals": [...],
  "allocation_weights": {
    "VOO": 0.30,
    "QQQM": 0.25,
    ...
  },
  "allocation_dollars": {
    "VOO": 3000.0,
    "QQQM": 2500.0,
    ...
  },
  "cov_estimation_days": 252,
  "notes": [...]
}
```

## Troubleshooting

### API not running
Start the API server:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Database connection errors
Make sure PostgreSQL is running:
```bash
# Check if database is running
pg_isready -h localhost -p 5432
```

### No data returned
Run backfill first to populate the database with price data.

### Format JSON output
Install `jq` for pretty JSON formatting:
```bash
# macOS
brew install jq

# Then use in curl commands:
curl ... | jq '.'
```


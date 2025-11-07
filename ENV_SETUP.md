# How to Add API Keys

## Step 1: Locate your `.env` file

The `.env` file should be in the **project root** directory (`/Users/aryanchadha/InvestingRecommender/.env`).

If you don't have a `.env` file, create it by copying the example:

```bash
cd /Users/aryanchadha/InvestingRecommender
cp .env.example .env
```

## Step 2: Edit the `.env` file

Open the `.env` file in your text editor and add your API keys:

```bash
# Option 1: Using a text editor (recommended)
nano .env
# or
code .env
# or
vim .env
```

## Step 3: Add your API keys

Add the following lines to your `.env` file (replace with your actual keys):

```bash
# Market Data API Keys
POLYGON_API_KEY=your_polygon_api_key_here

# News API Keys
NEWSAPI_API_KEY=your_newsapi_key_here

# Sentiment Analysis Model (optional - already has default)
FINBERT_MODEL=ProsusAI/finbert
```

### Example `.env` file:

```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg://invest:invest@localhost:5432/investdb
REDIS_URL=redis://localhost:6379/0

# Application Settings
ENV=dev
SECRET_KEY=change-me-in-production

# Market Data API Keys
POLYGON_API_KEY=abc123xyz789  # <-- Add your Polygon.io key here

# News API Keys
NEWSAPI_API_KEY=def456uvw012  # <-- Add your NewsAPI key here

# Sentiment Analysis Model
FINBERT_MODEL=ProsusAI/finbert
```

## Step 4: Save and verify

1. Save the `.env` file
2. The application will automatically load these variables on startup
3. No restart needed if the app is using environment variables

## Quick Commands

### View your current `.env` file:
```bash
cat .env
```

### Edit your `.env` file:
```bash
nano .env
```

### Check if keys are loaded (Python):
```bash
cd backend
python3 -c "from app.core.config import settings; print('Polygon:', 'Set' if settings.polygon_api_key else 'Not set'); print('NewsAPI:', 'Set' if settings.newsapi_api_key else 'Not set')"
```

## Important Notes

1. **Never commit `.env` to git** - it contains sensitive information
2. **The `.env` file is already in `.gitignore`** (or should be)
3. **API keys are optional** - the app works without them (uses fallbacks)
4. **Location matters** - Make sure the `.env` file is in the project root, not in the `backend/` directory

## Troubleshooting

### If keys aren't loading:
1. Make sure the `.env` file is in the project root
2. Check for typos in variable names (must match exactly)
3. Restart the application/server
4. Verify the keys are on separate lines (no spaces around `=`)

### If using Docker:
- Make sure `.env` is in the project root (where `docker-compose.yml` is)
- Docker Compose automatically loads `.env` files


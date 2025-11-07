# API Keys Configuration

This document explains how to obtain API keys for the Investment Recommender application.

## Required API Keys

All API keys are **optional** - the application will use fallback providers if keys are not provided.

### 1. Polygon.io API Key (Optional)

**Purpose**: Real-time and historical market data provider

**Where to get it**:
1. Visit: https://polygon.io/dashboard/signup
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key from the "API Keys" section

**Free Tier**:
- 5 API calls per minute
- Historical data access
- Suitable for development and small-scale use

**Usage**:
- Set `POLYGON_API_KEY` in your `.env` file
- If not set, the application will use yfinance (no API key required)

### 2. NewsAPI.org API Key (Optional)

**Purpose**: Financial news headlines provider

**Where to get it**:
1. Visit: https://newsapi.org/register
2. Sign up for a free account
3. Check your email for the API key
4. Copy your API key from the email or dashboard

**Free Tier**:
- 100 requests per day
- Development use only
- Suitable for testing and development

**Usage**:
- Set `NEWSAPI_API_KEY` in your `.env` file
- If not set, the application will use Google News RSS (no API key required)

### 3. FinBERT Model (Optional)

**Purpose**: Financial sentiment analysis model

**Model**: ProsusAI/finbert (default)

**Where to get it**:
- No API key required - it's a HuggingFace model
- Automatically downloads on first use (~500MB)
- Requires internet connection for first download

**Usage**:
- Set `FINBERT_MODEL` in your `.env` file (optional, defaults to "ProsusAI/finbert")
- If FinBERT fails to load, the application will use VADER (no API key required)

## Configuration

Add these to your `.env` file:

```bash
# Market Data API Keys
POLYGON_API_KEY=your_polygon_api_key_here

# News API Keys
NEWSAPI_API_KEY=your_newsapi_key_here

# Sentiment Analysis Model
FINBERT_MODEL=ProsusAI/finbert
```

## Fallback Behavior

The application is designed to work without any API keys:

- **Market Data**: yfinance (free, no API key)
- **News**: Google News RSS (free, no API key)
- **Sentiment**: VADER (free, no API key)

API keys are only needed if you want to use the premium providers (Polygon.io, NewsAPI.org, FinBERT).

## Environment Variables

All environment variables are documented in `.env.example`. Copy it to `.env` and fill in your keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```


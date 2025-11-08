"""Market data provider with yfinance and optional Polygon."""

from __future__ import annotations

from datetime import date, datetime, timedelta
import pandas as pd
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os

try:
    import yfinance as yf
except Exception:
    yf = None


class MarketProvider:
    def __init__(self, polygon_api_key: str | None = None):
        self.polygon_api_key = polygon_api_key or os.getenv("POLYGON_API_KEY")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def fetch_daily_prices(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        # Prefer Polygon if key provided; otherwise yfinance
        if self.polygon_api_key:
            return await self._fetch_polygon(symbol, start, end)
        return await self._fetch_yfinance(symbol, start, end)

    async def _fetch_yfinance(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        if yf is None:
            raise RuntimeError("yfinance not installed")
        # yfinance is sync; call in thread if you wish; here keep simple
        df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=False)
        if df.empty:
            raise ValueError(f"No yfinance data for {symbol}")
        
        # Handle MultiIndex columns (yfinance returns MultiIndex when single symbol)
        if isinstance(df.columns, pd.MultiIndex):
            # Flatten MultiIndex columns
            df.columns = df.columns.droplevel(1) if df.columns.nlevels > 1 else df.columns
        
        # Reset index to get Date as a column
        df = df.reset_index()
        
        # Rename columns
        df = df.rename(columns={"Close": "close", "Volume": "volume", "Date": "date"})
        
        # Ensure date column is datetime, then convert to date
        if "date" not in df.columns and "Date" in df.columns:
            df["date"] = pd.to_datetime(df["Date"]).dt.date
        elif "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.date
        
        # Select only needed columns
        df = df[["date", "close", "volume"]].dropna()
        return df

    async def _fetch_polygon(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start}/{end}"
        params = {"adjusted": "true", "sort": "asc", "apiKey": self.polygon_api_key, "limit": 50000}

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()

        results = data.get("results", [])
        if not results:
            raise ValueError(f"No Polygon data for {symbol}")

        rows = []
        for x in results:
            d = datetime.utcfromtimestamp(x["t"] / 1000).date()
            rows.append({"date": d, "close": float(x["c"]), "volume": float(x.get("v", 0))})

        return pd.DataFrame(rows)

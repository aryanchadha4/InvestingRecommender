"""Signal computation service with persistence."""

from __future__ import annotations

import asyncio
import pandas as pd
from datetime import date, timedelta

from .prices_cov import load_price_matrix, pct_returns
from ..providers.sentiment_provider import SentimentProvider
from ..providers.news_provider import NewsProvider
from ..providers.market_provider import MarketProvider
from ..providers.universe_provider import UniverseProvider
from ...db.repositories.signal_repo import SignalRepo
from ...db.repositories.asset_repo import AssetRepo
from ...db.repositories.price_repo import PriceRepo
from ...db.session import SessionLocal


class SignalService:
    def __init__(self, market: MarketProvider, news: NewsProvider, sentiment: SentimentProvider):
        self.market = market
        self.news = news
        self.sentiment = sentiment
        self.signal_repo = SignalRepo()
        self.asset_repo = AssetRepo()
        self.price_repo = PriceRepo()

    async def backfill_prices(self, symbol: str, lookback_days: int = 365 * 3) -> int:
        end, start = date.today(), date.today() - timedelta(days=lookback_days)

        # ensure asset exists
        self.asset_repo.ensure_assets([{"symbol": symbol, "name": symbol, "asset_class": "etf"}])

        # fetch & persist
        df = await self.market.fetch_daily_prices(symbol, start, end)

        # map to asset_id
        asset = self.asset_repo.get_by_symbol(symbol)
        if not asset:
            return 0

        rows = []
        for _, row in df.iterrows():
            date_val = row["date"]
            # Handle different date formats
            if isinstance(date_val, pd.Timestamp):
                date_val = date_val.date()
            elif isinstance(date_val, date):
                pass  # Already a date object
            else:
                # Convert string or other types to date
                if hasattr(date_val, 'date'):
                    date_val = date_val.date()
                else:
                    date_val = pd.to_datetime(str(date_val)).date()

            rows.append(
                {
                    "asset_id": asset.id,
                    "date": date_val,
                    "close": float(row["close"]),
                    "volume": float(row["volume"]),
                }
            )
        return self.price_repo.upsert_prices(rows)

    async def momentum_signal(self, symbol: str, lb_days: int = 60) -> float:
        end, start = date.today(), date.today() - timedelta(days=lb_days + 120)

        pm = load_price_matrix([symbol], start, end)

        if pm.empty or pm.shape[0] < lb_days + 1:
            await self.backfill_prices(symbol, lookback_days=lb_days + 365)
            pm = load_price_matrix([symbol], start, end)

        # simple trailing return
        s = pm[symbol].dropna()

        if len(s) < lb_days + 1:
            return 0.0

        return float((s.iloc[-1] - s.iloc[-lb_days - 1]) / s.iloc[-lb_days - 1])

    async def sentiment_signal(self, symbol: str, limit: int = 30) -> float:
        items = await self.news.fetch_headlines(symbol, limit)
        texts = [f"{x.get('title', '')} {x.get('text', '')}" for x in items]
        score = self.sentiment.score_texts(texts)
        return float(score)

    async def compute_and_persist(self, symbol: str, date_for: date | None = None) -> dict:
        date_for = date_for or date.today()

        mom = await self.momentum_signal(symbol)
        sen = await self.sentiment_signal(symbol)

        asset = self.asset_repo.get_by_symbol(symbol)
        if not asset:
            return {"symbol": symbol, "error": "Asset not found"}

        rows = [
            {
                "asset_id": asset.id,
                "date": date_for,
                "kind": "momentum",
                "value": mom,
                "meta": {},
            },
            {
                "asset_id": asset.id,
                "date": date_for,
                "kind": "sentiment",
                "value": sen,
                "meta": {},
            },
        ]

        self.signal_repo.upsert_signals(rows)

        return {
            "symbol": symbol,
            "date": str(date_for),
            "momentum": mom,
            "sentiment": sen,
            "score": 0.7 * mom + 0.3 * sen,
        }

    async def combine(self, symbol: str) -> dict:
        """Backward compatibility: compute signals without persisting."""
        mom = await self.momentum_signal(symbol)
        sen = await self.sentiment_signal(symbol)
        # weighted sum baseline
        value = 0.7 * mom + 0.3 * sen
        return {"symbol": symbol, "momentum": mom, "sentiment": sen, "score": value}


class UniverseService:
    def __init__(self, universe: UniverseProvider, market: MarketProvider):
        self.universe = universe
        self.asset_repo = AssetRepo()
        self.price_repo = PriceRepo()
        self.market = market

    async def ensure_assets_and_backfill(self, count: int = 100, lookback_days: int = 365 * 3) -> dict:
        symbols = await self.universe.expanded_universe(count=count)
        # 1) persist assets
        self.asset_repo.ensure_assets([{"symbol": s, "name": s, "asset_class": "equity"} for s in symbols])

        # 2) get asset_ids
        with SessionLocal() as s:
            ids = {s: self.asset_repo.get_by_symbol(s).id for s in symbols}

        # 3) batch backfill concurrently
        end, start = date.today(), date.today() - timedelta(days=lookback_days)

        async def fetch_and_upsert(sym: str) -> tuple[str, int]:
            try:
                df = await self.market.fetch_daily_prices(sym, start, end)
                if df is None or df.empty:
                    return (sym, 0)

                rows = []
                for _, row in df.iterrows():
                    date_val = row["date"]
                    # Handle different date formats
                    if isinstance(date_val, pd.Timestamp):
                        date_val = date_val.date()
                    elif isinstance(date_val, date):
                        pass  # Already a date object
                    else:
                        # Convert string or other types to date
                        if hasattr(date_val, "date"):
                            date_val = date_val.date()
                        else:
                            date_val = pd.to_datetime(str(date_val)).date()

                    rows.append(
                        {
                            "asset_id": ids[sym],
                            "date": date_val,
                            "close": float(row["close"]),
                            "volume": float(row["volume"]),
                        }
                    )
                n = self.price_repo.upsert_prices(rows)
                return (sym, n)
            except Exception:
                return (sym, 0)

        sem = asyncio.Semaphore(10)  # limit concurrency

        async def guarded(sym: str):
            async with sem:
                return await fetch_and_upsert(sym)

        results = await asyncio.gather(*[guarded(s) for s in symbols])
        return {"symbols": symbols, "upserts": {k: v for k, v in results}}

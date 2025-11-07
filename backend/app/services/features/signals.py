"""Signal computation service with persistence."""

from __future__ import annotations

import pandas as pd
from datetime import date, timedelta

from .prices_cov import load_price_matrix, pct_returns
from ..providers.sentiment_provider import SentimentProvider
from ..providers.news_provider import NewsProvider
from ..providers.market_provider import MarketProvider
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
            if isinstance(date_val, pd.Timestamp):
                date_val = date_val.date()
            elif not isinstance(date_val, date):
                date_val = pd.to_datetime(date_val).date()

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

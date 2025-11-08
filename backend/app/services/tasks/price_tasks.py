# backend/app/services/tasks/price_tasks.py

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import asyncio

from .celery_app import app
from .task_utils import RetriableTask, respectful_sleep
from ..providers.market_provider import MarketProvider
from ...db.repositories.asset_repo import AssetRepo
from ...db.repositories.price_repo import PriceRepo
from ...db.session import SessionLocal


@app.task(bind=True, base=RetriableTask, name="price.fetch_and_store", rate_limit="30/m")
def fetch_and_store_prices(self, symbol: str, lookback_days: int = 365 * 3) -> dict:
    """
    Download daily OHLCV (we use close+volume) and upsert into Postgres.

    Idempotent via unique (asset_id, date).
    """
    market = MarketProvider()
    asset_repo, price_repo = AssetRepo(), PriceRepo()

    # Ensure asset exists
    asset_repo.ensure_assets([{"symbol": symbol, "name": symbol, "asset_class": "equity"}])
    with SessionLocal() as s:
        asset_id = asset_repo.get_by_symbol(symbol).id

    end, start = date.today(), date.today() - timedelta(days=lookback_days)

    # Celery workers are sync; bridge to async provider
    df = asyncio.run(market.fetch_daily_prices(symbol, start, end))

    if df is None or df.empty:
        return {"symbol": symbol, "rows": 0, "note": "no data"}

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
                "asset_id": asset_id,
                "date": date_val,
                "close": float(row["close"]),
                "volume": float(row["volume"]),
            }
        )

    n = price_repo.upsert_prices(rows)
    return {"symbol": symbol, "rows": int(n)}


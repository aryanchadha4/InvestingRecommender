"""Signal endpoints - backfill, compute, and preview."""

from fastapi import APIRouter, Query, Depends

from ...services.providers.market_provider import MarketProvider
from ...services.providers.news_provider import NewsProvider
from ...services.providers.sentiment_provider import SentimentProvider
from ...services.features.signals import SignalService
from ...api.deps import get_signal_service

router = APIRouter()


def _svc():
    return SignalService(MarketProvider(), NewsProvider(), SentimentProvider())


@router.post("/backfill")
async def backfill(symbols: list[str] = Query(...), lookback_days: int = 365 * 3):
    svc = _svc()
    counts = {}
    for s in symbols:
        counts[s] = await svc.backfill_prices(s, lookback_days=lookback_days)
    return {"inserted_or_updated_rows": counts}


@router.post("/compute")
async def compute(symbols: list[str] = Query(...)):
    svc = _svc()
    out = []
    for s in symbols:
        out.append(await svc.compute_and_persist(s))
    return {"signals": out}


@router.get("/")
async def preview_signals(
    symbol: str = Query(..., description="Symbol to preview signals for"),
    signal_service=Depends(get_signal_service),
):
    """Preview signals for a symbol (non-persisting)."""
    result = await signal_service.combine(symbol)
    return result

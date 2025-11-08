from fastapi import APIRouter, Query
from sqlalchemy import select

from ...services.providers.universe_provider import UniverseProvider
from ...services.providers.market_provider import MarketProvider
from ...services.features.signals import UniverseService
from ...db.session import SessionLocal
from ...db.models.asset import Asset

router = APIRouter()


@router.post("/build")
async def build_universe(count: int = Query(100, ge=10, le=500), lookback_days: int = 365 * 3):
    svc = UniverseService(UniverseProvider(), MarketProvider())
    return await svc.ensure_assets_and_backfill(count=count, lookback_days=lookback_days)


@router.get("/list")
def list_universe(limit: int = 1000):
    with SessionLocal() as s:
        rows = s.execute(select(Asset.symbol).order_by(Asset.symbol)).scalars().all()
    return {"count": len(rows), "symbols": rows[:limit]}


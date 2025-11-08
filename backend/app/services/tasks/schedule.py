# backend/app/services/tasks/schedule.py

from __future__ import annotations

from .celery_app import app
from .orchestrate import universe_backfill_and_signals
from ..providers.universe_provider import UniverseProvider
import asyncio


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Every day at 01:30 UTC: backfill top 100 + ETFs (3y window kept up to date)
    sender.add_periodic_task(
        24 * 60 * 60,  # seconds; switch to crontab if you prefer
        nightly_universe_refresh.s(100, 365 * 3),
        name="nightly_universe_refresh",
    )


@app.task(name="schedule.nightly_universe_refresh")
def nightly_universe_refresh(count: int = 100, lookback_days: int = 365 * 3):
    # Build current universe (same as your /universe/build behavior)
    from ..providers.market_provider import MarketProvider
    from ..features.signals import UniverseService

    uni = UniverseProvider()
    mkt = MarketProvider()
    svc = UniverseService(uni, mkt)

    result = asyncio.run(svc.ensure_assets_and_backfill(count=count, lookback_days=lookback_days))
    # Kick signal compute in bulk
    symbols = result.get("symbols", [])
    universe_backfill_and_signals.delay(symbols, lookback_days)
    return {"scheduled": len(symbols)}


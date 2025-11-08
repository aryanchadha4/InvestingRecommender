# backend/app/services/tasks/orchestrate.py

from __future__ import annotations

from celery import group

from .celery_app import app
from .price_tasks import fetch_and_store_prices
from .signal_tasks import compute_signal_task


@app.task(name="orchestrate.backfill_then_signals")
def universe_backfill_and_signals(symbols: list[str], lookback_days: int = 365 * 3) -> dict:
    """
    1) Fan out price backfill tasks for all symbols
    2) After they complete, fan out signal compute tasks

    Returns task ids so you can inspect if desired.
    """
    # 1) Prices
    g_price = group(fetch_and_store_prices.s(sym, lookback_days) for sym in symbols)
    r_price = g_price.apply_async()
    r_price.join()  # Wait here in orchestration (you could skip waiting and return job ids)

    # 2) Signals
    g_sig = group(compute_signal_task.s(sym) for sym in symbols)
    r_sig = g_sig.apply_async()

    return {
        "price_task_ids": [x.id for x in r_price.results],
        "signal_task_ids": [x.id for x in r_sig.results],
        "count": len(symbols),
    }


# backend/app/api/v1/ingest.py

from fastapi import APIRouter, Query

from celery.result import AsyncResult

from ...services.tasks.celery_app import app as celery_app
from ...services.tasks.orchestrate import universe_backfill_and_signals
from ...services.tasks.price_tasks import fetch_and_store_prices
from ...services.tasks.signal_tasks import compute_signal_task

router = APIRouter()


@router.post("/celery/backfill")
def queue_backfill(symbols: list[str] = Query(...), lookback_days: int = 365 * 3):
    job = universe_backfill_and_signals.delay(symbols, lookback_days)
    return {"job_id": job.id, "queued": len(symbols)}


@router.post("/celery/price")
def queue_price(symbol: str, lookback_days: int = 365 * 3):
    job = fetch_and_store_prices.delay(symbol, lookback_days)
    return {"task_id": job.id}


@router.post("/celery/signal")
def queue_signal(symbol: str):
    job = compute_signal_task.delay(symbol)
    return {"task_id": job.id}


@router.get("/celery/status/{task_id}")
def get_status(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    out = {
        "id": res.id,
        "state": res.state,  # PENDING, STARTED, RETRY, FAILURE, SUCCESS
        "ready": res.ready(),
        "successful": res.successful() if res.ready() else False,
    }
    if res.ready():
        try:
            out["result"] = res.get(propagate=False)
        except Exception as e:
            out["error"] = str(e)
    return out


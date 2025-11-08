# backend/app/services/tasks/signal_tasks.py

from __future__ import annotations

import asyncio

from .celery_app import app
from .task_utils import RetriableTask
from ..providers.sentiment_provider import SentimentProvider
from ..providers.news_provider import NewsProvider
from ..providers.market_provider import MarketProvider
from ..features.signals import SignalService


@app.task(bind=True, base=RetriableTask, name="signal.compute", rate_limit="90/m")
def compute_signal_task(self, symbol: str) -> dict:
    """
    Computes momentum + sentiment for a symbol (today) and upserts signals table.
    """
    svc = SignalService(MarketProvider(), NewsProvider(), SentimentProvider())

    # Call the async service method from sync Celery
    return asyncio.run(svc.compute_and_persist(symbol))


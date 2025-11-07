"""Celery tasks for nightly data ingestion."""

from celery import Celery

from ...core.config import settings
from ..providers.market_provider import MarketProvider
from ..providers.news_provider import NewsProvider
from ..providers.sentiment_provider import SentimentProvider
from ..features.signals import SignalService

celery_app = Celery("ingest", broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task
def nightly_refresh():
    # TODO: read symbols from DB; using defaults
    symbols = ["VOO", "QQQM", "IWM", "EFA", "EMB", "AGG"]
    market, news, sent = MarketProvider(), NewsProvider(), SentimentProvider()
    signals = SignalService(market, news, sent)

    # compute & persist signals (placeholder: just trigger calls)
    # In a real impl, insert into DB via repositories
    return {"refreshed": symbols}

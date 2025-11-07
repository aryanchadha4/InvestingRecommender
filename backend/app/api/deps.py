"""API dependencies."""

from typing import Generator
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.providers.market_provider import MarketProvider
from app.services.providers.news_provider import NewsProvider
from app.services.providers.sentiment_provider import SentimentProvider
from app.services.features.signals import SignalService


def get_database() -> Generator[Session, None, None]:
    """Dependency for database session."""
    yield from get_db()


def get_signal_service():
    return SignalService(MarketProvider(), NewsProvider(), SentimentProvider())

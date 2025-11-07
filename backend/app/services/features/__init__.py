"""Feature engineering and analysis modules."""

from app.services.features.signals import SignalService
from app.services.features.risk import RiskPolicy, policy_from_risk_level
from app.services.features.optimizer import mean_variance_opt
from app.services.features.recommender import RecommenderService, DEFAULT_SYMBOLS
from app.services.features.prices_cov import (
    load_price_matrix,
    pct_returns,
    cov_matrix,
    daily_log_returns,
)

__all__ = [
    "SignalService",
    "RiskPolicy",
    "policy_from_risk_level",
    "mean_variance_opt",
    "RecommenderService",
    "DEFAULT_SYMBOLS",
    "load_price_matrix",
    "pct_returns",
    "cov_matrix",
    "daily_log_returns",
]

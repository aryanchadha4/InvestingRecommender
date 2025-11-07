"""Recommendation service combining signals, risk, and optimization."""

import numpy as np
from datetime import date, timedelta

from .signals import SignalService
from .risk import policy_from_risk_level
from .optimizer import mean_variance_opt
from .prices_cov import load_price_matrix, cov_matrix

DEFAULT_SYMBOLS = ["VOO", "QQQM", "IWM", "EFA", "EMB", "AGG"]


class RecommenderService:
    def __init__(self, signal_service: SignalService):
        self.signals = signal_service

    async def recommend(self, risk: str, invest_amount: float, symbols: list[str] = None):
        symbols = symbols or DEFAULT_SYMBOLS

        # ensure data exists & compute signals
        sigs = []
        for s in symbols:
            await self.signals.backfill_prices(s, lookback_days=3 * 365)
            sigs.append(await self.signals.compute_and_persist(s))

        mu = np.array([x["score"] for x in sigs], dtype=float)

        end, start = date.today(), date.today() - timedelta(days=365)
        pm = load_price_matrix(symbols, start, end)

        if pm.empty or pm.shape[0] < 60:
            cov = np.eye(len(symbols)) * 0.04
        else:
            cov_df = cov_matrix(pm)
            cov = cov_df.reindex(index=symbols, columns=symbols).fillna(0.0).to_numpy()

        policy = policy_from_risk_level(risk)
        w = mean_variance_opt(mu, cov, max_w=policy.max_weight)

        allocation = {sym: float(a) for sym, a in zip(symbols, w)}
        dollars = {sym: round(invest_amount * wt, 2) for sym, wt in allocation.items()}

        return {
            "inputs": {"risk": risk, "amount": invest_amount, "symbols": symbols},
            "signals": sigs,
            "allocation_weights": allocation,
            "allocation_dollars": dollars,
            "cov_estimation_days": pm.shape[0] if not pm.empty else 0,
            "notes": [
                "Signals persisted to DB; covariance from realized daily returns (1y fallback to identity)."
            ],
        }

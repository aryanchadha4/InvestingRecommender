"""Risk policy mapping."""

from pydantic import BaseModel


class RiskPolicy(BaseModel):
    max_weight: float = 0.35
    min_weight: float = 0.0
    target_vol: float | None = None


def policy_from_risk_level(level: str) -> RiskPolicy:
    level = level.lower()
    if level == "conservative":
        return RiskPolicy(max_weight=0.25, target_vol=0.10)
    if level == "balanced":
        return RiskPolicy(max_weight=0.30, target_vol=0.15)
    if level == "aggressive":
        return RiskPolicy(max_weight=0.40, target_vol=0.25)
    return RiskPolicy()

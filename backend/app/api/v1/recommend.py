"""Recommendation endpoints."""

from fastapi import APIRouter, Query, Depends

from ...services.features.recommender import RecommenderService
from ...api.deps import get_signal_service

router = APIRouter()


@router.get("/")
async def get_recommendation(
    risk: str = Query("balanced", pattern="^(conservative|balanced|aggressive)$"),
    amount: float = 10000,
    symbols: list[str] | None = Query(None),
    signal_service=Depends(get_signal_service),
):
    recommender = RecommenderService(signal_service)
    return await recommender.recommend(risk=risk, invest_amount=amount, symbols=symbols)

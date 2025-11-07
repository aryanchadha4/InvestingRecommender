"""Portfolio endpoints - save/load."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_database
from app.db.models.portfolio import Portfolio

router = APIRouter()


@router.get("/{user_id}")
async def load_portfolio(
    user_id: str,
    db: Session = Depends(get_database),
) -> List[dict]:
    """Load portfolio for a user."""
    stmt = select(Portfolio).where(Portfolio.user_id == user_id)
    result = db.execute(stmt)
    portfolios = result.scalars().all()
    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "allocations": p.allocations,
            "policy": p.policy,
        }
        for p in portfolios
    ]


@router.post("/")
async def save_portfolio(
    user_id: str,
    allocations: dict,
    policy: dict | None = None,
    db: Session = Depends(get_database),
) -> dict:
    """Save a portfolio."""
    portfolio = Portfolio(user_id=user_id, allocations=allocations, policy=policy or {})
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return {
        "id": portfolio.id,
        "user_id": portfolio.user_id,
        "allocations": portfolio.allocations,
        "policy": portfolio.policy,
    }

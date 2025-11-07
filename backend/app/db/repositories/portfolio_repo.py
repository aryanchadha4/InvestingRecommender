"""Portfolio repository."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.db.models.portfolio import Portfolio


class PortfolioRepository:
    """Repository for Portfolio operations."""

    def __init__(self, db: Session) -> None:
        """Initialize repository with database session."""
        self.db = db

    def get_by_id(self, portfolio_id: int) -> Optional[Portfolio]:
        """Get portfolio entry by ID."""
        stmt = select(Portfolio).where(Portfolio.id == portfolio_id)
        return self.db.scalar(stmt)

    def get_by_user_id(self, user_id: str) -> List[Portfolio]:
        """Get all portfolio entries for a user."""
        stmt = select(Portfolio).where(Portfolio.user_id == user_id)
        return list(self.db.scalars(stmt).all())

    def get_by_user_and_asset(
        self, user_id: str, asset_id: int
    ) -> Optional[Portfolio]:
        """Get portfolio entry for specific user and asset."""
        stmt = select(Portfolio).where(
            and_(Portfolio.user_id == user_id, Portfolio.asset_id == asset_id)
        )
        return self.db.scalar(stmt)

    def create(self, portfolio: Portfolio) -> Portfolio:
        """Create a new portfolio entry."""
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio

    def update(self, portfolio: Portfolio) -> Portfolio:
        """Update an existing portfolio entry."""
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio

    def delete(self, portfolio_id: int) -> bool:
        """Delete a portfolio entry."""
        portfolio = self.get_by_id(portfolio_id)
        if portfolio:
            self.db.delete(portfolio)
            self.db.commit()
            return True
        return False


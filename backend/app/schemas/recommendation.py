"""Recommendation schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class RecommendationBase(BaseModel):
    """Base recommendation schema."""

    asset_id: int
    action: str = Field(..., max_length=20)  # buy, sell, hold
    confidence: Decimal = Field(..., ge=0, le=1, decimal_places=2)
    target_price: Optional[Decimal] = Field(None, ge=0, decimal_places=4)
    stop_loss: Optional[Decimal] = Field(None, ge=0, decimal_places=4)
    reasoning: Optional[str] = None
    risk_score: Optional[Decimal] = Field(None, ge=0, le=1, decimal_places=2)


class RecommendationCreate(RecommendationBase):
    """Schema for creating a recommendation."""

    expires_at: Optional[datetime] = None


class Recommendation(RecommendationBase):
    """Recommendation schema with ID and timestamps."""

    id: int
    created_at: datetime
    expires_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


"""Portfolio schemas."""

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PortfolioBase(BaseModel):
    """Base portfolio schema."""

    user_id: str = Field(..., max_length=100)
    asset_id: int
    quantity: Decimal = Field(..., ge=0, decimal_places=4)
    average_price: Decimal = Field(..., ge=0, decimal_places=4)


class PortfolioCreate(PortfolioBase):
    """Schema for creating a portfolio entry."""

    pass


class PortfolioUpdate(BaseModel):
    """Schema for updating a portfolio entry."""

    quantity: Decimal | None = Field(None, ge=0, decimal_places=4)
    average_price: Decimal | None = Field(None, ge=0, decimal_places=4)


class Portfolio(PortfolioBase):
    """Portfolio schema with ID and timestamps."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


"""Signal schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class SignalBase(BaseModel):
    """Base signal schema."""

    asset_id: int
    signal_type: str = Field(..., max_length=50)
    strength: Decimal = Field(..., ge=0, le=1, decimal_places=2)
    source: str = Field(..., max_length=100)
    metadata: Optional[str] = None
    timestamp: datetime


class SignalCreate(SignalBase):
    """Schema for creating a signal."""

    pass


class Signal(SignalBase):
    """Signal schema with ID and timestamps."""

    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


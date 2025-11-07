"""Asset schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AssetBase(BaseModel):
    """Base asset schema."""

    symbol: str = Field(..., max_length=20)
    name: str = Field(..., max_length=255)
    asset_type: str = Field(..., max_length=50)
    sector: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class AssetCreate(AssetBase):
    """Schema for creating an asset."""

    pass


class AssetUpdate(BaseModel):
    """Schema for updating an asset."""

    name: Optional[str] = Field(None, max_length=255)
    sector: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class Asset(AssetBase):
    """Asset schema with ID and timestamps."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


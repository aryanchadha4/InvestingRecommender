"""Common schema definitions."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    created_at: datetime
    updated_at: datetime | None = None


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(from_attributes=True)


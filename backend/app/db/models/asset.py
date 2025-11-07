"""Asset model."""

from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.base import Base


class Asset(Base):
    __tablename__ = "assets"

    __table_args__ = (UniqueConstraint("symbol", name="uq_assets_symbol"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    name: Mapped[str] = mapped_column(String(120), default="")
    asset_class: Mapped[str] = mapped_column(String(20), default="equity")  # equity, etf, bond, crypto
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

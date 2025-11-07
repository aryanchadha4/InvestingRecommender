"""Price model."""

from sqlalchemy import ForeignKey, Date, Numeric, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Price(Base):
    __tablename__ = "prices"

    __table_args__ = (
        UniqueConstraint("asset_id", "date", name="uq_prices_asset_date"),
        Index("ix_prices_asset_date", "asset_id", "date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), index=True)
    date: Mapped[object] = mapped_column(Date)
    close: Mapped[float] = mapped_column(Numeric(18, 6))
    volume: Mapped[float] = mapped_column(Numeric(18, 2), default=0)

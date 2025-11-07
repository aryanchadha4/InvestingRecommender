"""Signal model."""

from sqlalchemy import ForeignKey, Date, JSON, String, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Signal(Base):
    __tablename__ = "signals"

    __table_args__ = (
        UniqueConstraint("asset_id", "date", "kind", name="uq_signals_asset_date_kind"),
        Index("ix_signals_asset_date_kind", "asset_id", "date", "kind"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), index=True)
    date: Mapped[object] = mapped_column(Date)
    kind: Mapped[str] = mapped_column(String(30))  # momentum, sentiment, value, risk
    value: Mapped[float]
    meta: Mapped[dict] = mapped_column(JSON, default=dict)

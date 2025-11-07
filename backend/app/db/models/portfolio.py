"""Portfolio model."""

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True, default="demo")
    allocations: Mapped[dict] = mapped_column(
        JSON, default=dict
    )  # {symbol: weight}
    policy: Mapped[dict] = mapped_column(
        JSON, default=dict
    )  # constraints/inputs


from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select, func

from ...db.session import SessionLocal
from ...db.models.asset import Asset
from ...db.models.price import Price


def top_by_avg_volume(k: int = 60, lookback_days: int = 60) -> list[str]:
    with SessionLocal() as s:
        end = date.today()
        start = end - timedelta(days=lookback_days)

        q = (
            select(Asset.symbol, func.avg(Price.volume).label("avgv"))
            .join(Price, Price.asset_id == Asset.id)
            .where(Price.date >= start, Price.date <= end)
            .group_by(Asset.symbol)
            .order_by(func.avg(Price.volume).desc())
            .limit(k)
        )

        rows = s.execute(q).all()
        return [r[0] for r in rows]


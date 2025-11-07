"""Price repository."""

from sqlalchemy.dialects.postgresql import insert

from ..session import SessionLocal
from ..models.price import Price


class PriceRepo:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def upsert_prices(self, rows: list[dict]) -> int:
        """
        rows: [{'asset_id':1,'date':date(YYYY,MM,DD),'close':float,'volume':float}, ...]
        """
        if not rows:
            return 0

        stmt = insert(Price).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_prices_asset_date",
            set_={"close": stmt.excluded.close, "volume": stmt.excluded.volume},
        )

        with self.session_factory() as s:
            res = s.execute(stmt)
            s.commit()
            return res.rowcount or 0

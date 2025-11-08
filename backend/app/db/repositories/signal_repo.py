"""Signal repository."""

from sqlalchemy.dialects.postgresql import insert

from ..session import SessionLocal
from ..models.signal import Signal


class SignalRepo:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def upsert_signals(self, rows: list[dict]) -> int:
        """
        rows: [{'asset_id':1,'date':date(...),'kind':'momentum','value':0.12,'meta':{...}}, ...]
        """
        if not rows:
            return 0

        stmt = insert(Signal).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_signals_asset_date_kind",
            set_={"value": stmt.excluded.value, "meta": stmt.excluded.meta},
        )

        with self.session_factory() as s:
            res = s.execute(stmt)
            s.commit()
            # rowcount can be -1 if not available, so return len(rows) as fallback
            return res.rowcount if res.rowcount and res.rowcount > 0 else len(rows)

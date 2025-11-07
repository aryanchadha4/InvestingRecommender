"""Asset repository."""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from ..session import SessionLocal
from ..models.asset import Asset


class AssetRepo:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def get_by_symbol(self, symbol: str) -> Asset | None:
        with self.session_factory() as s:
            return s.execute(select(Asset).where(Asset.symbol == symbol)).scalar_one_or_none()

    def ensure_assets(self, assets: list[dict]) -> list[int]:
        """assets: [{'symbol': 'VOO', 'name':'Vanguard 500', 'asset_class':'etf'}, ...]"""
        if not assets:
            return []

        stmt = insert(Asset).values(assets)
        stmt = stmt.on_conflict_do_update(
            index_elements=["symbol"],
            set_={"name": stmt.excluded.name, "asset_class": stmt.excluded.asset_class},
        )

        with self.session_factory() as s:
            result = s.execute(stmt.returning(Asset.id))
            s.commit()
            return [r[0] for r in result.fetchall()]

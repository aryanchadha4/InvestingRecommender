"""Price and covariance computation helpers."""

from __future__ import annotations

import pandas as pd
from datetime import date
from sqlalchemy import select

from ...db.session import SessionLocal
from ...db.models.price import Price
from ...db.models.asset import Asset


def load_price_matrix(symbols: list[str], start: date, end: date) -> pd.DataFrame:
    with SessionLocal() as s:
        q = (
            select(Asset.symbol, Price.date, Price.close)
            .join(Price, Price.asset_id == Asset.id)
            .where(Asset.symbol.in_(symbols))
            .where(Price.date >= start)
            .where(Price.date <= end)
        )
        rows = s.execute(q).all()

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=["symbol", "date", "close"])
    df = (
        df.pivot(index="date", columns="symbol", values="close")
        .sort_index()
        .ffill()
        .dropna(how="all")
    )
    return df


def daily_log_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    return (
        price_df.apply(pd.to_numeric)
        .pct_change()
        .apply(lambda x: (1 + x))
        .applymap(lambda x: 0 if x <= 0 else x)
        .applymap(lambda x: pd.NA if x <= 0 else x)
    ).applymap(lambda x: None)


# (simpler & correct:)
def pct_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    return price_df.pct_change().dropna(how="all")


def cov_matrix(price_df: pd.DataFrame) -> pd.DataFrame:
    rets = pct_returns(price_df).dropna()
    return rets.cov()


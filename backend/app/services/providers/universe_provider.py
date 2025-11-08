# backend/app/services/providers/universe_provider.py

from __future__ import annotations

import os, asyncio

import httpx

from datetime import date, timedelta


ETF_CORE = ["VOO", "QQQM", "IWM", "EFA", "EMB", "AGG"]


class UniverseProvider:
    def __init__(self, polygon_api_key: str | None = None):
        self.polygon_api_key = polygon_api_key or os.getenv("POLYGON_API_KEY")

    async def top_volume(self, count: int = 100) -> list[str]:
        if self.polygon_api_key:
            try:
                return await self._polygon_top_volume(count)
            except Exception:
                pass
        # fallback to Yahoo (screened via yfinance: top volume last ~30d across a known basket, e.g., S&P500)
        try:
            return await self._yahoo_top_volume_sp500(count)
        except Exception:
            # final fallback: return ETFs only
            return ETF_CORE

    async def _polygon_top_volume(self, count: int) -> list[str]:
        # Use Polygon "most active" aggregates today
        # Docs: /v2/snapshot/locale/us/markets/stocks/most-active
        url = "https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/most-active"
        params = {"apiKey": self.polygon_api_key}

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()

        tickers = []
        for item in data.get("tickers", []):
            sym = item.get("ticker")
            # Filter out weird symbols (warrants/units)
            if not sym:
                continue
            if any(s in sym for s in ("-", "^", ".U", ".W")):  # crude filter
                continue
            tickers.append(sym)
            if len(tickers) >= count:
                break

        # include ETFs at the end (dedup later)
        return tickers

    async def _yahoo_top_volume_sp500(self, count: int) -> list[str]:
        # Pull S&P500 list then rank by 30d avg volume
        try:
            from yahoo_fin import stock_info as si
        except Exception as e:
            raise RuntimeError("Install yahoo_fin: pip install yahoo_fin --upgrade") from e

        spx = si.tickers_sp500()

        # yfinance is sync; we'll fetch volumes in parallel with threads via asyncio.to_thread
        import yfinance as yf

        end = date.today()
        start = end - timedelta(days=45)

        async def vol_for(sym: str) -> tuple[str, float]:
            def _job():
                df = yf.download(sym, start=start, end=end, progress=False, auto_adjust=False)
                if df.empty:
                    return (sym, 0.0)
                return (sym, float(df["Volume"].tail(30).mean()))

            return await asyncio.to_thread(_job)

        tasks = [vol_for(s) for s in spx]
        vols = await asyncio.gather(*tasks, return_exceptions=True)
        rows = [(s, v) for (s, v) in vols if not isinstance((s, v), Exception)]
        rows = sorted(rows, key=lambda x: x[1], reverse=True)
        top = [s for s, _ in rows[:count]]

        return top

    async def expanded_universe(self, count: int = 100) -> list[str]:
        tickers = await self.top_volume(count=count)
        # Merge ETFs + top-volume, dedup, keep order (ETFs first)
        seen = set()
        out = []
        for s in ETF_CORE + tickers:
            if s and s not in seen:
                out.append(s)
                seen.add(s)
        return out


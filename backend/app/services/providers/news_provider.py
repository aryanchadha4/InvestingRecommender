"""News provider with NewsAPI and Google News RSS fallback."""

from __future__ import annotations

import os
import re
import html

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential


class NewsProvider:
    def __init__(self, newsapi_key: str | None = None):
        self.newsapi_key = newsapi_key or os.getenv("NEWSAPI_API_KEY")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=6))
    async def fetch_headlines(self, symbol: str, limit: int = 25) -> list[dict]:
        if self.newsapi_key:
            return await self._newsapi(symbol, limit)
        return await self._google_news(symbol, limit)

    async def _newsapi(self, symbol: str, limit: int) -> list[dict]:
        url = "https://newsapi.org/v2/everything"
        q = f'"{symbol}" OR {symbol}'
        params = {"q": q, "language": "en", "pageSize": min(limit, 100), "sortBy": "publishedAt"}
        headers = {"X-Api-Key": self.newsapi_key}

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, params=params, headers=headers)
            r.raise_for_status()
            data = r.json()

        arts = data.get("articles", [])
        out = []
        seen = set()

        for a in arts:
            title = a.get("title") or ""
            url = a.get("url")
            norm = self._norm(title)
            if not title or norm in seen:
                continue
            seen.add(norm)
            out.append({"title": title, "text": a.get("description") or "", "url": url})
            if len(out) >= limit:
                break

        return out

    async def _google_news(self, symbol: str, limit: int) -> list[dict]:
        url = "https://news.google.com/rss/search"
        params = {"q": symbol, "hl": "en-US", "gl": "US", "ceid": "US:en"}

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "xml")

        out, seen = [], set()

        for item in soup.find_all("item"):
            title = item.title.text if item.title else ""
            desc = item.description.text if item.description else ""
            link = item.link.text if item.link else ""

            norm = self._norm(title)
            if not title or norm in seen:
                continue
            seen.add(norm)

            out.append({"title": html.unescape(title), "text": self._strip(desc), "url": link})
            if len(out) >= limit:
                break

        return out

    def _strip(self, s: str) -> str:
        s = html.unescape(s or "")
        s = re.sub("<.*?>", "", s)
        return s.strip()

    def _norm(self, s: str) -> str:
        return re.sub(r"\W+", "", s or "").lower()

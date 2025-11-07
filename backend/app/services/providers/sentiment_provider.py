"""Sentiment provider with FinBERT and VADER fallback."""

from __future__ import annotations

from typing import Iterable
import os
from statistics import mean

FINBERT_MODEL = os.getenv("FINBERT_MODEL", "ProsusAI/finbert")


class SentimentProvider:
    def __init__(self):
        self._pipe = None
        self._vader = None

    def _ensure_finbert(self):
        if self._pipe is None:
            try:
                from transformers import pipeline

                self._pipe = pipeline(
                    "text-classification", model=FINBERT_MODEL, return_all_scores=True
                )
            except Exception:
                self._pipe = False  # mark unavailable

    def _ensure_vader(self):
        if self._vader is None:
            try:
                from nltk.sentiment import SentimentIntensityAnalyzer

                self._vader = SentimentIntensityAnalyzer()
            except Exception:
                self._vader = False

    def score_texts(self, texts: Iterable[str]) -> float:
        texts = [t for t in texts if t and t.strip()]
        if not texts:
            return 0.0

        self._ensure_finbert()
        if self._pipe:
            # FinBERT returns scores for labels: positive/negative/neutral
            scores = []
            batch = 16
            for i in range(0, len(texts), batch):
                out = self._pipe(texts[i : i + batch])
                for row in out:
                    d = {x["label"].lower(): x["score"] for x in row}
                    scores.append(d.get("positive", 0) - d.get("negative", 0))  # [-1, 1]
            return float(mean(scores))

        # fallback VADER
        self._ensure_vader()
        if self._vader:
            vals = [self._vader.polarity_scores(t)["compound"] for t in texts]
            return float(mean(vals))

        return 0.0

"""Sentiment scoring utilities for headlines.

Provides TextBlob-based sentiment and optional VADER fallback.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    _HAS_VADER = True
except Exception:
    _HAS_VADER = False

from textblob import TextBlob


def textblob_polarity(text: str) -> float:
    """Return TextBlob polarity score in [-1, 1]."""
    try:
        return float(TextBlob(str(text)).sentiment.polarity)
    except Exception:
        return 0.0


def vader_compound(text: str) -> float:
    """Return VADER compound score in [-1, 1], or raise if unavailable."""
    if not _HAS_VADER:
        raise RuntimeError("VADER not available in this environment")
    sia = SentimentIntensityAnalyzer()
    return float(sia.polarity_scores(str(text))["compound"])


def score_headlines(df: pd.DataFrame, headline_col: str = "headline", method: str = "textblob") -> pd.DataFrame:
    """Return DataFrame with a new `sentiment` column using the chosen method.

    method: 'textblob' or 'vader'
    """
    df = df.copy()
    if method == "vader":
        if not _HAS_VADER:
            raise RuntimeError("VADER not available; install NLTK and vader_lexicon")
        df["sentiment"] = df[headline_col].apply(vader_compound)
    else:
        df["sentiment"] = df[headline_col].apply(textblob_polarity)
    return df


def daily_average_sentiment(df: pd.DataFrame, date_col: str = "date", stock_col: str = "stock") -> pd.DataFrame:
    """Aggregate sentiment per stock per day (mean). Expects `sentiment` column present."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["date_only"] = df[date_col].dt.date
    grouped = df.groupby([stock_col, "date_only"]) ["sentiment"].mean().reset_index()
    grouped = grouped.rename(columns={"date_only": "date"})
    grouped["date"] = pd.to_datetime(grouped["date"])  # normalize to datetime
    return grouped


def daily_returns(df_prices: pd.DataFrame, date_col: str = "date", price_col: str = "adj_close") -> pd.DataFrame:
    """Compute daily percent returns per stock; expects columns `stock`, `date`, `adj_close` or `close`.

    Returns DataFrame with `stock`, `date`, `return`.
    """
    df = df_prices.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.sort_values(["stock", date_col])
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df["return"] = df.groupby("stock")[price_col].pct_change() * 100
    result = df[["stock", date_col, "return"]].dropna()
    result = result.rename(columns={date_col: "date"})
    result["date"] = pd.to_datetime(result["date"]).dt.date
    result["date"] = pd.to_datetime(result["date"])  # normalize
    return result


def pearson_correlation(sentiment_df: pd.DataFrame, returns_df: pd.DataFrame) -> float:
    """Compute Pearson correlation between daily sentiment and returns across aligned dates.

    Both inputs should have `stock` and `date` columns. Align on (stock,date) pairs.
    Returns overall Pearson r (float)."""
    s = sentiment_df.copy()
    r = returns_df.copy()
    # normalize date to dates
    s["date"] = pd.to_datetime(s["date"]).dt.date
    r["date"] = pd.to_datetime(r["date"]).dt.date
    merged = pd.merge(s, r, on=["stock", "date"] , how="inner")
    if merged.empty:
        return float('nan')
    return float(merged["sentiment"].corr(merged["return"]))

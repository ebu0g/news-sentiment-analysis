"""Reusable EDA helpers for financial news analysis."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def clean_headline(text: str) -> str:
    """Normalize a headline for lightweight text analysis."""
    value = str(text).lower()
    value = re.sub(r"[^a-z0-9\s]", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def add_headline_features(df: pd.DataFrame, headline_column: str = "headline") -> pd.DataFrame:
    """Return a copy with headline length and cleaned text columns."""
    result = df.copy()
    result["headline_length"] = result[headline_column].astype(str).str.len()
    result["headline_clean"] = result[headline_column].map(clean_headline)
    return result


def extract_domain(publisher: str) -> str | None:
    """Extract an email domain from a publisher string when present."""
    match = re.search(r"@([a-zA-Z0-9.-]+)", str(publisher))
    return match.group(1).lower() if match else None


def publication_counts_by_day(df: pd.DataFrame, date_column: str = "date") -> pd.Series:
    """Count articles by publication day."""
    dates = pd.to_datetime(df[date_column], errors="coerce")
    return dates.dt.date.value_counts().sort_index()


def publication_counts_by_hour(df: pd.DataFrame, date_column: str = "date") -> pd.Series:
    """Count articles by publication hour."""
    dates = pd.to_datetime(df[date_column], errors="coerce")
    return dates.dt.hour.value_counts().sort_index()


def top_keywords(
    headlines: Iterable[str],
    *,
    max_features: int = 20,
    ngram_range: tuple[int, int] = (1, 1),
    stop_words: str | None = "english",
) -> pd.Series:
    """Return the highest-scoring TF-IDF keywords as a Series."""
    vectorizer = TfidfVectorizer(max_features=max_features, stop_words=stop_words, ngram_range=ngram_range)
    matrix = vectorizer.fit_transform(list(headlines))
    scores = matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    series = pd.Series(scores, index=terms).sort_values(ascending=False)
    return series


def common_phrases(
    headlines: Iterable[str],
    *,
    max_features: int = 20,
    ngram_range: tuple[int, int] = (2, 2),
    stop_words: str | None = "english",
) -> pd.Series:
    """Return common phrases using count-based vectorization."""
    vectorizer = CountVectorizer(max_features=max_features, stop_words=stop_words, ngram_range=ngram_range)
    matrix = vectorizer.fit_transform(list(headlines))
    counts = matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    series = pd.Series(counts, index=terms).sort_values(ascending=False)
    return series
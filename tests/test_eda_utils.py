import pandas as pd

from src.eda_utils import (
    add_headline_features,
    clean_headline,
    common_phrases,
    extract_domain,
    publication_counts_by_day,
    publication_counts_by_hour,
    top_keywords,
)


def test_clean_headline_normalizes_text():
    assert clean_headline("Earnings Beat! AAPL jumps 5%") == "earnings beat aapl jumps 5"


def test_extract_domain_returns_email_domain():
    assert extract_domain("news@reuters.com") == "reuters.com"
    assert extract_domain("Reuters") is None


def test_add_headline_features_creates_expected_columns():
    df = pd.DataFrame({"headline": ["Stocks rise", "FDA approval"], "date": ["2026-05-01", "2026-05-02"]})
    result = add_headline_features(df)

    assert "headline_length" in result.columns
    assert "headline_clean" in result.columns
    assert result.loc[0, "headline_clean"] == "stocks rise"


def test_publication_counts_helpers_return_sorted_series():
    df = pd.DataFrame(
        {
            "date": ["2026-05-01 10:15", "2026-05-01 11:00", "2026-05-02 10:00"],
        }
    )

    day_counts = publication_counts_by_day(df)
    hour_counts = publication_counts_by_hour(df)

    assert day_counts.loc[pd.to_datetime("2026-05-01").date()] == 2
    assert day_counts.loc[pd.to_datetime("2026-05-02").date()] == 1
    assert hour_counts.loc[10] == 2
    assert hour_counts.loc[11] == 1


def test_text_vector_helpers_rank_terms():
    headlines = [
        "Apple earnings beat expectations",
        "Apple announces dividend",
        "FDA approval boosts biotech stocks",
    ]

    keywords = top_keywords(headlines, max_features=5)
    phrases = common_phrases(headlines, max_features=5)

    assert not keywords.empty
    assert not phrases.empty
    assert keywords.index[0] in {"apple", "earnings", "approval", "boosts", "biotech"}
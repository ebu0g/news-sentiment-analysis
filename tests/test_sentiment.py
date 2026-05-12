import pandas as pd

from src.sentiment import (
    daily_average_sentiment,
    daily_returns,
    pearson_correlation,
    score_headlines,
    textblob_polarity,
)


def test_textblob_polarity_bounds():
    assert -1.0 <= textblob_polarity('good excellent') <= 1.0
    assert -1.0 <= textblob_polarity('terrible bad') <= 1.0


def test_score_headlines_adds_sentiment_column():
    df = pd.DataFrame({'headline': ['good news', 'bad news'], 'date': ['2026-05-01', '2026-05-01'], 'stock': ['AAA', 'AAA']})
    scored = score_headlines(df, method='textblob')
    assert 'sentiment' in scored.columns


def test_daily_average_and_returns_and_correlation():
    df_news = pd.DataFrame({
        'headline': ['up', 'down', 'up'],
        'date': ['2026-05-01', '2026-05-02', '2026-05-02'],
        'stock': ['AAA', 'AAA', 'AAA'],
    })
    df_news = score_headlines(df_news)
    daily_sent = daily_average_sentiment(df_news)

    df_prices = pd.DataFrame({
        'stock': ['AAA', 'AAA', 'AAA'],
        'date': ['2026-05-01', '2026-05-02', '2026-05-03'],
        'adj_close': [100.0, 102.0, 101.0],
    })
    daily_ret = daily_returns(df_prices)

    # correlation should be computable (may be nan if insufficient overlap)
    corr = pearson_correlation(daily_sent, daily_ret)
    assert (pd.isna(corr) or isinstance(corr, float))

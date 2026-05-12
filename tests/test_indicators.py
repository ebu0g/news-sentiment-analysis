import pandas as pd

from src.indicators import ema, sma, rsi, macd


def make_series(values):
    return pd.Series(values, index=pd.date_range('2026-01-01', periods=len(values), freq='D'))


def test_sma_and_ema_agree_on_constant_series():
    s = make_series([1.0] * 20)
    assert sma(s, 5).iloc[-1] == 1.0
    assert ema(s, 5).iloc[-1] == 1.0


def test_rsi_on_gains_is_high():
    s = make_series(list(range(1, 21)))
    r = rsi(s, window=14)
    assert r.iloc[-1] > 70


def test_macd_structure_and_types():
    s = make_series([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    df = macd(s)
    assert set(df.columns) == {"macd", "signal", "hist"}
    assert not df.isnull().all().all()

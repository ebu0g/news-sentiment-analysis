"""Prepare dataset files for the analysis pipeline.

Moves the news CSV into `data/raw/financial_news.csv` and merges
per-ticker CSVs from `yfinance_data/Data/` into `data/raw/stock_prices.csv`.

Run from project root:
    python scripts/prepare_data.py
"""
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / 'data' / 'raw'
NEWS_SRC = ROOT / 'newsData' / 'raw_analyst_ratings.csv'
YFIN_DATA_DIR = ROOT / 'yfinance_data' / 'Data'


def ensure_dirs():
    DATA_RAW.mkdir(parents=True, exist_ok=True)


def move_news():
    if not NEWS_SRC.exists():
        print(f'News source not found: {NEWS_SRC} — skipping')
        return
    dst = DATA_RAW / 'financial_news.csv'
    # Copy to destination (do not remove original to be safe)
    print(f'Copying {NEWS_SRC} -> {dst}')
    df = pd.read_csv(NEWS_SRC)
    df.to_csv(dst, index=False)
    print(f'Wrote {len(df)} rows to {dst}')


def merge_stocks():
    if not YFIN_DATA_DIR.exists():
        print(f'YFinance data dir not found: {YFIN_DATA_DIR} — skipping')
        return
    files = sorted([p for p in YFIN_DATA_DIR.glob('*.csv') if not p.name.startswith('._')])
    if not files:
        print('No stock CSVs found — skipping')
        return
    out_rows = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception as e:
            print(f'Failed reading {p}: {e} — skipping')
            continue
        # Normalize column names
        df.columns = [c.strip() for c in df.columns]
        # Ensure Date column exists
        if 'Date' not in df.columns and 'date' not in df.columns:
            print(f'{p} missing Date column — skipping')
            continue
        # Add stock column from filename
        symbol = p.stem.upper()
        df['stock'] = symbol
        out_rows.append(df)
        print(f'Queued {len(df)} rows from {p.name} (stock={symbol})')

    if not out_rows:
        print('No valid stock data to write')
        return
    big = pd.concat(out_rows, ignore_index=True, sort=False)
    # Normalize date column name to 'date' and lower-case column names
    if 'Date' in big.columns:
        big = big.rename(columns={'Date': 'date'})
    big.columns = [c.lower() for c in big.columns]
    out_path = DATA_RAW / 'stock_prices.csv'
    # Keep common columns (date, open, high, low, close, volume, stock)
    cols = [c for c in ['date', 'open', 'high', 'low', 'close', 'volume', 'stock'] if c in big.columns]
    big.to_csv(out_path, index=False, columns=cols)
    print(f'Wrote {len(big)} total rows to {out_path}')


def clean_macos_artifacts():
    macos_dir = ROOT / 'yfinance_data' / '__MACOSX'
    if macos_dir.exists():
        print(f'Removing macOS artifact folder: {macos_dir}')
        try:
            import shutil

            shutil.rmtree(macos_dir)
            print('Removed macOS artifacts')
        except Exception as e:
            print(f'Failed to remove {macos_dir}: {e}')


def main():
    ensure_dirs()
    move_news()
    merge_stocks()
    clean_macos_artifacts()


if __name__ == '__main__':
    main()

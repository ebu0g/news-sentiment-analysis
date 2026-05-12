"""
Data loading utilities for the news sentiment analysis project.

Use these functions to load and validate your financial news and stock price data.
"""

import pandas as pd
from pathlib import Path


def load_news_data(filepath: str) -> pd.DataFrame:
    """
    Load financial news dataset.
    
    Expected columns: headline, url, publisher, date, stock
    
    Args:
        filepath: Path to news CSV file
        
    Returns:
        DataFrame with news data
        
    Example:
        df_news = load_news_data('data/raw/financial_news.csv')
    """
    df = pd.read_csv(filepath)
    
    # Validate required columns
    required_cols = ['headline', 'publisher', 'date', 'stock']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Add derived columns
    df['headline_length'] = df['headline'].str.len()
    
    print(f"✓ Loaded {len(df)} articles")
    print(f"✓ Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"✓ Unique publishers: {df['publisher'].nunique()}")
    print(f"✓ Unique stocks: {df['stock'].nunique()}")
    
    return df


def load_stock_prices(filepath: str) -> pd.DataFrame:
    """
    Load historical stock price dataset.
    
    Expected columns: Date, Open, High, Low, Close, Adj Close, Volume
    (or lowercase equivalents)
    
    Args:
        filepath: Path to stock price CSV file
        
    Returns:
        DataFrame with stock price data
        
    Example:
        df_stocks = load_stock_prices('data/raw/stock_prices.csv')
    """
    df = pd.read_csv(filepath)
    
    # Normalize column names to lowercase
    df.columns = df.columns.str.lower()
    
    # Validate required columns
    required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Ensure numeric columns
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    print(f"✓ Loaded {len(df)} trading days")
    print(f"✓ Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"✓ Price range: ${df['close'].min():.2f} to ${df['close'].max():.2f}")
    
    return df


# Example usage (uncomment and modify paths to test)
# if __name__ == '__main__':
#     df_news = load_news_data('data/raw/financial_news.csv')
#     df_stocks = load_stock_prices('data/raw/stock_prices.csv')
#     print("\n✅ Data loaded successfully!")

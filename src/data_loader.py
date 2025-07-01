import yfinance as yf
from fredapi import Fred
import pandas as pd

def load_yahoo_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    try:
        print(f" Downloading Yahoo data for {ticker}...")
        df = yf.download(ticker, start=start_date, end=end_date)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f" Error fetching Yahoo data: {e}")
        return pd.DataFrame()

def load_fred_data(series_id: str, api_key: str) -> pd.Series:
    try:
        print(f" Fetching FRED data for series: {series_id}...")
        fred = Fred(api_key=api_key)
        series = fred.get_series(series_id)
        series.name = series_id
        return series
    except Exception as e:
        print(f" Error fetching FRED data: {e}")
        return pd.Series(dtype='float64')

def load_housing_data_from_csv(path: str) -> pd.DataFrame:
    try:
        print(f" Loading housing data from: {path}")
        df = pd.read_csv(path)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f" Error loading housing CSV: {e}")
        return pd.DataFrame()

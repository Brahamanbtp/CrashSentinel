import pandas as pd
from fredapi import Fred
import os

# Load your FRED API key from environment variable
FRED_API_KEY = os.getenv("FRED_API_KEY")

if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY not found. Please set it as an environment variable.")

fred = Fred(api_key=FRED_API_KEY)

# Dictionary of indicator codes and their descriptions
INDICATORS = {
    "MEHOINUSA672N": "Median Household Income (USD)",
    "CPIAUCSL": "Consumer Price Index (CPI)",
    "UNRATE": "Unemployment Rate (%)",
    "FEDFUNDS": "Federal Funds Rate (%)",
    "GDPC1": "Real GDP (Billions, Chained 2012 USD)"
}

def fetch_fred_data(indicators=INDICATORS, start_date="2010-01-01", end_date=None) -> pd.DataFrame:
    """
    Fetch multiple economic indicators from FRED and return as a merged DataFrame.
    """
    print(" Fetching FRED economic indicators...")
    data_frames = []

    for code, desc in indicators.items():
        print(f"  • {desc} ({code})")
        series = fred.get_series(code, observation_start=start_date, observation_end=end_date)
        df = series.to_frame(name=desc)
        df.index.name = "Date"
        data_frames.append(df)

    # Merge all time series on date
    df_merged = pd.concat(data_frames, axis=1)
    return df_merged


if __name__ == "__main__":
    # Test run (for CLI)
    df = fetch_fred_data()
    print(df.tail())
    df.to_csv("../../data/fred_indicators.csv")

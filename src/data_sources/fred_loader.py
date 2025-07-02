import os
import pandas as pd
from fredapi import Fred
import requests
from dotenv import load_dotenv

# --- Load environment variables from .env file ---
load_dotenv()

# --- Fetch API Key ---
FRED_API_KEY = os.getenv("FRED_API_KEY")
if not FRED_API_KEY:
    raise ValueError(" FRED_API_KEY not found. Please set it in a .env file or as an environment variable.")

# --- Initialize FRED client ---
fred = Fred(api_key=FRED_API_KEY)

# --- Indicator dictionary ---
INDICATORS = {
    "MEHOINUSA672N": "Median Household Income (USD)",
    "CPIAUCSL": "Consumer Price Index (CPI)",
    "UNRATE": "Unemployment Rate (%)",
    "FEDFUNDS": "Federal Funds Rate (%)",
    "GDPC1": "Real GDP (Billions, Chained 2012 USD)"
}

# --- Fetch main FRED indicator time series ---
def fetch_fred_data(indicators=INDICATORS, start_date="2010-01-01", end_date=None) -> pd.DataFrame:
    print(" Fetching FRED economic indicators...")
    data_frames = []

    for code, desc in indicators.items():
        print(f"  • {desc} ({code})")
        series = fred.get_series(code, observation_start=start_date, observation_end=end_date)
        df = series.to_frame(name=desc)
        df.index.name = "Date"
        data_frames.append(df)

    df_merged = pd.concat(data_frames, axis=1)
    return df_merged

# --- Search for series by keyword ---
def search_series_by_keyword(keyword: str, limit=10) -> pd.DataFrame:
    print(f" Searching FRED for keyword: '{keyword}'")
    results = fred.search(keyword, limit=limit)
    return results[['id', 'title']]

# --- Get series in a given category ---
def get_series_by_category(category_id: int) -> pd.DataFrame:
    print(f" Getting series from category ID: {category_id}")
    df = fred.get_series_in_category(category_id)
    return df[['id', 'title']]

# --- Get release dates for a series ---
def get_series_release_dates(series_id: str) -> pd.DataFrame:
    print(f" Fetching release dates for series: {series_id}")
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise Exception(f"Failed to fetch observations: {r.status_code}")
    obs = r.json()["observations"]
    return pd.DataFrame(obs)

# --- CLI Test Runner ---
if __name__ == "__main__":
    df = fetch_fred_data()
    print(df.tail())
    os.makedirs("../../data", exist_ok=True)
    df.to_csv("../../data/fred_indicators.csv")

import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Quandl API key
QUANDL_API_KEY = os.getenv("QUANDL_API_KEY")

if not QUANDL_API_KEY:
    raise EnvironmentError("QUANDL_API_KEY not found. Please set it in a .env file or environment variable.")

# Base URL for Quandl API
QUANDL_BASE_URL = "https://www.quandl.com/api/v3/datasets"

# Common economic indicators from different datasets (e.g., WIKI is deprecated; use newer sources like FRED via Quandl)
QUANDL_INDICATORS = {
    "FRED/DEXUSEU": "USD to Euro Exchange Rate",
    "FRED/DTB3": "3-Month Treasury Bill: Secondary Market Rate",
    "FRED/GS10": "10-Year Treasury Constant Maturity Rate",
    "FRED/CPILFESL": "CPI: All Items Less Food & Energy",
    "FRED/M2SL": "M2 Money Stock"
}

def fetch_quandl_data(indicators=QUANDL_INDICATORS, start_date="2010-01-01", end_date=None) -> pd.DataFrame:
    """
    Fetch multiple economic indicators from Quandl and return as a merged DataFrame.
    """
    print("\✨ Fetching Quandl economic indicators...")
    dfs = []

    for code, desc in indicators.items():
        print(f"  • {desc} ({code})")
        url = f"{QUANDL_BASE_URL}/{code}.json"
        params = {
            "api_key": QUANDL_API_KEY,
            "start_date": start_date
        }
        if end_date:
            params["end_date"] = end_date

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"   Failed to fetch {code}: {response.status_code} - {response.text}")
            continue

        data_json = response.json()
        dataset = data_json["dataset"]
        df = pd.DataFrame(dataset["data"], columns=["Date", desc])
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        dfs.append(df)

    if not dfs:
        raise ValueError("No data fetched from Quandl.")

    df_merged = pd.concat(dfs, axis=1).sort_index()
    return df_merged


# CLI test
if __name__ == "__main__":
    df = fetch_quandl_data()
    print(df.tail())
    output_path = "../../data/quandl_indicators.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print(f"\n Saved to {output_path}")

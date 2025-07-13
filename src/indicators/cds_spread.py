import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve FRED API key
FRED_API_KEY = os.getenv("FRED_API_KEY")
if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY not found. Please set it in a .env file or environment variable.")

# Initialize FRED instance
fred = Fred(api_key=FRED_API_KEY)

# Dictionary of CDS indicators (you can expand this list)
CDS_INDICATORS = {
    "CDSDB6M": "CDS Spread - Deutsche Bank (6M, bps)",
    "CDSDB1Y": "CDS Spread - Deutsche Bank (1Y, bps)",
    "CDSCS1Y": "CDS Spread - Credit Suisse (1Y, bps)",
    "CDSCS5Y": "CDS Spread - Credit Suisse (5Y, bps)",
    "CDSITA5YUKD": "CDS Spread - Italy Sovereign (5Y, bps)",
}

def fetch_cds_spreads(indicators=CDS_INDICATORS, start_date="2010-01-01", end_date=None) -> pd.DataFrame:
    """
    Fetch CDS spreads from FRED API and return a merged DataFrame.
    """
    print(" Fetching CDS Spreads from FRED...")
    dfs = []

    for code, desc in indicators.items():
        print(f"  • {desc} ({code})")
        series = fred.get_series(code, observation_start=start_date, observation_end=end_date)
        df = series.to_frame(name=desc)
        df.index.name = "Date"
        dfs.append(df)

    merged_df = pd.concat(dfs, axis=1).sort_index()
    return merged_df


if __name__ == "__main__":
    df = fetch_cds_spreads()
    print(df.tail())

    os.makedirs("../../data", exist_ok=True)
    df.to_csv("../../data/cds_spreads.csv")

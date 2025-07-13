import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load FRED API key
FRED_API_KEY = os.getenv("FRED_API_KEY")
if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY not found. Please set it in a .env file.")

# Initialize FRED API client
fred = Fred(api_key=FRED_API_KEY)

# FRED series IDs
MEDIAN_INCOME_SERIES = "MEHOINUSA672N"  # Median Household Income in the U.S.
MEDIAN_HOME_PRICE_SERIES = "MSPUS"      # Median Sales Price of Houses Sold in the U.S.

def fetch_price_to_income_ratio(start_date="2000-01-01", end_date=None) -> pd.DataFrame:
    """
    Fetches median income and home prices and calculates the price-to-income ratio.
    Returns a DataFrame with all three series.
    """
    print(" Fetching Median Household Income...")
    income_series = fred.get_series(MEDIAN_INCOME_SERIES, observation_start=start_date, observation_end=end_date)
    income_df = income_series.to_frame(name="Median Household Income")
    income_df.index.name = "Date"

    print(" Fetching Median Home Prices...")
    price_series = fred.get_series(MEDIAN_HOME_PRICE_SERIES, observation_start=start_date, observation_end=end_date)
    price_df = price_series.to_frame(name="Median Home Price")
    price_df.index.name = "Date"

    # Merge on date index (FRED may use quarterly/monthly data, so allow outer join)
    df = pd.merge(price_df, income_df, left_index=True, right_index=True, how="outer").sort_index()

    # Compute Price-to-Income Ratio
    df["Price-to-Income Ratio"] = df["Median Home Price"] / df["Median Household Income"]

    return df


if __name__ == "__main__":
    df = fetch_price_to_income_ratio(start_date="2000-01-01")
    print(df.tail())
    
    # Save output
    os.makedirs("../../data", exist_ok=True)
    df.to_csv("../../data/price_to_income_ratio.csv")

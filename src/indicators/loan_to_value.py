import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get FRED API Key
FRED_API_KEY = os.getenv("FRED_API_KEY")
if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY not found. Please set it in a .env file.")

# Initialize FRED
fred = Fred(api_key=FRED_API_KEY)

# FRED Series IDs
# Mortgage Debt Outstanding for Households and Nonprofit Organizations
MORTGAGE_DEBT_SERIES = "HHMSDODNS"  # or "MDOTHNWMVBSN"
# Median Home Price
HOME_PRICE_SERIES = "MSPUS"         # Median Sales Price of Houses Sold in the U.S.

def fetch_loan_to_value_ratio(start_date="2000-01-01", end_date=None) -> pd.DataFrame:
    """
    Fetches mortgage debt and home price series from FRED and computes Loan-to-Value Ratio.
    LTV = Mortgage Debt / Median Home Price
    """
    print(" Fetching Mortgage Debt Outstanding...")
    debt_series = fred.get_series(MORTGAGE_DEBT_SERIES, observation_start=start_date, observation_end=end_date)
    debt_df = debt_series.to_frame(name="Mortgage Debt")
    debt_df.index.name = "Date"

    print(" Fetching Median Home Prices...")
    price_series = fred.get_series(HOME_PRICE_SERIES, observation_start=start_date, observation_end=end_date)
    price_df = price_series.to_frame(name="Median Home Price")
    price_df.index.name = "Date"

    # Merge on index (Date)
    df = pd.merge(debt_df, price_df, left_index=True, right_index=True, how="outer").sort_index()

    # Compute Loan-to-Value Ratio
    df["Loan-to-Value Ratio"] = df["Mortgage Debt"] / df["Median Home Price"]

    return df


if __name__ == "__main__":
    df = fetch_loan_to_value_ratio(start_date="2000-01-01")
    print(df.tail())

    os.makedirs("../../data", exist_ok=True)
    df.to_csv("../../data/loan_to_value_ratio.csv")

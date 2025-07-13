import os
import sys
import json
import pandas as pd
from pathlib import Path

# Add src path
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

# Local Imports
from data_loader import load_yahoo_data
from feature_engineering import volatility_index
from anomaly_detection import train_isolation_forest, append_anomaly_column
from time_series_model import forecast_with_prophet
from visualization import plot_anomalies

# Extended Modules
from data_sources.fred_loader import fetch_fred_data
from data_sources.zillow_loader import fetch_zillow_listings
from data_sources.reddit_scraper import fetch_reddit_sentiment
from data_sources.sec_scraper import download_sec_filings
from indicators.risk_score import compute_risk_index
from visualization import plot_risk_index

# --- Output Paths ---
data_dir = BASE_DIR / "data"
reports_dir = BASE_DIR / "reports"
models_dir = BASE_DIR / "models"

os.makedirs(data_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)
os.makedirs(models_dir, exist_ok=True)

# --- Step 1: Load Financial Market Data ---
print("\n[1] Loading S&P 500 historical data...")
sp500 = load_yahoo_data("^GSPC", "2015-01-01", "2023-12-31")
sp500.columns = [col[0] for col in sp500.columns] if isinstance(sp500.columns, pd.MultiIndex) else sp500.columns
sp500.to_csv(data_dir / "sp500_data.csv")

# --- Step 2: Feature Engineering ---
print("\n[2] Calculating volatility index...")
sp500['Volatility'] = volatility_index(sp500['Close'])
sp500_clean = sp500.dropna(subset=['Volatility'])

# --- Step 3: Anomaly Detection ---
print("\n[3] Detecting anomalies using Isolation Forest...")
model = train_isolation_forest(sp500_clean[['Volatility']])
sp500_anomalies = append_anomaly_column(sp500_clean, model, ['Volatility'])
sp500_anomalies.to_csv(data_dir / "sp500_anomalies.csv")

# --- Step 4: Forecasting ---
print("\n[4] Forecasting future volatility using Prophet...")
forecast_df = forecast_with_prophet(sp500['Close'], periods=90)
forecast_df.to_csv(data_dir / "sp500_forecast.csv", index=False)

# --- Step 5: Additional Economic Data Sources ---
print("\n[5] Fetching FRED economic indicators...")
fred_df = fetch_fred_data()
fred_df.to_csv(data_dir / "fred_indicators.csv")

print("\n[6] Fetching Zillow housing data...")
zillow_df = fetch_zillow_listings(zipcode="90210", limit=10)
zillow_df.to_csv(data_dir / "zillow_listings.csv", index=False)

print("\n[7] Fetching Reddit sentiment data...")
reddit_data = fetch_reddit_sentiment(subreddits=["stocks", "investing"], limit=100)
with open(data_dir / "reddit_sentiment.json", "w") as f:
    json.dump(reddit_data, f)

print("\n[8] Downloading SEC Filings (AAPL)...")
download_sec_filings("AAPL", "10-K", output_dir=data_dir / "sec_filings")

# --- Step 6: Risk Score Computation ---
print("\n[9] Calculating Market Risk Index...")
risk_index = compute_risk_index(sp500, fred_df, zillow_df)
risk_index.to_csv(data_dir / "market_risk_score.csv")

# --- Step 7: Visualization ---
print("\n[10] Plotting results...")
plot_anomalies(sp500_anomalies, 'Volatility', 'anomaly', save_path=reports_dir / "volatility_anomalies.png")
plot_risk_index(risk_index, save_path=reports_dir / "market_risk_index.png")

print("\n All pipeline steps completed.")

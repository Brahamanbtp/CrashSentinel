import sys
import pandas as pd

# Add src path
sys.path.append('/content/CrashSentinel/src')

from data_loader import load_yahoo_data
from feature_engineering import volatility_index
from anomaly_detection import train_isolation_forest, append_anomaly_column
from time_series_model import forecast_with_prophet
from visualization import plot_anomalies

# Step 1: Load Data
print(" Loading S&P 500 data...")
sp500 = load_yahoo_data("^GSPC", "2015-01-01", "2023-12-31")
sp500.columns = [col[0] for col in sp500.columns] if isinstance(sp500.columns, pd.MultiIndex) else sp500.columns

# Step 2: Engineer Features
print(" Calculating volatility...")
sp500['Volatility'] = volatility_index(sp500['Close'])
sp500_clean = sp500.dropna(subset=['Volatility'])

# Step 3: Anomaly Detection
print(" Training anomaly detector...")
model = train_isolation_forest(sp500_clean[['Volatility']])
sp500_with_anomaly = append_anomaly_column(sp500_clean, model, ['Volatility'])

# Step 4: Forecasting
print(" Running forecast with Prophet...")
forecast_df = forecast_with_prophet(sp500['Close'], periods=90)

# Step 5: Visualization
print(" Plotting results...")
plot_anomalies(sp500_with_anomaly, 'Volatility', 'anomaly')


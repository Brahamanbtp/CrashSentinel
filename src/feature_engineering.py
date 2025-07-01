import pandas as pd
import numpy as np

# Calculate Price-to-Income Ratio
def price_to_income_ratio(house_prices: pd.Series, income_levels: pd.Series) -> pd.Series:
    """
    Estimate housing affordability.
    """
    return house_prices / income_levels

# Calculate Loan-to-Value Ratio
def loan_to_value_ratio(total_loans: pd.Series, total_property_value: pd.Series) -> pd.Series:
    """
    Indicates leverage in housing/real estate.
    """
    return total_loans / total_property_value

# Calculate Volatility Index using rolling standard deviation
def volatility_index(prices: pd.Series, window: int = 30) -> pd.Series:
    """
    Measures market uncertainty using return volatility.
    """
    returns = prices.pct_change()
    return returns.rolling(window).std() * np.sqrt(window)

# Moving Average Feature
def moving_average(prices: pd.Series, window: int = 20) -> pd.Series:
    """
    Simple moving average to detect trend shifts.
    """
    return prices.rolling(window).mean()

# Z-score Calculation
def z_score(series: pd.Series, window: int = 30) -> pd.Series:
    """
    Standardized anomaly detector using Z-score.
    """
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

# Rolling Correlation
def rolling_correlation(series1: pd.Series, series2: pd.Series, window: int = 30) -> pd.Series:
    """
    Measures relationship between two time-series over time.
    """
    return series1.rolling(window).corr(series2)
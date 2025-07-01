import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Prepare data for Prophet model
def prepare_prophet_data(series: pd.Series) -> pd.DataFrame:
    """
    Converts a time series into Prophet-compatible format.

    Args:
        series (pd.Series): Series with DateTime index

    Returns:
        pd.DataFrame: DataFrame with 'ds' and 'y' columns
    """
    df = series.reset_index()
    df.columns = ['ds', 'y']
    df = df[['ds', 'y']].dropna()
    df['ds'] = pd.to_datetime(df['ds'])
    return df

# Train and forecast using Prophet
def forecast_with_prophet(series: pd.Series, periods: int = 90, freq: str = 'D') -> pd.DataFrame:
    """
    Forecasts future values using Facebook Prophet.

    Args:
        series (pd.Series): Time series to forecast
        periods (int): Number of future periods to forecast
        freq (str): Frequency (e.g. 'D' for daily)

    Returns:
        pd.DataFrame: Forecast including yhat, yhat_lower, yhat_upper
    """
    df = prepare_prophet_data(series)
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)
    return forecast

# Plot forecast
def plot_prophet_forecast(forecast: pd.DataFrame, title: str = "Prophet Forecast") -> None:
    """
    Plots the forecast output from Prophet.

    Args:
        forecast (pd.DataFrame): Prophet forecast output
        title (str): Title of the plot
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecast['ds'], forecast['yhat'], label='Prediction', color='blue')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='skyblue', alpha=0.3, label='Confidence Interval')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Forecasted Value')
    ax.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

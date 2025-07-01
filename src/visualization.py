import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go

# Line chart for time series data
def plot_market_index(df: pd.DataFrame, column: str = 'Close', title: str = "Market Index Over Time"):
    """
    Plots a simple time-series line chart.

    Args:
        df (pd.DataFrame): DataFrame with DateTime index
        column (str): Column to plot
        title (str): Chart title
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[column], label=column, color='blue')
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Heatmap of risk scores
def heatmap_of_risks(risk_df: pd.DataFrame, title: str = "Market Risk Heatmap"):
    """
    Displays a heatmap of risk scores.

    Args:
        risk_df (pd.DataFrame): DataFrame of risk indicators
        title (str): Title for the heatmap
    """
    plt.figure(figsize=(10, 6))
    sns.heatmap(risk_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(title)
    plt.tight_layout()
    plt.show()

# Sentiment trend over time
def show_sentiment_trends(df: pd.DataFrame, sentiment_col: str = 'sentiment_score'):
    """
    Plot sentiment score trend line.

    Args:
        df (pd.DataFrame): DataFrame with DateTime index
        sentiment_col (str): Column with sentiment scores
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[sentiment_col], color='purple', label='Sentiment')
    plt.title(" Sentiment Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Anomaly visualization
def plot_anomalies(df: pd.DataFrame, value_col: str, anomaly_col: str, title: str = "Anomalies Detected"):
    """
    Plots time series data with anomaly markers.

    Args:
        df (pd.DataFrame): DataFrame with values and anomaly flags
        value_col (str): Column name for values
        anomaly_col (str): Column name with anomaly (-1/1)
        title (str): Title of the plot
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[value_col], label=value_col, color='blue')
    plt.scatter(df[df[anomaly_col] == -1].index,
                df[df[anomaly_col] == -1][value_col],
                color='red', label='Anomaly', marker='x')
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(value_col)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Interactive plot (optional)
def plotly_market_index(df: pd.DataFrame, column: str = 'Close', title: str = " Interactive Market Chart"):
    """
    Uses Plotly to plot interactive line chart.

    Args:
        df (pd.DataFrame): DataFrame with DateTime index
        column (str): Column to visualize
        title (str): Title of chart
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title=column, template='plotly_white')
    fig.show()

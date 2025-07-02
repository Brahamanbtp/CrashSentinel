import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

#  Adjust path to include /src for local execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from data_loader import load_yahoo_data
from feature_engineering import volatility_index
from anomaly_detection import train_isolation_forest, append_anomaly_column
from time_series_model import forecast_with_prophet

# --- Page Config ---
st.set_page_config(page_title="CrashSentinel Dashboard", layout="wide")
st.title(" CrashSentinel: Market Risk Monitoring Dashboard")

# --- Sidebar Filters ---
st.sidebar.markdown("###  Data Controls")
ticker = st.sidebar.text_input(" Ticker Symbol", value="^GSPC")
start_date = st.sidebar.date_input(" Start Date", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input(" End Date", pd.to_datetime("2023-12-31"))
st.sidebar.markdown("---")

# --- Load Data ---
st.info(f"Downloading Yahoo data for `{ticker}`...")
data = load_yahoo_data(ticker, str(start_date), str(end_date))
data.columns = [col[0] for col in data.columns] if isinstance(data.columns, pd.MultiIndex) else data.columns

# --- Tabs for Sections ---
tab1, tab2, tab3 = st.tabs([" Price & Volatility", " Anomaly Detection", " Forecasting"])

with tab1:
    st.subheader(" Price Chart")
    st.line_chart(data['Close'], use_container_width=True)

    st.subheader(" Volatility Index")
    data['Volatility'] = volatility_index(data['Close'])
    st.line_chart(data['Volatility'])

with tab2:
    st.subheader(" Detected Volatility Anomalies")
    data_clean = data.dropna(subset=['Volatility'])
    model = train_isolation_forest(data_clean[['Volatility']])
    data_anomalies = append_anomaly_column(data_clean.copy(), model, ['Volatility'])

    fig = px.scatter(
        data_anomalies.reset_index(), x='Date', y='Volatility',
        color=data_anomalies['anomaly'].map({1: "Normal", -1: "Anomaly"}),
        title="Detected Volatility Anomalies",
        color_discrete_map={"Normal": "blue", "Anomaly": "red"}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader(" Crash Forecast with Prophet")
    forecast = forecast_with_prophet(data['Close'], periods=90)
    fig2 = px.line(forecast, x='ds', y='yhat', title="Forecasted Closing Prices")
    st.plotly_chart(fig2, use_container_width=True)

# --- Footer ---
st.markdown("""
<hr style='border: 1px solid #ccc;' />
<div style='text-align: center'>
    Built with ❤️ by <strong>CrashSentinel</strong> | Powered by <em>Streamlit</em>, <em>Prophet</em> & <em>Scikit-Learn</em>
</div>
""", unsafe_allow_html=True)

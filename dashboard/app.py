import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from io import BytesIO
from datetime import datetime
from fpdf import FPDF

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from data_loader import load_yahoo_data
from feature_engineering import volatility_index
from anomaly_detection import train_isolation_forest, append_anomaly_column
from time_series_model import forecast_with_prophet
from data_sources.fred_loader import fetch_fred_data
from indicators.risk_score import compute_risk_index

# --- Page Config ---
st.set_page_config(page_title="CrashSentinel Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Header ---
st.markdown("<h1 style='text-align: center;'>📉 CrashSentinel Dashboard</h1>", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("⚙️ Settings")
ticker = st.sidebar.text_input("Ticker Symbol", "^GSPC")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))
forecast_days = st.sidebar.slider("Forecast Days (Prophet)", 30, 180, 90)
theme = st.sidebar.selectbox("Theme", ["light", "dark"])
st.sidebar.markdown("---")
st.sidebar.caption("📊 Powered by Yahoo Finance + FRED")

# --- Apply Theme ---
def apply_theme():
    if theme == "dark":
        st.markdown("""
            <style>
                body { background-color: #0e1117; color: #f1f1f1; }
            </style>
        """, unsafe_allow_html=True)

apply_theme()

# --- Load Data ---
st.info(f"📥 Downloading data for `{ticker}`...")
try:
    data = load_yahoo_data(ticker, str(start_date), str(end_date))
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
except Exception as e:
    st.error(f"❌ Data loading failed: {e}")
    st.stop()

data['Volatility'] = volatility_index(data['Close'])
data_clean = data.dropna(subset=['Volatility'])

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Price & Volatility", "🚨 Anomaly Detection", "🔮 Forecasting", "📉 Risk Score", "📤 Export"
])

# --- Tab 1: Price & Volatility ---
with tab1:
    st.subheader("Closing Price")
    st.line_chart(data['Close'], use_container_width=True)

    st.subheader("Volatility Index")
    st.line_chart(data['Volatility'], use_container_width=True)

# --- Tab 2: Anomaly Detection ---
with tab2:
    st.subheader("Detected Volatility Anomalies")
    try:
        model = train_isolation_forest(data_clean[['Volatility']])
        data_anomalies = append_anomaly_column(data_clean.copy(), model, ['Volatility'])

        fig = px.scatter(
            data_anomalies.reset_index(),
            x='Date', y='Volatility',
            color=data_anomalies['anomaly'].map({1: "Normal", -1: "Anomaly"}),
            title="Volatility Anomalies",
            color_discrete_map={"Normal": "blue", "Anomaly": "red"}
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Anomaly detection failed: {e}")

# --- Tab 3: Forecasting ---
with tab3:
    st.subheader("Crash Forecast with Prophet")
    try:
        forecast = forecast_with_prophet(data['Close'], periods=forecast_days)
        fig = px.line(forecast, x='ds', y='yhat', title=f"{forecast_days}-Day Forecast")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Forecasting failed: {e}")

# --- Tab 4: Risk Score ---
with tab4:
    st.subheader("📉 Market Risk Index")
    try:
        fred_data = fetch_fred_data()
        risk_index = compute_risk_index(data, fred_data, pd.DataFrame())
        st.line_chart(risk_index['Risk Score'], use_container_width=True)
    except Exception as e:
        st.error(f"❌ Risk score computation failed: {e}")

# --- Tab 5: Export Options ---
with tab5:
    st.subheader("📤 Export Data")

    # CSV Download
    csv = data.to_csv(index=True).encode('utf-8')
    st.download_button("Download CSV", csv, "market_data.csv", "text/csv")

    # PDF Export
    def create_pdf(df: pd.DataFrame) -> BytesIO:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="CrashSentinel Market Report", ln=True, align='C')
        pdf.ln(10)
        for i, row in df.tail(20).iterrows():
            pdf.cell(200, 6, txt=f"{i.date()} | Close: {row['Close']:.2f} | Vol: {row['Volatility']:.4f}", ln=True)
        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

    pdf_buffer = create_pdf(data)
    st.download_button("Download PDF", pdf_buffer, "market_report.pdf", mime="application/pdf")

# --- Footer ---
st.markdown("""
<hr />
<div style='text-align: center; font-size: 14px;'>
    🚨 Built with ❤️ by <b>CrashSentinel</b> | Streamlit ⚙️ Prophet 🔮 Plotly 📊
</div>
""", unsafe_allow_html=True)

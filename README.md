
# 📉 CrashSentinel

> 🔮 **CrashSentinel** is an AI-powered early warning system that predicts market crashes or instability by analyzing financial, housing, credit, and investor sentiment data. It combines real-time anomaly detection, time-series forecasting, and risk scoring with an interactive dashboard built in Streamlit.

---

## 🎯 Project Goal

Build a system that issues **advance alerts of market instability** using signals from:

- 📉 Financial markets (S&P 500, Volatility)
- 🏘️ Housing data (Price-to-Income, LTV)
- 💳 Credit stress indicators (CDS spreads)
- 🧠 Sentiment from Reddit/Twitter
- 🏦 Regulatory disclosures (SEC 10-K)

---

## ✅ Phases & Workflow

### Phase 1: Data Collection & EDA (Google Colab)
- ✅ Sources: `FRED`, `Yahoo Finance`, `Zillow`, `Quandl`, `Reddit`, `Twitter`, `NewsAPI`, `SEC Filings`
- 🔧 Features engineered:
  - Price-to-Income Ratio
  - Loan-to-Value Ratio (LTV)
  - CDS Spread Indicators
  - Reddit Sentiment Score
  - Volatility Index

### Phase 2: Modeling
- 🚨 Anomaly Detection: Isolation Forest, One-Class SVM
- 🔮 Forecasting: Prophet, ARIMA, LSTM (future)
- 🧮 Risk Scoring: Composite index combining engineered signals (0–100)
- 📚 (Optional) Explainability: SHAP values, scenario simulation

### Phase 3: Visualization
- 📊 Plotly, Matplotlib, Seaborn for:
  - Time trends
  - Heatmaps
  - Risk progression

### Phase 4: Dashboard (VS Code + Streamlit)
- 🎛 Interactive features:
  - Market Stability Index
  - Top Risk Contributors
  - Downloadable Reports (CSV, PDF)
  - Light/Dark Theme
  - Optional Alerts (email, Telegram)

---

## 🧱 Core System Components

| Layer               | Tools & Techniques                             |
|--------------------|-------------------------------------------------|
| **Data Collection** | `fredapi`, `yfinance`, Zillow API, Quandl, PRAW |
| **Sentiment**       | `Reddit`, `Twitter` (via snscrape)             |
| **Feature Engine**  | Volatility, LTV, P/I Ratio, CDS spreads        |
| **Modeling**        | Prophet, Isolation Forest, SHAP                |
| **Visualization**   | Streamlit, Plotly, Matplotlib                  |
| **Alerting**        | PDF reports, risk score threshold triggers     |

---

## 📁 Project Structure

```
CrashSentinel/
├── data/
│   └── sec_filings/
├── notebooks/
│   └── 01_data_collection_eda.ipynb
├── src/
│   ├── data_loader.py
│   ├── anomaly_detection.py
│   ├── feature_engineering.py
│   ├── time_series_model.py
│   ├── visualization.py
│   ├── data_sources/
│   │   ├── fred_loader.py
│   │   ├── zillow_loader.py
│   │   ├── quandl_loader.py
│   │   ├── reddit_scraper.py
│   │   ├── twitter_scraper.py
│   │   └── sec_scraper.py
│   ├── indicators/
│   │   ├── risk_score.py
│   │   ├── price_to_income.py
│   │   ├── loan_to_value.py
│   │   └── cds_spread.py
├── models/
│   └── prophet_model.json
│   └── anomaly_model.pkl
├── dashboard/
│   └── app.py
├── reports/
│   └── summary_report.pdf
├── .env
├── requirements.txt
├── README.md
└── main.py
```


## ▶️ Quickstart

### 🔁 Clone the Repo

```bash
git clone https://github.com/your-username/CrashSentinel.git
cd CrashSentinel
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Set Environment Variables

Create a `.env` file with:

```env
FRED_API_KEY=your_fred_key
ZILLOW_API_KEY=your_zillow_key
REDDIT_CLIENT_ID=your_client_id
REDDIT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=CrashSentinel/0.1
TWITTER_BEARER_TOKEN=your_token
SEC_EMAIL=your_email
```

---

### ▶️ Run the App Locally

```bash
streamlit run dashboard/app.py
```

Visit [http://localhost:8501](http://localhost:8501)

---

## 🌐 Deployment Guide

1. Push repo to GitHub  
2. Go to https://streamlit.io/cloud  
3. Connect repo  
4. Set secrets in `Manage App` → `Secrets`  
5. Click **Deploy**

---

## 📊 Data Sources

- [Yahoo Finance](https://finance.yahoo.com/)
- [FRED](https://fred.stlouisfed.org/)
- [Zillow](https://www.zillow.com/research/data/)
- [Reddit API](https://www.reddit.com/dev/api)
- [Twitter](https://github.com/JustAnotherArchivist/snscrape)
- [SEC EDGAR](https://www.sec.gov/edgar.shtml)

---

## 📤 Export Options

- Download market data as **CSV**
- Generate **PDF Reports**
- Planned: Alerts via Email/Telegram

---

## 📌 Future Roadmap

- Alerts & Notifications (email, Telegram)
- GPT summaries of Reddit/SEC content
- LSTM + Transformer forecasting
- Zillow affordability analytics
- SHAP + LIME Explainability

---

## 📜 License

MIT License

---

## ✨ Contributors

Built with ❤️ by [@Brahamanbtp](https://github.com/Brahamanbtp)

---

## 📬 Contact

📧 pranaysharma5626@gmail.com

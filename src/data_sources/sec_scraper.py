import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables (e.g., custom headers)
load_dotenv()
EMAIL_CONTACT = os.getenv("SEC_EMAIL", "your_email@example.com")  # SEC requires a contact

# SEC API base
SEC_SEARCH_URL = "https://data.sec.gov/submissions/CIK{}.json"
SEC_HEADER = {
    "User-Agent": f"CrashSentinel/1.0 ({EMAIL_CONTACT})"
}


def get_cik_from_ticker(ticker: str) -> str:
    """
    Get Central Index Key (CIK) for a given stock ticker.
    """
    cik_url = f"https://www.sec.gov/files/company_tickers.json"
    response = requests.get(cik_url, headers=SEC_HEADER)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve CIKs: {response.status_code}")

    data = response.json()
    for company in data.values():
        if company["ticker"].lower() == ticker.lower():
            return str(company["cik_str"]).zfill(10)

    raise ValueError(f"CIK not found for ticker: {ticker}")


def get_recent_filings(cik: str, filing_types=["10-K", "10-Q"], limit=10) -> pd.DataFrame:
    """
    Fetch recent SEC filings (10-K, 10-Q, etc.) for a given CIK.
    """
    print(f" Fetching recent filings for CIK: {cik}")
    url = SEC_SEARCH_URL.format(cik)
    response = requests.get(url, headers=SEC_HEADER)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch filings: {response.status_code}")

    data = response.json()
    filings = data.get("filings", {}).get("recent", {})

    records = []
    for i in range(len(filings["accessionNumber"])):
        if filings["form"][i] not in filing_types:
            continue

        records.append({
            "form": filings["form"][i],
            "date_filed": filings["filingDate"][i],
            "accession_number": filings["accessionNumber"][i],
            "report_url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{filings['accessionNumber'][i].replace('-', '')}/{filings['primaryDocument'][i]}"
        })

        if len(records) >= limit:
            break

    return pd.DataFrame(records)


# CLI test
if __name__ == "__main__":
    ticker = "AAPL"
    cik = get_cik_from_ticker(ticker)
    df = get_recent_filings(cik, limit=5)
    print(df)

    os.makedirs("../../data", exist_ok=True)
    df.to_csv("../../data/sec_filings_aapl.csv", index=False)

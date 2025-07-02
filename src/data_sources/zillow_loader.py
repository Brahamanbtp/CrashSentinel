import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

#  Load .env file for secure API key handling
load_dotenv()

#  Get Zillow API Key from environment variable
ZWSID = os.getenv("ZILLOW_API_KEY")
if not ZWSID:
    raise EnvironmentError(" ZILLOW_API_KEY not found. Please set it in a .env file or as an environment variable.")

#  Base URL for RapidAPI Zillow endpoint
ZILLOW_BASE_URL = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"

#  Request headers using the RapidAPI key
HEADERS = {
    "X-RapidAPI-Key": ZWSID,
    "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
}

def fetch_zillow_listings(zipcode="10001", property_type="houses", limit=20) -> pd.DataFrame:
    """
    Fetch property listings from Zillow via RapidAPI based on zip code and type.
    Returns a DataFrame with selected property details.
    """
    print(f" Fetching Zillow listings for ZIP: {zipcode}, Type: {property_type}")

    params = {
        "location": zipcode,
        "home_type": property_type,
        "sort": "newest",
        "status_type": "for_sale",
        "limit": limit
    }

    try:
        response = requests.get(ZILLOW_BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f" Failed to fetch Zillow data: {e}")

    data = response.json()
    properties = data.get("props", [])

    if not properties:
        print(" No properties found.")
        return pd.DataFrame()

    #  Parse and structure response into a DataFrame
    listings = [
        {
            "address": p.get("address"),
            "price": p.get("price"),
            "bedrooms": p.get("bedrooms"),
            "bathrooms": p.get("bathrooms"),
            "area_sqft": p.get("livingArea"),
            "listing_date": datetime.utcfromtimestamp(p.get("listingDate") / 1000).date() if p.get("listingDate") else None,
            "zpid": p.get("zpid"),
            "latitude": p.get("latitude"),
            "longitude": p.get("longitude")
        }
        for p in properties
    ]

    return pd.DataFrame(listings)


#  CLI Test Execution
if __name__ == "__main__":
    df = fetch_zillow_listings(zipcode="90210", property_type="houses", limit=10)
    print(df.head())

    #  Save output
    output_path = "../../data/zillow_listings.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f" Zillow listings saved to {output_path}")

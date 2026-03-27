import yfinance as yf # type: ignore
import pandas as pd # type: ignore
import requests

def get_fear_greed_index():
    """Fetches the current Fear and Greed Index value."""
    # Using a common open-source API for sentiment data
    url = "https://api.alternative.me"
    try:
        response = requests.get(url)
        data = response.json()
        return int(data['data'][0]['value'])
    except Exception as e:
        print(f"Error fetching sentiment: {e}")
        return 50  # Default to neutral if API fails
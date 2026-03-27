import requests
from django.conf import settings
from decimal import Decimal
from datetime import datetime
import time

class AlphaVantageClient:
    """
    Client for Alpha Vantage API
    Get free API key at: https://www.alphavantage.co/
    """
    
    BASE_URL = 'https://www.alphavantage.co/query'
    
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.ALPHA_VANTAGE_API_KEY
    
    def get_forex_daily(self, from_symbol, to_symbol):
        """
        Get daily forex data
        
        Args:
            from_symbol: Currency to convert from (e.g., EUR)
            to_symbol: Currency to convert to (e.g., USD)
        
        Returns:
            dict with time series data
        """
        params = {
            'function': 'FX_DAILY',
            'from_symbol': from_symbol,
            'to_symbol': to_symbol,
            'apikey': self.api_key,
            'outputsize': 'full'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Error Message' in data:
                raise Exception(f"API Error: {data['Error Message']}")
            
            if 'Note' in data:
                raise Exception(f"API Rate Limited: {data['Note']}")
            
            return data.get('Time Series FX (Daily)', {})
        
        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get_forex_intraday(self, from_symbol, to_symbol, interval='60min'):
        """
        Get intraday forex data
        
        Args:
            from_symbol: Currency to convert from (e.g., EUR)
            to_symbol: Currency to convert to (e.g., USD)
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
        
        Returns:
            dict with time series data
        """
        params = {
            'function': 'FX_INTRADAY',
            'from_symbol': from_symbol,
            'to_symbol': to_symbol,
            'interval': interval,
            'apikey': self.api_key,
            'outputsize': 'full'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'Error Message' in data:
                raise Exception(f"API Error: {data['Error Message']}")
            
            if 'Note' in data:
                raise Exception(f"API Rate Limited: {data['Note']}")
            
            # Find the correct time series key
            for key in data.keys():
                if 'Time Series' in key:
                    return data[key]
            
            return {}
        
        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    @staticmethod
    def parse_forex_data(time_series_data):
        """
        Parse Alpha Vantage forex data into standard format
        
        Returns:
            list of tuples (timestamp, open, high, low, close)
        """
        parsed_data = []
        
        for timestamp_str, ohlc in sorted(time_series_data.items(), reverse=True):
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d')
                
                parsed_data.append({
                    'timestamp': timestamp,
                    'open': Decimal(ohlc['1. open']),
                    'high': Decimal(ohlc['2. high']),
                    'low': Decimal(ohlc['3. low']),
                    'close': Decimal(ohlc['4. close']),
                })
            except (ValueError, KeyError) as e:
                print(f"Error parsing data for {timestamp_str}: {str(e)}")
                continue
        
        return parsed_data

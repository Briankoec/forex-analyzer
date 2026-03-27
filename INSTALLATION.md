# 🚀 Forex Analyzer - Complete Installation Guide

## Overview

The Forex Analyzer is a complete Django web application for analyzing forex markets with:
- Real-time technical indicators (RSI, MACD, SMA)
- Automated buy/sell signal generation
- RSI-based "Greed Scale" sentiment analyzer
- Beautiful interactive charts
- REST API for integration

---

## ⚡ Express Setup (5 minutes)

```bash
# 1. Navigate to project
cd /workspaces/codespaces-blank

# 2. Activate environment
source venv/bin/activate

# 3. Start the application
cd forex_analyzer
python manage.py runserver

# 4. Open browser
# Dashboard: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
```

---

## 📋 Prerequisites

- Python 3.8 or higher ✓ (3.12.1 detected)
- Virtual environment ✓ (already created in `venv/`)
- All dependencies installed ✓ (Django, requests, pandas, numpy)

---

## 🔑 API Setup

### Get Your Free Alpha Vantage API Key

1. Visit: **https://www.alphavantage.co/api/**
2. Enter your email and get instant API key
3. **Edit** `forex_analyzer/.env` file:

```bash
# Before
ALPHA_VANTAGE_API_KEY=demo

# After
ALPHA_VANTAGE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
```

### Why Alpha Vantage?
- ✅ Free tier (5 requests/minute)
- ✅ Forex, stocks, crypto data
- ✅ 20+ years of historical data
- ✅ Easy to use REST API

---

## 📁 Project Structure

```
forex_analyzer/
├── analyzer/                          # Main application
│   ├── models.py                     # Database models
│   ├── views.py                      # View logic (URLs → HTML/JSON)
│   ├── indicators.py                 # Technical calculations
│   ├── api_client.py                 # Alpha Vantage integration
│   ├── admin.py                      # Django admin config
│   ├── urls.py                       # App routing
│   ├── migrations/                   # Database schema changes
│   │   └── 0001_initial.py           # Initial schema
│   ├── templates/
│   │   ├── base.html                 # Base template
│   │   ├── index.html                # Dashboard
│   │   └── pair_detail.html          # Analysis page
│   └── static/
│       ├── css/                      # Stylesheets
│       └── js/                       # JavaScript
│
├── forex_analyzer/                    # Project settings
│   ├── settings.py                   # Django configuration
│   ├── urls.py                       # Project routing
│   └── wsgi.py                       # Production server config
│
├── manage.py                         # Django CLI
├── db.sqlite3                        # SQLite database
├── requirements.txt                  # Python dependencies
├── .env                              # API keys (DO NOT COMMIT)
└── .env.example                      # Template for .env
```

---

## 💾 Database Models

### 1. ForexPair
Stores currency pair information
```
EUR/USD   → Euro to US Dollar
GBP/USD   → British Pound to US Dollar
JPY/USD   → Japanese Yen to US Dollar
```

### 2. ForexData
Historical OHLC (Open, High, Low, Close) data
- Imported from Alpha Vantage
- Timestamp, prices, volume
- Unique per pair per day

### 3. TechnicalIndicators
Calculated technical analysis for each price point
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- SMA (Simple Moving Averages 20 & 50)

### 4. TradingSignal
Generated buy/sell/hold signals
- Signal type (BUY, SELL, HOLD)
- Confidence score (0-100%)
- Greed level analysis
- Reasoning

---

## 🎯 Features Explained

### RSI (Relative Strength Index) - "Greed Scale"

Measures momentum on 0-100 scale:

| RSI Range | Signal | Sentiment | Action |
|-----------|--------|-----------|--------|
| 80-100 | OVERBOUGHT | **Extreme Greed** | SELL ↓ |
| 60-80 | HIGH | **Greed** | Consider Sell |
| 40-60 | NEUTRAL | **Neutral** | HOLD → |
| 20-40 | LOW | **Fear** | Consider Buy |
| 0-20 | OVERSOLD | **Extreme Fear** | BUY ↑ |

### MACD (Moving Average Convergence Divergence)

Trend and momentum indicator:
- **Buy Signal**: MACD crosses above signal line
- **Sell Signal**: MACD crosses below signal line
- **Histogram**: Shows momentum strength

### SMA (Simple Moving Averages)

Trend identification:
- **SMA 20 > SMA 50**: Uptrend (Bullish)
- **SMA 20 < SMA 50**: Downtrend (Bearish)

---

## 🌐 Using the Application

### 1. Dashboard (`/`)
See all monitored currency pairs at a glance
- Current price
- Latest RSI value with greed level
- MACD status
- Most recent trading signal
- Refresh button for each pair

### 2. Add Currency Pair
```
From: EUR
To: USD
→ Creates EUR/USD pair with historical data
```

Supported formats: Any valid 3-letter currency code
- Popular: EUR, USD, GBP, JPY, CHF, CAD, AUD, NZD

### 3. Pair Analysis Page (`/pair/<id>/`)
Detailed technical analysis for one pair:
- Live charts (price, RSI, MACD)
- Current indicators
- Trading signals history
- Signal confidence levels

### 4. Manual Refresh
Click "Refresh" to fetch latest data from API
- Updates OHLC prices
- Recalculates all indicators
- Logs trading signals

---

## 🔌 REST API Endpoints

### Get Dashboard Data
```bash
GET /
```
Returns: HTML dashboard

### Get Pair Details
```bash
GET /pair/<id>/
```
Returns: HTML pair analysis page

### Get Chart Data (JSON)
```bash
GET /api/pair/<id>/data/
```
Returns:
```json
{
  "pair": "EUR/USD",
  "data_points": [
    {
      "timestamp": "2026-03-27T00:00:00Z",
      "close": 1.0847,
      "rsi": 45.23,
      "macd": 0.00234
    }
  ]
}
```

### Get Trading Signals (JSON)
```bash
GET /api/pair/<id>/signals/
```
Returns:
```json
{
  "pair": "EUR/USD",
  "signals": [
    {
      "timestamp": "2026-03-27T12:00:00Z",
      "type": "BUY",
      "confidence": 78.5,
      "price": 1.0850,
      "greed_level": "fear"
    }
  ]
}
```

### Refresh Pair Data
```bash
POST /pair/<id>/refresh/
```
Returns: Success status + data count

### Create New Pair
```bash
GET /api/create-pair/?from=EUR&to=USD
```
Returns: Pair ID and symbol

---

## 🛠️ Django Admin Panel

Access at: `http://127.0.0.1:8000/admin/`

Features:
- View all currency pairs
- Browse historical data
- See calculated indicators
- Review trading signals
- Create/edit pairs manually

### Create Admin User (optional)
```bash
python manage.py createsuperuser
# Follow prompts to set username/password
```

---

## 📊 Adding Your First Pair

### Method 1: Web Interface (Recommended)
1. Go to http://127.0.0.1:8000/
2. Fill in "Add New Currency Pair" form
3. From: `EUR` → To: `USD`
4. Click "Add Pair"
5. Wait 10-15 seconds (first API call)
6. Charts will appear automatically

### Method 2: Using API
```bash
curl "http://127.0.0.1:8000/api/create-pair/?from=GBP&to=USD"
```

### Method 3: Django Shell
```bash
python manage.py shell
```
```python
from analyzer.models import ForexPair, ForexData
from analyzer.api_client import AlphaVantageClient

# Create pair
pair = ForexPair.objects.create(symbol='EUR/USD', name='Euro to US Dollar')

# Fetch data
client = AlphaVantageClient()
data = client.get_forex_daily('EUR', 'USD')

# Save data
for timestamp, prices in data.items():
    ForexData.objects.create(
        pair=pair,
        timestamp=timestamp,
        open_price=Decimal(prices['1. open']),
        high_price=Decimal(prices['2. high']),
        low_price=Decimal(prices['3. low']),
        close_price=Decimal(prices['4. close'])
    )
```

---

## ⚙️ Configuration

### settings.py Key Settings
```python
# Database (SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# API Configuration
ALPHA_VANTAGE_API_KEY = 'your-key-here'

# Debug mode (change to False for production)
DEBUG = True
```

### environment Variables (.env)
```
ALPHA_VANTAGE_API_KEY=your_api_key
DEBUG=True
SECRET_KEY=your-secret-key
```

---

## 🐛 Troubleshooting

### "API Rate Limited" Error
**Problem**: Too many requests in short time
**Solution**: Wait 60 seconds before next request (free tier: 5/minute)

### "No Data Available"
**Problem**: First API call timed out
**Solution**: Click refresh again, or wait and refresh page

### "ModuleNotFoundError: django"
**Problem**: Virtual environment not activated
**Solution**: 
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Database Locked
**Problem**: SQLite conflicts
**Solution**: 
```bash
rm db.sqlite3  # Delete database
python manage.py migrate  # Recreate it
```

### Port 8000 Already in Use
**Problem**: Another service using port 8000
**Solution**: 
```bash
python manage.py runserver 8001  # Use different port
```

---

## 📈 Performance Tips

1. **Cache Data**: Use `update_or_create()` to avoid duplicates
2. **Batch Operations**: Calculate indicators in bulk
3. **Limit Queries**: Use `select_related()` and `prefetch_related()`
4. **Database Indexes**: Already configured on `pair` and `timestamp`

---

## 🔒 Security for Production

### Before deploying:
1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Use environment variables for secrets
4. Set ALLOWED_HOSTS properly
5. Use PostgreSQL instead of SQLite
6. Enable HTTPS
7. Set secure cookie flags
8. Use `.env` file that's not committed

### Production Deployment:
```bash
# Use Gunicorn instead of `runserver`
gunicorn forex_analyzer.wsgi:application

# Use Nginx as reverse proxy
# Deploy with Docker for consistency
```

---

## 📚 Learning Resources

- **Technical Analysis**: https://school.stockcharts.com/
- **Alpha Vantage API**: https://www.alphavantage.co/documentation/
- **Django**: https://docs.djangoproject.com/
- **RSI Indicator**: https://www.investopedia.com/terms/r/rsi.asp
- **MACD Indicator**: https://www.investopedia.com/terms/m/macd.asp
- **Forex Trading**: https://www.investopedia.com/terms/f/forex.asp

---

## 🎓 Educational Notes

⚠️ **Important Disclaimers**:
- This system is for **learning and analysis** only
- Do NOT use signals for real trading without proper risk management
- Always do your own research before trading
- Backtest strategies before going live
- Never risk more than you can afford to lose

---

## 📞 Support

### Check logs
```bash
# View recent errors
tail -f /tmp/django.log
```

### Test API connection
```bash
python manage.py shell
from analyzer.api_client import AlphaVantageClient
client = AlphaVantageClient()
data = client.get_forex_daily('EUR', 'USD')
print(list(data.keys())[:5])
```

### Validate models
```bash
python manage.py check analyzer
```

---

**✅ You're all set! Start the server with:**
```bash
cd forex_analyzer
python manage.py runserver
```

**Then visit: http://127.0.0.1:8000/**

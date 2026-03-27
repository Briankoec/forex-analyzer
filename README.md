# 📈 Forex Market Analysis & Trading Signal Generator

A comprehensive web-based application for analyzing forex markets and generating buy/sell trading signals using technical indicators with a greed scale (RSI) implementation.

## 🎯 Features

- **Real-time Forex Analysis**: Monitor multiple currency pairs simultaneously
- **Technical Indicators**: 
  - RSI (Relative Strength Index) as Greed Scale
  - MACD (Moving Average Convergence Divergence)
  - SMA (Simple Moving Averages) - 20 & 50 periods
- **Trading Signals**: Automated buy/sell/hold signals based on technical analysis
- **Greed Scale**: Map RSI values to market sentiment:
  - 🔴 Extreme Greed (RSI > 80): Sell signal
  - 🟠 Greed (RSI 60-80): Consider selling
  - ⚪ Neutral (RSI 40-60): No clear signal
  - 🔵 Fear (RSI 20-40): Consider buying
  - 🟢 Extreme Fear (RSI < 20): Buy signal
- **Interactive Dashboards**: Beautiful, responsive UI with real-time charts
- **Historical Data**: OHLC data visualization and analysis
- **Admin Panel**: Manage pairs, view signals, and configure settings

## 📋 System Requirements

- Python 3.8+
- Django 4.2+
- pandas, numpy
- Alpha Vantage API (free key available)
- Modern web browser

## 🚀 Installation

### Option 1: Quick Start (Recommended)

```bash
# Run the setup script
bash /workspaces/codespaces-blank/run_app.sh

# App will be available at http://localhost:8000
# Admin: http://localhost:8000/admin
# Credentials: admin / admin
```

### Option 2: Manual Setup

```bash
# Navigate to project
cd /workspaces/codespaces-blank

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Django
cd forex_analyzer
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Create admin user

# Run server
python manage.py runserver 0.0.0.0:8000
```

### Option 3: Docker Setup (Production-Ready)

```bash
cd /workspaces/codespaces-blank

# Build and run
docker-compose up --build

# Access at http://localhost:8000
```
## 🔑 Configuration

### Alpha Vantage API Key

The app uses Alpha Vantage for forex data. Get your free API key:

1. Visit https://www.alphavantage.co/
2. Sign up for a free API key
3. Update `.env` file in the project root:

```env
ALPHA_VANTAGE_API_KEY=your_api_key_here
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Default Admin Credentials

- **Username**: admin
- **Password**: admin

⚠️ **Change these in production!**

## 📊 Usage

### Dashboard

1. Navigate to http://localhost:8000
2. Add currency pairs (e.g., EUR/USD, GBP/JPY)
3. Click "Refresh Data" to fetch market data
4. View real-time indicators and trading signals

### Pair Analysis

Click on any pair to view:
- Detailed price charts with RSI overlay
- Trading signals with confidence levels
- Historical OHLC data
- Greed level indicators
- MACD and Moving Average analysis

### Admin Panel

Access admin panel at http://localhost:8000/admin to:
- Manage forex pairs
- View trading signals
- Edit technical indicators
- Configure system settings

## 🧮 Technical Indicators Explained

### RSI (Relative Strength Index)
- **Period**: 14 (default)
- **Range**: 0-100
- **What it measures**: Momentum and overbought/oversold conditions
- **Interpretation**:
  - > 70: Overbought (potential sell signal, greed)
  - < 30: Oversold (potential buy signal, fear)
  - Used as the "Greed Scale" in this application

### MACD (Moving Average Convergence Divergence)
- **Fast EMA**: 12 periods
- **Slow EMA**: 26 periods
- **Signal Line**: 9-period EMA of MACD
- **Trading Signals**:
  - MACD crosses above signal line: Bullish (buy signal)
  - MACD crosses below signal line: Bearish (sell signal)

### SMA (Simple Moving Average)
- **SMA-20**: Short-term trend (20-day average)
- **SMA-50**: Long-term trend (50-day average)
- **Trending Signals**:
  - SMA-20 > SMA-50: Uptrend (bullish)
  - SMA-20 < SMA-50: Downtrend (bearish)

## 📈 Trading Signal Logic

Signals are generated using a confidence scoring system:

```
CONFIDENCE CALCULATION:
━━━━━━━━━━━━━━━━━━━━━━━━

RSI Analysis:
  • RSI < 30 (oversold): +35 confidence (buy signal)
  • RSI > 70 (overbought): +35 confidence (sell signal)

MACD Analysis:
  • MACD > Signal Line (bullish cross): +25 confidence
  • MACD < Signal Line (bearish cross): -25 confidence

Moving Average Analysis:
  • SMA-20 > SMA-50 (uptrend): +20 confidence
  • SMA-20 < SMA-50 (downtrend): -20 confidence

FINAL SIGNALS:
  • BUY: Confidence > 40% AND RSI < 50%
  • SELL: Confidence < -40% AND RSI > 50%
  • HOLD: Otherwise (conflicting signals)
```

## 📁 Project Structure

```
forex_analyzer/
├── analyzer/
│   ├── migrations/          # Database migrations
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Custom styling
│   │   └── js/
│   │       └── main.js     # Main JavaScript functions
│   ├── templates/
│   │   ├── base.html       # Base template (header, nav, footer)
│   │   ├── index.html      # Dashboard with pair grid
│   │   └── pair_detail.html# Detailed analysis for a pair
│   ├── models.py           # Database models
│   ├── views.py            # View controllers
│   ├── urls.py             # URL routing (analyzer app)
│   ├── indicators.py       # Technical analysis calculations
│   ├── api_client.py       # Alpha Vantage API client
│   ├── tasks.py            # Celery tasks (optional)
│   └── admin.py            # Django admin configuration
├── forex_analyzer/
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main project URLs
│   └── wsgi.py             # WSGI application entry point
├── requirements.txt        # Python dependencies
├── manage.py              # Django management CLI
├── run_app.sh             # Automated setup script
├── Dockerfile             # Docker containerization
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## 🔌 API Endpoints

### Web Pages
- `GET /` - Dashboard with all pairs
- `GET /pair/<pair_id>/` - Detailed analysis for a specific pair

### JSON APIs (for AJAX/Frontend)

```
GET /api/create-pair/?from=EUR&to=USD
    Create a new currency pair for monitoring
    Returns: {"success": true, "pair_id": 1, "symbol": "EUR/USD"}

GET /api/pair/<pair_id>/data/
    Get historical price and indicator data for charting
    Returns: {"pair": "EUR/USD", "data_points": [...]}

GET /api/pair/<pair_id>/signals/
    Get recent trading signals for a pair
    Returns: {"pair": "EUR/USD", "signals": [...]}

POST /pair/<pair_id>/refresh/
    Manually refresh historical data for a pair
    Headers: X-CSRFToken (required)
    Returns: {"success": true, "message": "..."}
```

## 🐛 Troubleshooting

### Problem: "API Rate Limited" Error
**Solution**: Alpha Vantage has a 5 calls/minute limit on free tier
- Wait 60 seconds before retrying
- Upgrade to premium API key for more calls/minute

### Problem: "No data available"
**Solution**: Check your configuration
```bash
# Verify API key in .env
cat .env

# Check if the database exists
ls -la forex_analyzer/db.sqlite3

# Try manual migration
cd forex_analyzer
python manage.py migrate
```

### Problem: Port 8000 already in use
**Solution**: Use a different port
```bash
python manage.py runserver 8001
```

### Problem: ModuleNotFoundError
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: Static files not loading
**Solution**: Collect static files
```bash
cd forex_analyzer
python manage.py collectstatic --noinput
```

## 🚀 Deployment

### Deploy to Heroku

```bash
# Create Procfile
echo "web: cd forex_analyzer && gunicorn forex_analyzer.wsgi --log-file -" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
git push heroku main
```

### Deploy to AWS EC2

```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Clone project
git clone https://github.com/your-repo/forex-analyzer.git
cd forex-analyzer

# Setup
bash run_app.sh

# Use systemd to auto-start (optional)
sudo nano /etc/systemd/system/forex-analyzer.service
```

### Deploy with Docker

```bash
# Build image
docker build -t forex-analyzer:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e ALPHA_VANTAGE_API_KEY=your_key \
  --name forex-analyzer \
  forex-analyzer:latest

# Or use Docker Compose
docker-compose up -d
```

## 📚 References & Learning Resources

- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- [Technical Analysis Basics](https://school.stockcharts.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Investopedia - RSI](https://www.investopedia.com/terms/r/rsi.asp)
- [Investopedia - MACD](https://www.investopedia.com/terms/m/macd.asp)
- [Chart.js Documentation](https://www.chartjs.org/)

## 📊 Data Models

### ForexPair
```python
- symbol: CharField (e.g., 'EUR/USD')
- name: CharField (e.g., 'Euro to US Dollar')
- is_active: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

### ForexData
```python
- pair: ForeignKey(ForexPair)
- timestamp: DateTimeField
- open_price: DecimalField
- high_price: DecimalField
- low_price: DecimalField
- close_price: DecimalField
- volume: IntegerField
```

### TechnicalIndicators
```python
- forex_data: OneToOneField(ForexData)
- rsi: FloatField (0-100)
- rsi_signal: CharField (overbought/normal/oversold)
- macd: FloatField
- macd_signal: FloatField
- macd_histogram: FloatField
- sma_20: FloatField
- sma_50: FloatField
```

### TradingSignal
```python
- pair: ForeignKey(ForexPair)
- timestamp: DateTimeField
- signal_type: CharField (BUY/SELL/HOLD)
- confidence: FloatField (0-100)
- reason: TextField
- price_at_signal: DecimalField
- rsi_value: FloatField
- greed_level: CharField (extreme_greed/greed/neutral/fear/extreme_fear)
- is_active: BooleanField
```

## 💡 Future Enhancements

- [ ] Machine Learning predictions (LSTM/Prophet)
- [ ] More technical indicators (Bollinger Bands, Stochastic, ATR)
- [ ] Multi-timeframe analysis
- [ ] Backtesting engine
- [ ] Email/SMS alerts for trading signals
- [ ] Portfolio management features
- [ ] Risk/Reward ratio calculator
- [ ] Real-time WebSocket updates
- [ ] Mobile app (React Native/Flutter)
- [ ] Historical signal performance reports

## ⚠️ Important Disclaimer

**⚠️ EDUCATIONAL PURPOSE ONLY**

This application is for educational and learning purposes only. It is NOT financial advice and should NOT be used for real trading without:

1. Extensive backtesting and validation
2. Risk management strategies
3. Professional financial consultation
4. Paper trading verification

**Remember**: 
- Past performance ≠ Future results
- Always do your own research (DYOR)
- Never risk more than you can afford to lose
- Use stop-losses and proper risk management

Use this tool at your own risk. The developers assume no responsibility for financial losses.



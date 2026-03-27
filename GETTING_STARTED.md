## 🚀 Getting Started Guide

Welcome to the Forex Market Analysis Application! This guide will help you get up and running quickly.

### ⚡ Quick Start (< 2 minutes)

```bash
# Navigate to project root
cd /workspaces/codespaces-blank

# Run the automated setup
bash run_app.sh
```

That's it! The app will start at `http://localhost:8000`

### 📋 Step-by-Step Setup

#### Step 1: Install the App

```bash
cd /workspaces/codespaces-blank
bash run_app.sh
```

#### Step 2: Get Your API Key

1. Visit https://www.alphavantage.co/
2. Click "GET FREE API KEY"
3. Enter your email and create an account
4. You'll receive your API key via email
5. Edit `.env` file and add your key:

```env
ALPHA_VANTAGE_API_KEY=your_api_key_here
DEBUG=False
SECRET_KEY=your-secret-key
```

#### Step 3: Start Using the App

1. Open browser: http://localhost:8000
2. You should see the dashboard
3. Admin panel: http://localhost:8000/admin (admin/admin)

#### Step 4: Add Your First Currency Pair

1. In the dashboard, find "Add New Currency Pair"
2. Enter "EUR" in the "From" field
3. Enter "USD" in the "To" field
4. Click "Add Pair"
5. Wait for data to load (may take 5-10 seconds on first run)
6. You'll see a card for EUR/USD with price and indicators

#### Step 5: Refresh and Analyze

1. Click "Refresh Data" on any pair card
2. Watch the technical indicators update:
   - **RSI**: Shows market greed/fear (0-100 scale)
   - **MACD**: Shows trend momentum
   - **Price**: Current exchange rate
3. Check the trading signal for buy/sell recommendations

### 📊 Understanding the Dashboard

#### Main Dashboard
- **Cards at top**: Summary statistics
- **Pair Grid**: All monitored currency pairs
- **Indicators**: Real-time RSI, MACD, and prices
- **Signals**: BUY/SELL/HOLD with confidence

#### Pair Detail Page
- **Price Chart**: Interactive chart with price and RSI
- **RSI Chart**: Separate RSI greed scale visualization
- **MACD Chart**: Momentum indicator
- **Historical Data**: Last 30 days OHLC data
- **Trading Signals**: Recent generated signals

### 🧮 Understanding Indicators

#### RSI (Greed Scale)
- **80+**: 🔴 Extreme Greed - SELL Signal
- **60-80**: 🟠 Greed - Consider selling
- **40-60**: ⚪ Neutral - No clear signal
- **20-40**: 🔵 Fear - Consider buying
- **<20**: 🟢 Extreme Fear - BUY Signal

#### MACD
- When MACD line is above signal line: Bullish 📈
- When MACD line is below signal line: Bearish 📉

#### Moving Averages
- When SMA-20 > SMA-50: Uptrend 📈
- When SMA-20 < SMA-50: Downtrend 📉

### 💡 Trading Signals

Signals are generated with a confidence score (0-100%):

**BUY Signal** (Green)
- RSI < 30 (Oversold)
- MACD above signal line
- Confidence > 40%

**SELL Signal** (Red)
- RSI > 70 (Overbought)
- MACD below signal line
- Confidence > 40%

**HOLD Signal** (Yellow)
- Conflicting indicators
- No clear directional bias

### 🔧 Common Tasks

#### Change Admin Password
```bash
cd forex_analyzer
python manage.py changepassword admin
```

#### Add Another Currency Pair
1. Dashboard → "Add New Currency Pair"
2. Enter currency codes (EUR, GBP, JPY, etc.)
3. Click "Add Pair"

#### Refresh All Data
```bash
cd forex_analyzer
python manage.py shell
from analyzer.views import generate_indicators_for_pair
from analyzer.models import ForexPair
for pair in ForexPair.objects.filter(is_active=True):
    generate_indicators_for_pair(pair)
exit()
```

#### Stop the Server
Press `Ctrl+C` in the terminal

#### Restart the Server
```bash
cd /workspaces/codespaces-blank
bash start_dev.sh
```

### 🐛 Troubleshooting

**Problem**: App won't start
- Check Python version: `python --version` (need 3.8+)
- Check port: `lsof -i :8000`
- Check dependencies: `pip install -r requirements.txt`

**Problem**: "API Rate Limited"
- Alpha Vantage allows 5 calls/minute
- Wait and try again later
- Free tier has limited concurrency

**Problem**: No data showing
- Verify API key in `.env`
- Check internet connection
- Try refreshing: click the refresh button on pair card

**Problem**: Static files not loading (CSS/JS broken)
```bash
cd forex_analyzer
python manage.py collectstatic --noinput
```

### 📚 Next Steps

1. **Explore the Dashboard**: Add different currency pairs
2. **Learn Indicators**: Study how RSI, MACD work
3. **Test Signals**: Compare signals across different pairs
4. **Backtesting**: Use historical data to validate signals
5. **Deployment**: Deploy to cloud (Heroku, AWS, etc.)

### 🔗 Useful Resources

- [Alpha Vantage API](https://www.alphavantage.co/)
- [Technical Analysis Guide](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [Django Docs](https://docs.djangoproject.com/)
- [Chart.js Docs](https://www.chartjs.org/)

### ⚠️ Important Reminders

1. **Educational Purpose**: This is for learning, not real trading
2. **Do Your Research**: Always validate signals before trading
3. **Risk Management**: Use stop-losses and position sizing
4. **API Limits**: Free tier has rate limits (5 calls/min)
5. **Data Quality**: First data fetch may take 5-10 seconds

### 🎉 You're All Set!

Start exploring forex markets with technical analysis. Happy trading!

---

**Need Help?**
- Check README.md for comprehensive documentation
- Review indicator definitions in this guide
- Check Django logs for errors: `tail -f ../forex_analyzer/db.sqlite3`

**Questions?**
- Review the code in `forex_analyzer/analyzer/`
- Check the admin panel for database contents
- Experiment with different currency pairs

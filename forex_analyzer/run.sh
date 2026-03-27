#!/bin/bash

# Quick Start Script for Forex Analyzer

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        🚀 FOREX MARKET ANALYZER - QUICK START            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if venv is activated
if [[ ! "$VIRTUAL_ENV" == *"venv"* ]]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

echo "✅ Virtual environment: $VIRTUAL_ENV"
echo ""

# Navigate to project directory
cd forex_analyzer

echo "🌐 Starting Django development server..."
echo ""
echo "📍 App URL: http://127.0.0.1:8000/"
echo "📍 Admin Panel: http://127.0.0.1:8000/admin/"
echo ""
echo "⚠️  IMPORTANT: To use the API, edit the .env file with your Alpha Vantage API key:"
echo "   1. Get your FREE API key at: https://www.alphavantage.co/"
echo "   2. Edit .env file in the forex_analyzer directory"
echo "   3. Replace 'demo' with your actual API key"
echo ""
echo "📚 Default credentials for learning:"
echo "   • Username: admin"
echo "   • Password: admin123"
echo ""
echo "🎯 Getting Started:"
echo "   1. Open http://127.0.0.1:8000/ in your browser"
echo "   2. Go to Dashboard"
echo "   3. Add a currency pair (e.g., EUR, USD)"
echo "   4. Wait for data to load (first request may take 10-15 seconds)"
echo "   5. View charts and trading signals"
echo ""
echo "🔑 Press Ctrl+C to stop the server"
echo ""

# Run server
python manage.py runserver

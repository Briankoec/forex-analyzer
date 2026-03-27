#!/bin/bash

# Forex Analyzer - Development Server Startup Guide

echo "======================================"
echo "  Forex Market Analyzer"
echo "  Development Server Startup Guide"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "forex_analyzer/manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   cd /workspaces/codespaces-blank"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found"
    echo "   Run: bash run_app.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Navigate to Django project
cd forex_analyzer

echo "✓ Virtual environment activated"
echo ""

# Check database
if [ ! -f "db.sqlite3" ]; then
    echo "⚠️  Database not found. Running migrations..."
    python manage.py migrate --noinput
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  🚀 Starting Development Server"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📍 Application URLs:"
echo "   Dashboard:     http://localhost:8000"
echo "   Admin Panel:   http://localhost:8000/admin"
echo "   Admin Login:   admin / admin (change in production)"
echo ""
echo "📚 Documentation:"
echo "   README:        ../README.md"
echo "   API Docs:      See README.md section 'API Endpoints'"
echo ""
echo "⌨️  Commands:"
echo "   Ctrl+C         Stop server"
echo "   Ctrl+D         Exit"
echo ""
echo "⚠️  First Run:"
echo "   1. Get Alpha Vantage API key from https://www.alphavantage.co/"
echo "   2. Update ../.env with your API key"
echo "   3. Add a currency pair (e.g., EUR/USD)"
echo "   4. Refresh data to fetch market information"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""

# Start server
python manage.py runserver 0.0.0.0:8000

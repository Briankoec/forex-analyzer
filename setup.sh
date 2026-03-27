#!/bin/bash

# Forex Analyzer Setup Script

echo "🚀 Forex Analyzer Setup Script"
echo "==============================="
echo ""

# Check Python version
echo "📝 Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo ""
echo "🗄️ Running database migrations..."
cd forex_analyzer
python manage.py migrate

# Create .env if doesn't exist
echo ""
echo "🔑 Checking for .env file..."
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "ALPHA_VANTAGE_API_KEY=demo" > .env
    echo ""
    echo "⚠️  .env file created with demo API key."
    echo "📍 Get your free API key at: https://www.alphavantage.co/"
    echo "📝 Edit .env file and replace 'demo' with your actual API key."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. cd forex_analyzer"
echo "   3. python manage.py runserver"
echo "   4. Visit: http://localhost:8000/"
echo ""

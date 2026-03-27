#!/bin/bash

# Forex Analyzer Setup and Run Script
set -e

echo "======================================"
echo "   Forex Market Analyzer - Setup"
echo "======================================"
echo ""

# Change to project directory
cd /workspaces/codespaces-blank

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "✓ Activating virtual environment..."
    source venv/bin/activate
else
    echo "✓ Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
fi

echo ""
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file from template..."
    cp .env.example .env
    echo "   Please update .env with your Alpha Vantage API key"
fi

echo ""
echo "✓ Setting up Django application..."
cd forex_analyzer

# Run migrations
echo "✓ Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "✓ Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional - only if database is empty)
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.exists())" 2>/dev/null | grep -q "True"; then
    echo ""
    echo "✓ Creating superuser..."
    echo "   Enter Django admin credentials:"
    python manage.py createsuperuser --no-input \
        --username admin \
        --email admin@localhost.com 2>/dev/null || true
    echo "   Default login: admin / admin (change in production)"
fi

echo ""
echo "======================================"
echo "   Setup Complete!"
echo "======================================"
echo ""
echo "Starting development server..."
echo ""
echo "🌐 Application will be available at:"
echo "   http://localhost:8000"
echo ""
echo "📊 Admin panel:"
echo "   http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start development server
python manage.py runserver 0.0.0.0:8000

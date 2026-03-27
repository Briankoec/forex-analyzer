"""
Management command to populate sample forex data for testing.
This is useful for development and testing without needing a real API key.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
from analyzer.models import ForexPair, ForexData, TechnicalIndicators, TradingSignal
from analyzer.indicators import TechnicalAnalyzer, TradingSignalGenerator
import random


class Command(BaseCommand):
    help = 'Populate sample forex data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=60,
            help='Number of days of sample data to generate'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating'
        )

    def handle(self, *args, **options):
        days = options['days']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write('Clearing existing data...')
            ForexData.objects.all().delete()
            TradingSignal.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Generating sample forex data...'))

        # Get or create pairs
        pairs_data = [
            ('EUR/USD', 1.0850, 'Euro to US Dollar'),
            ('GBP/USD', 1.2650, 'British Pound to US Dollar'),
            ('USD/JPY', 149.50, 'US Dollar to Japanese Yen'),
        ]

        for symbol, start_price, name in pairs_data:
            pair, created = ForexPair.objects.get_or_create(
                symbol=symbol,
                defaults={'name': name, 'is_active': True}
            )

            if created:
                self.stdout.write(f'  Created pair: {symbol}')

            # Generate sample historical data
            self.stdout.write(f'  Generating {days} days of data for {symbol}...')
            current_price = start_price
            base_date = timezone.now() - timedelta(days=days)

            for day in range(days):
                timestamp = base_date + timedelta(days=day)

                # Generate realistic OHLC data
                daily_change = random.uniform(-0.02, 0.02)  # -2% to +2% daily change
                open_price = Decimal(str(current_price))
                close_price = Decimal(str(current_price * (1 + daily_change)))
                high_price = Decimal(str(max(current_price, current_price * (1 + random.uniform(0, daily_change + 0.01)))))
                low_price = Decimal(str(min(current_price, current_price * (1 + random.uniform(daily_change - 0.01, 0)))))

                current_price = float(close_price)

                # Create ForexData entry
                forex_data, created = ForexData.objects.get_or_create(
                    pair=pair,
                    timestamp=timestamp,
                    defaults={
                        'open_price': open_price,
                        'high_price': high_price,
                        'low_price': low_price,
                        'close_price': close_price,
                        'volume': random.randint(1000, 10000),
                    }
                )

                if created and day % 10 == 0:
                    self.stdout.write(f'    {timestamp.date()}: ${close_price}')

            # Generate indicators for all data
            self.stdout.write(f'  Calculating technical indicators for {symbol}...')
            self.generate_indicators(pair)

            # Generate trading signals
            self.stdout.write(f'  Generating trading signals for {symbol}...')
            self.generate_signals(pair)

        self.stdout.write(self.style.SUCCESS('✓ Sample data generation complete!'))
        self.stdout.write(self.style.SUCCESS('You can now view the app with chart data.'))
        self.stdout.write(self.style.WARNING('Note: This is sample data for testing. Use your own API key for real data.'))

    def generate_indicators(self, pair):
        """Generate technical indicators for all data points"""
        forex_data = ForexData.objects.filter(pair=pair).order_by('timestamp')

        if not forex_data.exists():
            return

        all_prices = [float(d.close_price) for d in forex_data]

        for i, data in enumerate(forex_data):
            # Need at least 26 data points for MACD (slow=26)
            if i < 25:
                continue

            prices_up_to_now = all_prices[:i+1]

            # Calculate indicators
            rsi = TechnicalAnalyzer.calculate_rsi(prices_up_to_now, period=14)
            macd, macd_signal, macd_histogram = TechnicalAnalyzer.calculate_macd(prices_up_to_now)
            sma_20 = TechnicalAnalyzer.calculate_sma(prices_up_to_now, period=20)
            sma_50 = TechnicalAnalyzer.calculate_sma(prices_up_to_now, period=50)

            # Save indicators
            indicators, created = TechnicalIndicators.objects.get_or_create(forex_data=data)
            indicators.rsi = rsi
            indicators.rsi_signal = TechnicalAnalyzer.get_rsi_signal(rsi)
            indicators.macd = macd
            indicators.macd_signal = macd_signal
            indicators.macd_histogram = macd_histogram
            indicators.sma_20 = sma_20
            indicators.sma_50 = sma_50
            indicators.save()

    def generate_signals(self, pair):
        """Generate trading signals for a pair"""
        latest_data = ForexData.objects.filter(
            pair=pair,
            indicators__isnull=False
        ).order_by('-timestamp').first()

        if not latest_data or not latest_data.indicators:
            return

        indicators = latest_data.indicators

        signal_data = TradingSignalGenerator.generate_signal(
            rsi=indicators.rsi,
            macd_value=indicators.macd,
            macd_signal=indicators.macd_signal,
            sma_20=indicators.sma_20,
            sma_50=indicators.sma_50,
            current_price=latest_data.close_price
        )

        greed_level = TechnicalAnalyzer.get_greed_level(indicators.rsi)

        TradingSignal.objects.create(
            pair=pair,
            signal_type=signal_data['signal_type'],
            confidence=signal_data['confidence'],
            reason=signal_data['reason'],
            price_at_signal=latest_data.close_price,
            rsi_value=indicators.rsi,
            macd_value=indicators.macd,
            greed_level=greed_level,
        )

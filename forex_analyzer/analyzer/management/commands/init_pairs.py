from django.core.management.base import BaseCommand
from analyzer.models import ForexPair

class Command(BaseCommand):
    help = 'Initialize default forex pairs'

    def handle(self, *args, **options):
        # Create default pairs if they don't exist
        pairs = [
            {'symbol': 'EUR/USD', 'name': 'Euro / US Dollar', 'base_asset': 'EUR', 'quote_asset': 'USD', 'exchange': 'FOREX'},
            {'symbol': 'GBP/USD', 'name': 'British Pound / US Dollar', 'base_asset': 'GBP', 'quote_asset': 'USD', 'exchange': 'FOREX'},
            {'symbol': 'USD/JPY', 'name': 'US Dollar / Japanese Yen', 'base_asset': 'USD', 'quote_asset': 'JPY', 'exchange': 'FOREX'},
            {'symbol': 'XAU/USD', 'name': 'Gold / US Dollar', 'base_asset': 'XAU', 'quote_asset': 'USD', 'exchange': 'FOREX'},
            {'symbol': 'BTC/USD', 'name': 'Bitcoin / US Dollar', 'base_asset': 'BTC', 'quote_asset': 'USD', 'exchange': 'CRYPTO'},
            {'symbol': 'ETH/USD', 'name': 'Ethereum / US Dollar', 'base_asset': 'ETH', 'quote_asset': 'USD', 'exchange': 'CRYPTO'},
        ]
        
        created_count = 0
        for pair_data in pairs:
            pair, created = ForexPair.objects.get_or_create(
                symbol=pair_data['symbol'],
                defaults={
                    'name': pair_data['name'],
                    'base_asset': pair_data['base_asset'],
                    'quote_asset': pair_data['quote_asset'],
                    'exchange': pair_data['exchange'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created {pair.symbol}'))
            else:
                self.stdout.write(f'  {pair.symbol} already exists')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Initialized {created_count} pairs'))

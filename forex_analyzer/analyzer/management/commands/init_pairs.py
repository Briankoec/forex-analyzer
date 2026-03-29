from django.core.management.base import BaseCommand
from analyzer.models import ForexPair

class Command(BaseCommand):
    help = 'Initialize default forex pairs'

    def handle(self, *args, **options):
        # Create default pairs if they don't exist
        pairs = [
            {'symbol': 'EUR/USD', 'name': 'Euro / US Dollar'},
            {'symbol': 'GBP/USD', 'name': 'British Pound / US Dollar'},
            {'symbol': 'USD/JPY', 'name': 'US Dollar / Japanese Yen'},
            {'symbol': 'XAU/USD', 'name': 'Gold / US Dollar'},
            {'symbol': 'BTC/USD', 'name': 'Bitcoin / US Dollar'},
            {'symbol': 'ETH/USD', 'name': 'Ethereum / US Dollar'},
        ]
        
        created_count = 0
        for pair_data in pairs:
            pair, created = ForexPair.objects.get_or_create(
                symbol=pair_data['symbol'],
                defaults={
                    'name': pair_data['name'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created {pair.symbol}'))
            else:
                self.stdout.write(f'  {pair.symbol} already exists')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Initialized {created_count} pairs'))

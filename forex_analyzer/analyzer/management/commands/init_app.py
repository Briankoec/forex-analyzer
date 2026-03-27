from django.core.management.base import BaseCommand
from analyzer.management.commands.populate_sample_data import Command as PopulateCommand

class Command(BaseCommand):
    help = 'Initialize pairs and populate data if database is empty'

    def handle(self, *args, **options):
        from analyzer.models import ForexPair, ForexData
        
        # Initialize pairs
        self.stdout.write('Initializing pairs...')
        pair_creator = PopulateCommand()
        pair_creator.handle(*args, **{'verbosity': 0})
        
        # Check if data exists
        pair_count = ForexPair.objects.count()
        data_count = ForexData.objects.count()
        
        if pair_count > 0 and data_count == 0:
            self.stdout.write('Populating initial data...')
            # Run populate_sample_data
            try:
                populate_cmd = PopulateCommand()
                populate_cmd.handle(days=60, clear=False, verbosity=1)
                self.stdout.write(self.style.SUCCESS('✓ Data populated'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not auto-populate data: {str(e)}'))
        elif data_count > 0:
            self.stdout.write(f'✓ Database already populated ({data_count} data points)')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Initialization complete!'))

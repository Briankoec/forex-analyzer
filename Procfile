web: cd forex_analyzer && gunicorn forex_analyzer.wsgi:application
release: cd forex_analyzer && python manage.py migrate && python manage.py init_pairs && python manage.py populate_sample_data --days 60

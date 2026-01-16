"""
Management command to load demo data for LegalDocs Manager.

Usage:
    python manage.py load_demo_data         # Load demo data
    python manage.py load_demo_data --clear # Clear existing data and reload
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from cases.models import Case
from clients.models import Client
from documents.models import Document


class Command(BaseCommand):
    """Load demo data fixtures into the database."""

    help = 'Load demo data (clients, cases, documents) into the database'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading fixtures',
        )

    def handle(self, *args, **options):
        """Execute the command."""
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Document.objects.all().delete()
            Case.objects.all().delete()
            Client.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        self.stdout.write('Loading demo data...')

        # Load fixtures in order (respecting foreign key relationships)
        fixtures = [
            'fixtures/demo_clients.json',
            'fixtures/demo_cases.json',
            'fixtures/demo_documents.json',
        ]

        for fixture in fixtures:
            self.stdout.write(f'  Loading {fixture}...')
            try:
                call_command('loaddata', fixture, verbosity=0)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  Error loading {fixture}: {e}')
                )
                return

        # Report counts
        client_count = Client.objects.count()
        case_count = Case.objects.count()
        document_count = Document.objects.count()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully!'))
        self.stdout.write(f'  Clients: {client_count}')
        self.stdout.write(f'  Cases: {case_count}')
        self.stdout.write(f'  Documents: {document_count}')

        # Validation
        if client_count < 20:
            self.stdout.write(
                self.style.WARNING(f'  Warning: Expected 20+ clients, got {client_count}')
            )
        if case_count < 30:
            self.stdout.write(
                self.style.WARNING(f'  Warning: Expected 30+ cases, got {case_count}')
            )
        if document_count < 50:
            self.stdout.write(
                self.style.WARNING(f'  Warning: Expected 50+ documents, got {document_count}')
            )

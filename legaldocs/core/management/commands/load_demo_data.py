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

        # Seed mock files to storage for any demo documents that don't have files
        self.stdout.write('Seeding mock files to storage backend...')
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        import os

        # Minimal valid PDF content to prevent viewer errors
        MINIMAL_PDF = (
            b"%PDF-1.4\n"
            b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
            b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Resources<<>>/Contents 4 0 R>>endobj\n"
            b"4 0 obj<</Length 46>>stream\n"
            b"BT /F1 24 Tf 100 700 Td (Demo Legal Document) Tj ET\n"
            b"endstream\n"
            b"endobj\n"
            b"xref\n"
            b"0 5\n"
            b"0000000000 65535 f\n"
            b"0000000009 00000 n\n"
            b"0000000052 00000 n\n"
            b"0000000101 00000 n\n"
            b"0000000201 00000 n\n"
            b"trailer<</Size 5/Root 1 0 R>>\n"
            b"startxref\n"
            b"298\n"
            b"%%EOF"
        )

        seeded_count = 0
        for doc in Document.objects.all():
            if doc.file and not default_storage.exists(doc.file.name):
                _, ext = os.path.splitext(doc.file.name.lower())
                if ext == '.pdf':
                    content = MINIMAL_PDF
                else:
                    content = b"This is a placeholder for a demo legal document."
                
                default_storage.save(doc.file.name, ContentFile(content))
                seeded_count += 1
        
        if seeded_count > 0:
            self.stdout.write(self.style.SUCCESS(f'  Successfully seeded {seeded_count} mock files to storage.'))

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

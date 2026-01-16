"""
Tests for Document serializers.

Tests DocumentSerializer with valid and invalid data.
"""

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from cases.models import Case
from clients.models import Client
from documents.models import Document
from documents.serializers import DocumentSerializer


class DocumentSerializerTests(TestCase):
    """Tests for DocumentSerializer."""

    def setUp(self):
        """Create test client, case, and user for document relationships."""
        self.client_obj = Client.objects.create(
            full_name='Doc Serializer Client',
            identification_number='DOCSRC001',
            email='docsrc@example.com',
            phone='555-0000'
        )
        self.case = Case.objects.create(
            client=self.client_obj,
            title='Doc Serializer Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )
        self.user = User.objects.create_user(
            username='docseruser',
            email='docseruser@example.com',
            password='testpass123'
        )

    def test_serialize_document(self):
        """Test serializing a document instance."""
        test_file = SimpleUploadedFile('test.pdf', b'content', 'application/pdf')
        document = Document.objects.create(
            case=self.case,
            title='Serialize Test Doc',
            document_type='contrato',
            description='Test description',
            file=test_file,
            uploaded_by=self.user
        )
        serializer = DocumentSerializer(document)
        data = serializer.data

        self.assertEqual(data['title'], 'Serialize Test Doc')
        self.assertEqual(data['document_type'], 'contrato')
        self.assertIn('case_number', data)
        self.assertEqual(data['case_number'], self.case.case_number)
        self.assertIn('uploaded_by_username', data)
        self.assertEqual(data['uploaded_by_username'], 'docseruser')

    def test_serialize_file_size_included(self):
        """Test that file_size is included in serialized data."""
        content = b'Test content for size'
        test_file = SimpleUploadedFile('size.pdf', content, 'application/pdf')
        document = Document.objects.create(
            case=self.case,
            title='Size Test Doc',
            document_type='demanda',
            file=test_file
        )
        serializer = DocumentSerializer(document)
        data = serializer.data

        self.assertIn('file_size', data)
        self.assertEqual(data['file_size'], len(content))

    def test_deserialize_valid_data(self):
        """Test deserializing valid document data."""
        test_file = SimpleUploadedFile('new.pdf', b'new content', 'application/pdf')
        data = {
            'case': self.case.id,
            'title': 'New Document',
            'document_type': 'poder',
            'description': 'New document description',
            'file': test_file,
            'is_confidential': True
        }
        serializer = DocumentSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        document = serializer.save()
        self.assertEqual(document.title, 'New Document')
        self.assertTrue(document.is_confidential)

    def test_deserialize_invalid_document_type(self):
        """Test that invalid document_type is rejected."""
        test_file = SimpleUploadedFile('invalid.pdf', b'content', 'application/pdf')
        data = {
            'case': self.case.id,
            'title': 'Invalid Type Doc',
            'document_type': 'invalid_type',
            'file': test_file
        }
        serializer = DocumentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('document_type', serializer.errors)

    def test_file_size_read_only(self):
        """Test that file_size is read-only."""
        test_file = SimpleUploadedFile('readonly.pdf', b'content', 'application/pdf')
        data = {
            'case': self.case.id,
            'title': 'File Size Read Only',
            'document_type': 'sentencia',
            'file': test_file,
            'file_size': 999999  # Attempting to set read-only field
        }
        serializer = DocumentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        document = serializer.save()
        # file_size should be calculated from file, not the provided value
        self.assertNotEqual(document.file_size, 999999)
        self.assertEqual(document.file_size, len(b'content'))

    def test_uploaded_by_read_only(self):
        """Test that uploaded_by is read-only."""
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass123'
        )
        test_file = SimpleUploadedFile('uploader.pdf', b'content', 'application/pdf')
        data = {
            'case': self.case.id,
            'title': 'Uploader Read Only',
            'document_type': 'escritura',
            'file': test_file,
            'uploaded_by': other_user.id
        }
        serializer = DocumentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        document = serializer.save()
        # uploaded_by should not be set from data
        self.assertIsNone(document.uploaded_by)

    def test_uploaded_at_read_only(self):
        """Test that uploaded_at is read-only."""
        test_file = SimpleUploadedFile('time.pdf', b'content', 'application/pdf')
        data = {
            'case': self.case.id,
            'title': 'Time Read Only',
            'document_type': 'otro',
            'file': test_file,
            'uploaded_at': '2020-01-01T00:00:00Z'
        }
        serializer = DocumentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        document = serializer.save()
        # uploaded_at should be auto-set
        self.assertNotEqual(str(document.uploaded_at), '2020-01-01T00:00:00Z')

    def test_all_document_types_valid(self):
        """Test that all document types serialize correctly."""
        valid_types = ['contrato', 'demanda', 'poder', 'sentencia', 'escritura', 'otro']
        for doc_type in valid_types:
            test_file = SimpleUploadedFile(f'{doc_type}.pdf', b'content', 'application/pdf')
            document = Document.objects.create(
                case=self.case,
                title=f'{doc_type} doc',
                document_type=doc_type,
                file=test_file
            )
            serializer = DocumentSerializer(document)
            self.assertEqual(serializer.data['document_type'], doc_type)

    def test_uploaded_by_username_null_when_no_uploader(self):
        """Test that uploaded_by_username is null when no uploader."""
        test_file = SimpleUploadedFile('nouploader.pdf', b'content', 'application/pdf')
        document = Document.objects.create(
            case=self.case,
            title='No Uploader Doc',
            document_type='contrato',
            file=test_file,
            uploaded_by=None
        )
        serializer = DocumentSerializer(document)
        data = serializer.data

        self.assertIsNone(data['uploaded_by_username'])

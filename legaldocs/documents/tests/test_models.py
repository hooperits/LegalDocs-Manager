"""
Tests for Document model.

Tests document creation, file size calculation, and cascade deletion.
"""

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from cases.models import Case
from clients.models import Client
from documents.models import Document


class DocumentModelTests(TestCase):
    """Tests for the Document model."""

    def setUp(self):
        """Create test client, case, and user for document relationships."""
        self.client_obj = Client.objects.create(
            full_name='Document Test Client',
            identification_number='DOC001',
            email='doc@example.com',
            phone='555-0000'
        )
        self.case = Case.objects.create(
            client=self.client_obj,
            title='Document Test Case',
            description='Test case for documents',
            case_type='civil',
            start_date=timezone.now().date()
        )
        self.user = User.objects.create_user(
            username='docuser',
            email='docuser@example.com',
            password='testpass123'
        )

    def test_create_document_with_valid_data(self):
        """Test creating a document with all valid data."""
        test_file = SimpleUploadedFile(
            name='test_document.pdf',
            content=b'PDF content here',
            content_type='application/pdf'
        )
        document = Document.objects.create(
            case=self.case,
            title='Test Contract',
            document_type='contrato',
            description='Test contract description',
            file=test_file,
            uploaded_by=self.user,
            is_confidential=False
        )
        self.assertEqual(document.title, 'Test Contract')
        self.assertEqual(document.document_type, 'contrato')
        self.assertIsNotNone(document.uploaded_at)
        self.assertEqual(document.uploaded_by, self.user)

    def test_document_file_size_auto_calculated(self):
        """Test that file_size is automatically calculated on save."""
        content = b'This is test file content for size calculation'
        test_file = SimpleUploadedFile(
            name='size_test.txt',
            content=content,
            content_type='text/plain'
        )
        document = Document.objects.create(
            case=self.case,
            title='Size Test',
            document_type='otro',
            file=test_file
        )
        self.assertEqual(document.file_size, len(content))

    def test_document_str_method(self):
        """Test the __str__ method returns expected format."""
        test_file = SimpleUploadedFile(
            name='str_test.pdf',
            content=b'content',
            content_type='application/pdf'
        )
        document = Document.objects.create(
            case=self.case,
            title='My Demanda',
            document_type='demanda',
            file=test_file
        )
        self.assertEqual(str(document), 'Demanda: My Demanda')

    def test_document_default_is_confidential_false(self):
        """Test that is_confidential defaults to False."""
        test_file = SimpleUploadedFile(
            name='default_test.pdf',
            content=b'content',
            content_type='application/pdf'
        )
        document = Document.objects.create(
            case=self.case,
            title='Default Confidential Test',
            document_type='poder',
            file=test_file
        )
        self.assertFalse(document.is_confidential)

    def test_document_cascade_delete_with_case(self):
        """Test that documents are deleted when their case is deleted."""
        test_file = SimpleUploadedFile(
            name='cascade_test.pdf',
            content=b'content',
            content_type='application/pdf'
        )
        document = Document.objects.create(
            case=self.case,
            title='Cascade Test',
            document_type='sentencia',
            file=test_file
        )
        document_id = document.id

        # Delete the case
        self.case.delete()

        # Document should also be deleted
        self.assertFalse(Document.objects.filter(id=document_id).exists())

    def test_document_uploaded_by_can_be_null(self):
        """Test that uploaded_by can be null."""
        test_file = SimpleUploadedFile(
            name='null_uploader.pdf',
            content=b'content',
            content_type='application/pdf'
        )
        document = Document.objects.create(
            case=self.case,
            title='No Uploader',
            document_type='escritura',
            file=test_file,
            uploaded_by=None
        )
        self.assertIsNone(document.uploaded_by)

    def test_document_ordering_by_uploaded_at_descending(self):
        """Test that documents are ordered by uploaded_at descending."""
        file1 = SimpleUploadedFile('doc1.pdf', b'content1', 'application/pdf')
        file2 = SimpleUploadedFile('doc2.pdf', b'content2', 'application/pdf')

        doc1 = Document.objects.create(
            case=self.case,
            title='First Document',
            document_type='contrato',
            file=file1
        )
        doc2 = Document.objects.create(
            case=self.case,
            title='Second Document',
            document_type='contrato',
            file=file2
        )

        documents = list(Document.objects.all())
        # Most recent first
        self.assertEqual(documents[0], doc2)
        self.assertEqual(documents[1], doc1)

    def test_document_all_types_valid(self):
        """Test that all document types from choices are valid."""
        valid_types = ['contrato', 'demanda', 'poder', 'sentencia', 'escritura', 'otro']
        for doc_type in valid_types:
            test_file = SimpleUploadedFile(
                name=f'{doc_type}_test.pdf',
                content=b'content',
                content_type='application/pdf'
            )
            document = Document.objects.create(
                case=self.case,
                title=f'Type Test {doc_type}',
                document_type=doc_type,
                file=test_file
            )
            self.assertEqual(document.document_type, doc_type)

    def test_document_description_optional(self):
        """Test that description field is optional."""
        test_file = SimpleUploadedFile(
            name='no_desc.pdf',
            content=b'content',
            content_type='application/pdf'
        )
        document = Document.objects.create(
            case=self.case,
            title='No Description',
            document_type='otro',
            file=test_file,
            description=''
        )
        self.assertEqual(document.description, '')

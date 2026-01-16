"""
Tests for Case serializers.

Tests CaseSerializer and CaseDetailSerializer with valid and invalid data.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from cases.models import Case
from cases.serializers import CaseDetailSerializer, CaseSerializer
from clients.models import Client


class CaseSerializerTests(TestCase):
    """Tests for CaseSerializer."""

    def setUp(self):
        """Create test client for case relationships."""
        self.client_obj = Client.objects.create(
            full_name='Serializer Test Client',
            identification_number='SERTC001',
            email='sertc@example.com',
            phone='555-0000'
        )

    def test_serialize_case(self):
        """Test serializing a case instance."""
        case = Case.objects.create(
            client=self.client_obj,
            title='Serialize Test Case',
            description='Test description',
            case_type='civil',
            status='en_proceso',
            start_date=timezone.now().date()
        )
        serializer = CaseSerializer(case)
        data = serializer.data

        self.assertEqual(data['title'], 'Serialize Test Case')
        self.assertEqual(data['case_type'], 'civil')
        self.assertIn('case_number', data)
        self.assertIn('client_name', data)
        self.assertEqual(data['client_name'], 'Serializer Test Client')

    def test_deserialize_valid_data(self):
        """Test deserializing valid case data."""
        data = {
            'client': self.client_obj.id,
            'title': 'New Case',
            'description': 'New case description',
            'case_type': 'penal',
            'status': 'en_proceso',
            'priority': 'alta',
            'start_date': timezone.now().date().isoformat()
        }
        serializer = CaseSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        case = serializer.save()
        self.assertEqual(case.title, 'New Case')
        self.assertEqual(case.case_type, 'penal')

    def test_deserialize_invalid_case_type(self):
        """Test that invalid case_type is rejected."""
        data = {
            'client': self.client_obj.id,
            'title': 'Invalid Type',
            'description': 'Test',
            'case_type': 'invalid_type',
            'start_date': timezone.now().date().isoformat()
        }
        serializer = CaseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('case_type', serializer.errors)

    def test_deserialize_invalid_status(self):
        """Test that invalid status is rejected."""
        data = {
            'client': self.client_obj.id,
            'title': 'Invalid Status',
            'description': 'Test',
            'case_type': 'civil',
            'status': 'invalid_status',
            'start_date': timezone.now().date().isoformat()
        }
        serializer = CaseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_case_number_read_only(self):
        """Test that case_number is read-only."""
        data = {
            'client': self.client_obj.id,
            'title': 'Read Only Case Number',
            'description': 'Test',
            'case_type': 'civil',
            'start_date': timezone.now().date().isoformat(),
            'case_number': 'CUSTOM-001'
        }
        serializer = CaseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        case = serializer.save()
        # case_number should be auto-generated, not the custom value
        self.assertNotEqual(case.case_number, 'CUSTOM-001')
        self.assertTrue(case.case_number.startswith('CASE-'))


class CaseDetailSerializerTests(TestCase):
    """Tests for CaseDetailSerializer."""

    def setUp(self):
        """Create test client for case relationships."""
        self.client_obj = Client.objects.create(
            full_name='Detail Serializer Client',
            identification_number='DETSRC001',
            email='detsrc@example.com',
            phone='555-0001'
        )

    def test_serialize_includes_nested_client(self):
        """Test that detail serializer includes nested client data."""
        case = Case.objects.create(
            client=self.client_obj,
            title='Detail Test Case',
            description='Test',
            case_type='laboral',
            start_date=timezone.now().date()
        )
        serializer = CaseDetailSerializer(case)
        data = serializer.data

        self.assertIn('client', data)
        self.assertIsInstance(data['client'], dict)
        self.assertEqual(data['client']['full_name'], 'Detail Serializer Client')

    def test_serialize_includes_documents_list(self):
        """Test that detail serializer includes documents list."""
        from django.core.files.uploadedfile import SimpleUploadedFile
        from documents.models import Document

        case = Case.objects.create(
            client=self.client_obj,
            title='Documents Test Case',
            description='Test',
            case_type='mercantil',
            start_date=timezone.now().date()
        )
        # Create a document
        test_file = SimpleUploadedFile('test.pdf', b'content', 'application/pdf')
        Document.objects.create(
            case=case,
            title='Test Document',
            document_type='contrato',
            file=test_file
        )

        serializer = CaseDetailSerializer(case)
        data = serializer.data

        self.assertIn('documents', data)
        self.assertEqual(len(data['documents']), 1)
        self.assertEqual(data['documents'][0]['title'], 'Test Document')

    def test_deserialize_with_client_id(self):
        """Test deserializing with client_id write-only field."""
        data = {
            'client_id': self.client_obj.id,
            'title': 'Client ID Test',
            'description': 'Test',
            'case_type': 'familia',
            'start_date': timezone.now().date().isoformat()
        }
        serializer = CaseDetailSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        case = serializer.save()
        self.assertEqual(case.client, self.client_obj)

    def test_all_case_types_valid(self):
        """Test that all case types from choices serialize correctly."""
        valid_types = ['civil', 'penal', 'laboral', 'mercantil', 'familia']
        for case_type in valid_types:
            case = Case.objects.create(
                client=self.client_obj,
                title=f'{case_type} case',
                description='Test',
                case_type=case_type,
                start_date=timezone.now().date()
            )
            serializer = CaseSerializer(case)
            self.assertEqual(serializer.data['case_type'], case_type)

    def test_all_status_values_valid(self):
        """Test that all status values serialize correctly."""
        valid_statuses = ['en_proceso', 'pendiente_documentos', 'en_revision', 'cerrado']
        for status in valid_statuses:
            case = Case.objects.create(
                client=self.client_obj,
                title=f'{status} case',
                description='Test',
                case_type='civil',
                status=status,
                start_date=timezone.now().date()
            )
            serializer = CaseSerializer(case)
            self.assertEqual(serializer.data['status'], status)

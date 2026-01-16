"""
Tests for DocumentViewSet.

Tests CRUD operations, file uploads, and IsOwnerOrReadOnly permission.
"""

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cases.models import Case
from clients.models import Client
from documents.models import Document


class DocumentViewSetTests(APITestCase):
    """Tests for DocumentViewSet."""

    def setUp(self):
        """Create test user, client, case, and documents."""
        self.user = User.objects.create_user(
            username='docuser',
            email='docuser@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.client_obj = Client.objects.create(
            full_name='Doc Test Client',
            identification_number='DTC001',
            email='dtc@example.com',
            phone='555-0000'
        )
        self.case = Case.objects.create(
            client=self.client_obj,
            title='Doc Test Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )

        test_file = SimpleUploadedFile('test.pdf', b'test content', 'application/pdf')
        self.document = Document.objects.create(
            case=self.case,
            title='Test Document',
            document_type='contrato',
            file=test_file,
            uploaded_by=self.user
        )

    def test_list_documents(self):
        """Test listing all documents."""
        response = self.client.get('/api/v1/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_document_with_file(self):
        """Test creating a document with file upload."""
        test_file = SimpleUploadedFile('new.pdf', b'new content', 'application/pdf')
        data = {
            'case': self.case.id,
            'title': 'New Document',
            'document_type': 'demanda',
            'file': test_file
        }
        response = self.client.post('/api/v1/documents/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Document')
        self.assertIn('file_size', response.data)
        # uploaded_by should be auto-set
        self.assertEqual(response.data['uploaded_by'], self.user.id)

    def test_retrieve_document(self):
        """Test retrieving a single document."""
        response = self.client.get(f'/api/v1/documents/{self.document.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Document')
        self.assertIn('case_number', response.data)

    def test_update_document(self):
        """Test updating a document."""
        test_file = SimpleUploadedFile('updated.pdf', b'updated', 'application/pdf')
        data = {
            'case': self.case.id,
            'title': 'Updated Document',
            'document_type': 'poder',
            'file': test_file
        }
        response = self.client.put(
            f'/api/v1/documents/{self.document.id}/',
            data,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Document')

    def test_partial_update_document(self):
        """Test partially updating a document."""
        data = {'is_confidential': True}
        response = self.client.patch(f'/api/v1/documents/{self.document.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_confidential'])

    def test_delete_own_document(self):
        """Test that owner can delete their document."""
        response = self.client.delete(f'/api/v1/documents/{self.document.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Document.objects.filter(id=self.document.id).exists())

    def test_filter_by_case(self):
        """Test filtering documents by case."""
        response = self.client.get(f'/api/v1/documents/?case={self.case.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_document_type(self):
        """Test filtering documents by document_type."""
        response = self.client.get('/api/v1/documents/?document_type=contrato')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_is_confidential(self):
        """Test filtering documents by is_confidential."""
        response = self.client.get('/api/v1/documents/?is_confidential=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_by_title(self):
        """Test searching documents by title."""
        response = self.client.get('/api/v1/documents/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class DocumentPermissionTests(APITestCase):
    """Tests for IsOwnerOrReadOnly permission on DocumentViewSet."""

    def setUp(self):
        """Create two users, one document owned by user1."""
        self.user1 = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='testpass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        self.client_obj = Client.objects.create(
            full_name='Permission Test Client',
            identification_number='PTC001',
            email='ptc@example.com',
            phone='555-0000'
        )
        self.case = Case.objects.create(
            client=self.client_obj,
            title='Permission Test Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )

        test_file = SimpleUploadedFile('owner.pdf', b'content', 'application/pdf')
        self.document = Document.objects.create(
            case=self.case,
            title='Owner Document',
            document_type='contrato',
            file=test_file,
            uploaded_by=self.user1
        )

    def test_non_owner_can_read_document(self):
        """Test that non-owner can read documents."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.get(f'/api/v1/documents/{self.document.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_delete_document(self):
        """Test that non-owner cannot delete documents."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.delete(f'/api/v1/documents/{self.document.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_document(self):
        """Test that owner can delete their own documents."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.delete(f'/api/v1/documents/{self.document.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_staff_can_delete_any_document(self):
        """Test that staff can delete any document."""
        self.user2.is_staff = True
        self.user2.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.delete(f'/api/v1/documents/{self.document.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DocumentViewSetUnauthenticatedTests(APITestCase):
    """Tests for unauthenticated access to DocumentViewSet."""

    def test_list_documents_unauthenticated(self):
        """Test that unauthenticated users cannot list documents."""
        response = self.client.get('/api/v1/documents/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_document_unauthenticated(self):
        """Test that unauthenticated users cannot create documents."""
        client_obj = Client.objects.create(
            full_name='Unauth Doc Client',
            identification_number='UDC001',
            email='udc@example.com',
            phone='555-0000'
        )
        case = Case.objects.create(
            client=client_obj,
            title='Unauth Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )
        test_file = SimpleUploadedFile('unauth.pdf', b'content', 'application/pdf')
        data = {
            'case': case.id,
            'title': 'Unauthorized Doc',
            'document_type': 'contrato',
            'file': test_file
        }
        response = self.client.post('/api/v1/documents/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

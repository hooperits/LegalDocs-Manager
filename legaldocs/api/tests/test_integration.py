"""
Integration tests for LegalDocs Manager API.

Tests complete workflows across multiple endpoints:
- Client → Case → Document creation workflow
- Dashboard statistics accuracy
- Global search functionality
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


class ClientCaseDocumentWorkflowTests(APITestCase):
    """Integration tests for the complete client → case → document workflow."""

    def setUp(self):
        """Create test user and authenticate."""
        self.user = User.objects.create_user(
            username='workflowuser',
            email='workflow@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_complete_workflow_create_client_case_document(self):
        """Test creating a client, then a case, then uploading a document."""
        # Step 1: Create a client
        client_data = {
            'full_name': 'Integration Test Client',
            'identification_number': 'INT-001',
            'email': 'integration@example.com',
            'phone': '555-1234'
        }
        response = self.client.post('/api/v1/clients/', client_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client_id = response.data['id']

        # Step 2: Create a case for the client
        case_data = {
            'client': client_id,
            'title': 'Integration Test Case',
            'description': 'Testing the complete workflow',
            'case_type': 'civil',
            'start_date': timezone.now().date().isoformat()
        }
        response = self.client.post('/api/v1/cases/', case_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        case_id = response.data['id']
        case_number = response.data['case_number']
        self.assertTrue(case_number.startswith('CASE-'))

        # Step 3: Upload a document to the case
        test_file = SimpleUploadedFile('test.pdf', b'PDF content', 'application/pdf')
        doc_data = {
            'case': case_id,
            'title': 'Integration Test Document',
            'document_type': 'contrato',
            'file': test_file
        }
        response = self.client.post('/api/v1/documents/', doc_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doc_id = response.data['id']
        self.assertEqual(response.data['case_number'], case_number)
        self.assertEqual(response.data['uploaded_by'], self.user.id)

        # Step 4: Verify client's cases endpoint shows the case
        response = self.client.get(f'/api/v1/clients/{client_id}/cases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], case_id)

        # Step 5: Verify case detail shows the document
        response = self.client.get(f'/api/v1/cases/{case_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['documents']), 1)
        self.assertEqual(response.data['documents'][0]['id'], doc_id)

        # Step 6: Close the case
        response = self.client.post(f'/api/v1/cases/{case_id}/close/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'cerrado')
        self.assertIsNotNone(response.data['closed_date'])

    def test_workflow_document_upload_sets_file_size(self):
        """Test that document file_size is correctly calculated in workflow."""
        # Create client and case first
        client = Client.objects.create(
            full_name='File Size Test Client',
            identification_number='FST-001',
            email='filesize@example.com',
            phone='555-0000'
        )
        case = Case.objects.create(
            client=client,
            title='File Size Test Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )

        # Upload document with known content size
        content = b'X' * 1024  # 1KB file
        test_file = SimpleUploadedFile('size_test.pdf', content, 'application/pdf')
        doc_data = {
            'case': case.id,
            'title': 'Size Test Document',
            'document_type': 'otro',
            'file': test_file
        }
        response = self.client.post('/api/v1/documents/', doc_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['file_size'], 1024)

    def test_workflow_cascade_delete_case(self):
        """Test that deleting a case cascades to documents."""
        # Create complete hierarchy
        client = Client.objects.create(
            full_name='Cascade Delete Client',
            identification_number='CDC-001',
            email='cascade@example.com',
            phone='555-0000'
        )
        case = Case.objects.create(
            client=client,
            title='Cascade Delete Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )
        test_file = SimpleUploadedFile('cascade.pdf', b'content', 'application/pdf')
        doc = Document.objects.create(
            case=case,
            title='Cascade Delete Document',
            document_type='contrato',
            file=test_file
        )

        # Record IDs
        case_id = case.id
        doc_id = doc.id

        # Delete case via API (should cascade delete documents)
        response = self.client.delete(f'/api/v1/cases/{case_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify cascade - case and document deleted
        self.assertFalse(Case.objects.filter(id=case_id).exists())
        self.assertFalse(Document.objects.filter(id=doc_id).exists())


class DashboardAccuracyTests(APITestCase):
    """Integration tests for dashboard statistics accuracy."""

    def setUp(self):
        """Create test user and authenticate."""
        self.user = User.objects.create_user(
            username='dashboarduser',
            email='dashboard@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_dashboard_client_counts(self):
        """Test that dashboard shows correct client counts."""
        # Create mix of active and inactive clients
        Client.objects.create(
            full_name='Active Client 1',
            identification_number='AC1',
            email='ac1@example.com',
            phone='555-0001',
            is_active=True
        )
        Client.objects.create(
            full_name='Active Client 2',
            identification_number='AC2',
            email='ac2@example.com',
            phone='555-0002',
            is_active=True
        )
        Client.objects.create(
            full_name='Inactive Client',
            identification_number='IC1',
            email='ic1@example.com',
            phone='555-0003',
            is_active=False
        )

        response = self.client.get('/api/v1/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_clients'], 3)
        self.assertEqual(response.data['active_clients'], 2)

    def test_dashboard_case_counts_by_status(self):
        """Test that dashboard shows correct case counts by status."""
        client = Client.objects.create(
            full_name='Dashboard Case Client',
            identification_number='DCC1',
            email='dcc@example.com',
            phone='555-0000'
        )

        # Create cases with different statuses
        statuses = ['en_proceso', 'en_proceso', 'pendiente_documentos', 'cerrado']
        for i, status_val in enumerate(statuses):
            Case.objects.create(
                client=client,
                title=f'Status Test Case {i}',
                description='Test',
                case_type='civil',
                status=status_val,
                start_date=timezone.now().date()
            )

        response = self.client.get('/api/v1/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cases_by_status']['en_proceso'], 2)
        self.assertEqual(response.data['cases_by_status']['pendiente_documentos'], 1)
        self.assertEqual(response.data['cases_by_status']['cerrado'], 1)

    def test_dashboard_document_count(self):
        """Test that dashboard shows correct document count by type."""
        client = Client.objects.create(
            full_name='Dashboard Doc Client',
            identification_number='DDC1',
            email='ddc@example.com',
            phone='555-0000'
        )
        case = Case.objects.create(
            client=client,
            title='Dashboard Doc Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )

        # Create multiple documents
        for i in range(5):
            test_file = SimpleUploadedFile(f'doc{i}.pdf', b'content', 'application/pdf')
            Document.objects.create(
                case=case,
                title=f'Dashboard Doc {i}',
                document_type='otro',
                file=test_file
            )

        response = self.client.get('/api/v1/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Dashboard returns documents_by_type dict
        self.assertIn('documents_by_type', response.data)
        self.assertEqual(response.data['documents_by_type'].get('otro', 0), 5)

    def test_dashboard_recent_cases(self):
        """Test that dashboard shows recent cases."""
        client = Client.objects.create(
            full_name='Recent Cases Client',
            identification_number='RCC1',
            email='rcc@example.com',
            phone='555-0000'
        )

        # Create cases
        for i in range(3):
            Case.objects.create(
                client=client,
                title=f'Recent Case {i}',
                description='Test',
                case_type='civil',
                start_date=timezone.now().date()
            )

        response = self.client.get('/api/v1/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('recent_cases', response.data)
        self.assertGreater(len(response.data['recent_cases']), 0)


class SearchFunctionalityTests(APITestCase):
    """Integration tests for global search functionality."""

    def setUp(self):
        """Create test user, authenticate, and create test data."""
        self.user = User.objects.create_user(
            username='searchuser',
            email='search@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create test data with searchable content
        self.client_garcia = Client.objects.create(
            full_name='Juan García López',
            identification_number='JGL-001',
            email='juan.garcia@example.com',
            phone='555-0001'
        )
        self.client_martinez = Client.objects.create(
            full_name='María Martínez Ruiz',
            identification_number='MMR-002',
            email='maria.martinez@example.com',
            phone='555-0002'
        )

        self.case_garcia = Case.objects.create(
            client=self.client_garcia,
            title='García vs Empresa ABC',
            description='Demanda laboral García',
            case_type='laboral',
            start_date=timezone.now().date()
        )
        self.case_martinez = Case.objects.create(
            client=self.client_martinez,
            title='Divorcio Martínez',
            description='Caso de familia Martínez',
            case_type='familia',
            start_date=timezone.now().date()
        )

        test_file = SimpleUploadedFile('poder_garcia.pdf', b'content', 'application/pdf')
        self.document_garcia = Document.objects.create(
            case=self.case_garcia,
            title='Poder García',
            document_type='poder',
            file=test_file
        )

    def test_search_finds_clients_by_name(self):
        """Test that search finds clients by name."""
        response = self.client.get('/api/v1/search/?q=García')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']['clients']), 1)
        self.assertEqual(response.data['results']['clients'][0]['full_name'], 'Juan García López')

    def test_search_finds_cases_by_title(self):
        """Test that search finds cases by title."""
        response = self.client.get('/api/v1/search/?q=Divorcio')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']['cases']), 1)
        self.assertEqual(response.data['results']['cases'][0]['title'], 'Divorcio Martínez')

    def test_search_finds_documents_by_title(self):
        """Test that search finds documents by title."""
        response = self.client.get('/api/v1/search/?q=Poder')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']['documents']), 1)
        self.assertEqual(response.data['results']['documents'][0]['title'], 'Poder García')

    def test_search_returns_multiple_types(self):
        """Test that search can return results across multiple types."""
        response = self.client.get('/api/v1/search/?q=García')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should find client, case, and document all containing "García"
        self.assertGreater(len(response.data['results']['clients']), 0)
        self.assertGreater(len(response.data['results']['cases']), 0)
        self.assertGreater(len(response.data['results']['documents']), 0)

    def test_search_requires_minimum_query_length(self):
        """Test that search requires minimum query length."""
        response = self.client.get('/api/v1/search/?q=a')
        # Should either return empty results or 400
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_search_empty_query_returns_error_or_empty(self):
        """Test that search with no query returns error or empty results."""
        response = self.client.get('/api/v1/search/')
        # Should either return empty results or 400
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        # Use lowercase search
        response = self.client.get('/api/v1/search/?q=juan')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']['clients']), 0)

        # Use uppercase search
        response = self.client.get('/api/v1/search/?q=JUAN')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']['clients']), 0)


class AuthenticationWorkflowTests(APITestCase):
    """Integration tests for authentication workflow."""

    def test_full_auth_workflow(self):
        """Test complete authentication flow: register → login → access → logout."""
        # Step 1: Register
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        response = self.client.post('/api/v1/auth/register/', register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        token = response.data['token']

        # Step 2: Access protected endpoint with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newuser')

        # Step 3: Access dashboard
        response = self.client.get('/api/v1/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 4: Logout
        response = self.client.post('/api/v1/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 5: Verify token is invalidated (can't access protected endpoints)
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_and_access_resources(self):
        """Test login and accessing resources with valid token."""
        # Create user
        User.objects.create_user(
            username='logintest',
            email='login@example.com',
            password='testpass123'
        )

        # Login
        login_data = {
            'username': 'logintest',
            'password': 'testpass123'
        }
        response = self.client.post('/api/v1/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        # Use token to access protected resource
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get('/api/v1/clients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_credentials_login(self):
        """Test login with invalid credentials."""
        User.objects.create_user(
            username='validuser',
            email='valid@example.com',
            password='correctpass'
        )

        login_data = {
            'username': 'validuser',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/v1/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

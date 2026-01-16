"""
Tests for ClientViewSet.

Tests CRUD operations, filtering, search, and custom actions.
"""

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cases.models import Case
from clients.models import Client


class ClientViewSetTests(APITestCase):
    """Tests for ClientViewSet."""

    def setUp(self):
        """Create test user and clients."""
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.client1 = Client.objects.create(
            full_name='Juan García',
            identification_number='JG001',
            email='juan@example.com',
            phone='555-0001',
            is_active=True
        )
        self.client2 = Client.objects.create(
            full_name='María López',
            identification_number='ML002',
            email='maria@example.com',
            phone='555-0002',
            is_active=False
        )

    def test_list_clients(self):
        """Test listing all clients."""
        response = self.client.get('/api/v1/clients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_create_client(self):
        """Test creating a new client."""
        data = {
            'full_name': 'New Client',
            'identification_number': 'NC001',
            'email': 'newclient@example.com',
            'phone': '555-0003'
        }
        response = self.client.post('/api/v1/clients/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], 'New Client')
        self.assertTrue(Client.objects.filter(identification_number='NC001').exists())

    def test_retrieve_client(self):
        """Test retrieving a single client."""
        response = self.client.get(f'/api/v1/clients/{self.client1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Juan García')
        # Detail view should include notes and case_count
        self.assertIn('notes', response.data)
        self.assertIn('case_count', response.data)

    def test_update_client(self):
        """Test updating a client with PUT."""
        data = {
            'full_name': 'Juan García Updated',
            'identification_number': 'JG001',
            'email': 'juan.updated@example.com',
            'phone': '555-0001-updated'
        }
        response = self.client.put(f'/api/v1/clients/{self.client1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Juan García Updated')

    def test_partial_update_client(self):
        """Test partially updating a client with PATCH."""
        data = {'email': 'patched@example.com'}
        response = self.client.patch(f'/api/v1/clients/{self.client1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'patched@example.com')

    def test_delete_client(self):
        """Test deleting a client."""
        response = self.client.delete(f'/api/v1/clients/{self.client2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client2.id).exists())

    def test_filter_by_is_active(self):
        """Test filtering clients by is_active status."""
        response = self.client.get('/api/v1/clients/?is_active=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'Juan García')

        response = self.client.get('/api/v1/clients/?is_active=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'María López')

    def test_search_by_full_name(self):
        """Test searching clients by full_name."""
        response = self.client.get('/api/v1/clients/?search=García')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'Juan García')

    def test_search_by_email(self):
        """Test searching clients by email."""
        response = self.client.get('/api/v1/clients/?search=maria@')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['full_name'], 'María López')

    def test_search_by_identification_number(self):
        """Test searching clients by identification_number."""
        response = self.client.get('/api/v1/clients/?search=JG001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_ordering_by_full_name(self):
        """Test ordering clients by full_name."""
        response = self.client.get('/api/v1/clients/?ordering=full_name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [r['full_name'] for r in response.data['results']]
        self.assertEqual(names, sorted(names))

    def test_cases_custom_action(self):
        """Test the cases custom action returns client's cases."""
        # Create a case for client1
        Case.objects.create(
            client=self.client1,
            title='Test Case',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )
        response = self.client.get(f'/api/v1/clients/{self.client1.id}/cases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Case')


class ClientViewSetUnauthenticatedTests(APITestCase):
    """Tests for unauthenticated access to ClientViewSet."""

    def test_list_clients_unauthenticated(self):
        """Test that unauthenticated users cannot list clients."""
        response = self.client.get('/api/v1/clients/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_client_unauthenticated(self):
        """Test that unauthenticated users cannot create clients."""
        data = {
            'full_name': 'Unauthorized',
            'identification_number': 'UN001',
            'email': 'unauth@example.com',
            'phone': '555-0000'
        }
        response = self.client.post('/api/v1/clients/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_client_unauthenticated(self):
        """Test that unauthenticated users cannot retrieve clients."""
        client_obj = Client.objects.create(
            full_name='Test',
            identification_number='TEST001',
            email='test@example.com',
            phone='555-0000'
        )
        response = self.client.get(f'/api/v1/clients/{client_obj.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

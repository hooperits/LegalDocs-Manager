"""
Tests for search endpoint.

Tests global search across clients, cases, and documents.
"""

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cases.models import Case
from clients.models import Client


class SearchTests(APITestCase):
    """Tests for the search endpoint."""

    def setUp(self):
        """Create test user and sample data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)

        # Create sample clients
        self.client1 = Client.objects.create(
            full_name='Juan García',
            identification_number='12345678',
            email='juan.garcia@example.com',
            phone='555-1234',
            is_active=True
        )
        self.client2 = Client.objects.create(
            full_name='María López',
            identification_number='87654321',
            email='maria@example.com',
            phone='555-5678',
            is_active=True
        )

        # Create sample cases
        self.case1 = Case.objects.create(
            client=self.client1,
            title='García vs Smith',
            description='Descripción del caso',
            case_type='civil',
            status='en_proceso',
            start_date=timezone.now().date()
        )
        self.case2 = Case.objects.create(
            client=self.client2,
            title='Caso de familia López',
            description='Descripción del caso',
            case_type='familia',
            status='en_proceso',
            start_date=timezone.now().date()
        )

    def test_search_clients_by_name(self):
        """Test search finds clients by name."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/?q=García')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['query'], 'García')
        self.assertGreater(len(response.data['results']['clients']), 0)

        client_result = response.data['results']['clients'][0]
        self.assertEqual(client_result['type'], 'client')
        self.assertEqual(client_result['full_name'], 'Juan García')

    def test_search_clients_by_email(self):
        """Test search finds clients by email."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/?q=garcia@example')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']['clients']), 0)

    def test_search_cases_by_title(self):
        """Test search finds cases by title."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/?q=García')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']['cases']), 0)

        case_result = response.data['results']['cases'][0]
        self.assertEqual(case_result['type'], 'case')
        self.assertIn('García', case_result['title'])

    def test_search_cases_by_case_number(self):
        """Test search finds cases by case number."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        case_number = self.case1.case_number
        response = self.client.get(f'/api/v1/search/?q={case_number}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']['cases']), 0)

    def test_search_unified_results(self):
        """Test search returns unified results from all models."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/?q=García')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('clients', response.data['results'])
        self.assertIn('cases', response.data['results'])
        self.assertIn('documents', response.data['results'])
        self.assertIn('counts', response.data)
        self.assertIn('total', response.data['counts'])

    def test_search_limit_results(self):
        """Test search limits results to 10 per model."""
        # Create 15 clients with same name pattern
        for i in range(15):
            Client.objects.create(
                full_name=f'Test García {i}',
                identification_number=f'TEST{i:04d}',
                email=f'test{i}@example.com',
                phone='555-0000',
                is_active=True
            )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/?q=García')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data['results']['clients']), 10)

    def test_search_empty_query(self):
        """Test search with empty query returns 400."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/?q=')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_search_missing_query(self):
        """Test search without query parameter returns 400."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_no_results(self):
        """Test search with no matching results returns empty lists."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/search/?q=nonexistentterm12345')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']['clients']), 0)
        self.assertEqual(len(response.data['results']['cases']), 0)
        self.assertEqual(len(response.data['results']['documents']), 0)
        self.assertEqual(response.data['counts']['total'], 0)

    def test_search_without_auth(self):
        """Test search without authentication returns 401."""
        response = self.client.get('/api/v1/search/?q=test')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_case_insensitive(self):
        """Test search is case insensitive."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Search with lowercase (using ASCII to ensure consistent behavior across DBs)
        response1 = self.client.get('/api/v1/search/?q=maria')
        # Search with uppercase
        response2 = self.client.get('/api/v1/search/?q=MARIA')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        # Both should find the same client (María López)
        self.assertEqual(
            response1.data['counts']['clients'],
            response2.data['counts']['clients']
        )

"""
Tests for dashboard endpoint.

Tests dashboard statistics with various data scenarios.
"""

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cases.models import Case
from clients.models import Client


class DashboardTests(APITestCase):
    """Tests for the dashboard endpoint."""

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
            email='juan@example.com',
            phone='555-1234',
            is_active=True
        )
        self.client2 = Client.objects.create(
            full_name='María López',
            identification_number='87654321',
            email='maria@example.com',
            phone='555-5678',
            is_active=False
        )

        # Create sample cases
        today = timezone.now().date()
        self.case1 = Case.objects.create(
            client=self.client1,
            title='Caso Civil 1',
            description='Descripción del caso',
            case_type='civil',
            status='en_proceso',
            start_date=today,
            deadline=today + timedelta(days=5)
        )
        self.case2 = Case.objects.create(
            client=self.client1,
            title='Caso Penal 1',
            description='Descripción del caso',
            case_type='penal',
            status='cerrado',
            start_date=today - timedelta(days=30)
        )

    def test_dashboard_success(self):
        """Test dashboard returns all required statistics."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/dashboard/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_clients', response.data)
        self.assertIn('active_clients', response.data)
        self.assertIn('cases_by_status', response.data)
        self.assertIn('cases_by_type', response.data)
        self.assertIn('recent_cases', response.data)
        self.assertIn('documents_by_type', response.data)
        self.assertIn('upcoming_deadlines', response.data)

    def test_dashboard_client_counts(self):
        """Test dashboard returns correct client counts."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/dashboard/')

        self.assertEqual(response.data['total_clients'], 2)
        self.assertEqual(response.data['active_clients'], 1)

    def test_dashboard_cases_by_status(self):
        """Test dashboard returns correct cases by status."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/dashboard/')

        cases_by_status = response.data['cases_by_status']
        self.assertEqual(cases_by_status.get('en_proceso', 0), 1)
        self.assertEqual(cases_by_status.get('cerrado', 0), 1)

    def test_dashboard_cases_by_type(self):
        """Test dashboard returns correct cases by type."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/dashboard/')

        cases_by_type = response.data['cases_by_type']
        self.assertEqual(cases_by_type.get('civil', 0), 1)
        self.assertEqual(cases_by_type.get('penal', 0), 1)

    def test_dashboard_recent_cases(self):
        """Test dashboard returns recent cases with correct structure."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/dashboard/')

        recent_cases = response.data['recent_cases']
        self.assertIsInstance(recent_cases, list)
        self.assertLessEqual(len(recent_cases), 5)
        if recent_cases:
            case = recent_cases[0]
            self.assertIn('id', case)
            self.assertIn('case_number', case)
            self.assertIn('title', case)
            self.assertIn('status', case)
            self.assertIn('client_name', case)

    def test_dashboard_upcoming_deadlines(self):
        """Test dashboard returns upcoming deadlines correctly."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/dashboard/')

        upcoming = response.data['upcoming_deadlines']
        self.assertIsInstance(upcoming, list)
        # Case 1 has deadline in 5 days, should appear
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0]['title'], 'Caso Civil 1')

    def test_dashboard_without_auth(self):
        """Test dashboard without authentication returns 401."""
        response = self.client.get('/api/v1/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_empty_data(self):
        """Test dashboard with no data returns empty/zero values."""
        # Delete all data
        Case.objects.all().delete()
        Client.objects.all().delete()

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/dashboard/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_clients'], 0)
        self.assertEqual(response.data['active_clients'], 0)

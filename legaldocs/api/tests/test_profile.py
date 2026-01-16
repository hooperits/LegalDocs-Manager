"""
Tests for profile endpoint.

Tests profile get and update functionality.
"""

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cases.models import Case
from clients.models import Client


class ProfileTests(APITestCase):
    """Tests for the profile endpoint."""

    def setUp(self):
        """Create test user with token."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.token = Token.objects.create(user=self.user)

    def test_get_profile_success(self):
        """Test get profile returns user data with assigned cases count."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertIn('assigned_cases_count', response.data)
        self.assertIn('date_joined', response.data)

    def test_get_profile_assigned_cases_count(self):
        """Test profile returns correct assigned cases count."""
        # Create a client and cases assigned to this user
        test_client = Client.objects.create(
            full_name='Test Client',
            identification_number='12345678',
            email='client@example.com',
            phone='555-1234',
            is_active=True
        )
        Case.objects.create(
            client=test_client,
            title='Case 1',
            description='Description',
            case_type='civil',
            status='en_proceso',
            start_date=timezone.now().date(),
            assigned_to=self.user
        )
        Case.objects.create(
            client=test_client,
            title='Case 2',
            description='Description',
            case_type='penal',
            status='en_proceso',
            start_date=timezone.now().date(),
            assigned_to=self.user
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/v1/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['assigned_cases_count'], 2)

    def test_update_profile_email(self):
        """Test update profile email via PATCH."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch('/api/v1/profile/', {
            'email': 'newemail@example.com'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'newemail@example.com')

        # Verify in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_update_profile_name(self):
        """Test update profile first and last name via PATCH."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch('/api/v1/profile/', {
            'first_name': 'Updated',
            'last_name': 'Name'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'Name')

        # Verify in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_update_profile_multiple_fields(self):
        """Test update multiple profile fields at once."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch('/api/v1/profile/', {
            'email': 'multi@example.com',
            'first_name': 'Multi',
            'last_name': 'Update'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'multi@example.com')
        self.assertEqual(response.data['first_name'], 'Multi')
        self.assertEqual(response.data['last_name'], 'Update')

    def test_update_profile_username_readonly(self):
        """Test username is read-only and cannot be changed."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch('/api/v1/profile/', {
            'username': 'newusername'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Username should remain unchanged
        self.assertEqual(response.data['username'], 'testuser')

        # Verify in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')

    def test_get_profile_without_auth(self):
        """Test get profile without authentication returns 401."""
        response = self.client.get('/api/v1/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_without_auth(self):
        """Test update profile without authentication returns 401."""
        response = self.client.patch('/api/v1/profile/', {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_date_joined_readonly(self):
        """Test date_joined is read-only."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        original_date = self.user.date_joined

        response = self.client.patch('/api/v1/profile/', {
            'date_joined': '2020-01-01T00:00:00Z'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Date should remain unchanged
        self.user.refresh_from_db()
        self.assertEqual(self.user.date_joined, original_date)

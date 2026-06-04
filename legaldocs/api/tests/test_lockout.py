"""
Tests for account lockout protection (django-axes).
"""

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from axes.utils import reset


class LockoutTests(APITestCase):
    """Test suite for verifying brute-force protection and account lockout."""

    def setUp(self):
        """Set up test users and clear any existing axes lockout records."""
        reset()
        self.username = 'lockoutuser'
        self.password = 'securepass123'
        self.user = User.objects.create_user(
            username=self.username,
            email='lockout@example.com',
            password=self.password
        )

    def tearDown(self):
        """Clean up lockout records after each test."""
        reset()

    def test_account_lockout_after_five_failures(self):
        """Test that 5 failed login attempts trigger a lockout on the 6th attempt."""
        login_url = '/api/v1/auth/login/'

        # Send 5 failed login attempts (wrong password)
        for _ in range(5):
            response = self.client.post(login_url, {
                'username': self.username,
                'password': 'wrongpassword'
            })
            # First 5 attempts return 400 Bad Request
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 6th attempt should trigger a lockout and return 403 Forbidden
        response = self.client.post(login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        }, HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())
        self.assertIn('Account locked out', response.json()['detail'])

    def test_lockout_spanish_translation(self):
        """Test that the custom JSON lockout response is translated to Spanish when requested."""
        login_url = '/api/v1/auth/login/'

        # Trigger lockout
        for _ in range(5):
            self.client.post(login_url, {
                'username': self.username,
                'password': 'wrongpassword'
            })

        # 6th request with Spanish header
        response = self.client.post(login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        }, HTTP_ACCEPT_LANGUAGE='es')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detalle', response.json())
        self.assertIn('Cuenta bloqueada', response.json()['detalle'])

    def test_reset_on_successful_login(self):
        """Test that a successful login resets failed attempts for that user."""
        login_url = '/api/v1/auth/login/'

        # Send 3 failed attempts
        for _ in range(3):
            response = self.client.post(login_url, {
                'username': self.username,
                'password': 'wrongpassword'
            })
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Send 1 successful login
        response = self.client.post(login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Send another 3 failed attempts (total would be 6 without reset, causing lockout)
        for _ in range(3):
            response = self.client.post(login_url, {
                'username': self.username,
                'password': 'wrongpassword'
            })
            # Should still be 400 (not locked out) because successful login reset the failures counter
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manual_lockout_reset(self):
        """Test that programmatically resetting the lockout resolves the lockout state."""
        login_url = '/api/v1/auth/login/'

        # Trigger lockout
        for _ in range(5):
            self.client.post(login_url, {
                'username': self.username,
                'password': 'wrongpassword'
            })

        # Verify lockout is active
        response = self.client.post(login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Reset lockout
        reset(username=self.username)

        # Verify lockout is cleared (returns 400 login error instead of 403 lockout)
        response = self.client.post(login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

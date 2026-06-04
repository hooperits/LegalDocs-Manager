"""
Tests for API throttling (rate limiting).
"""

from unittest.mock import patch
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import override_settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.throttling import CustomAnonRateThrottle, CustomUserRateThrottle, SearchRateThrottle


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'throttling-tests-cache',
        }
    }
)
class ThrottlingTests(APITestCase):
    """Test suite for API throttling configuration and translations."""

    def setUp(self):
        """Set up test users, clear cache, and dynamically override rates on throttle classes."""
        cache.clear()
        
        # Save original rates
        self.orig_anon_rate = getattr(CustomAnonRateThrottle, 'rate', None)
        self.orig_user_rate = getattr(CustomUserRateThrottle, 'rate', None)
        self.orig_search_rate = getattr(SearchRateThrottle, 'rate', None)

        # Set test rates
        CustomAnonRateThrottle.rate = '2/min'
        CustomUserRateThrottle.rate = '3/min'
        SearchRateThrottle.rate = '2/min'

        # Force re-parsing of rates
        for throttle_cls in (CustomAnonRateThrottle, CustomUserRateThrottle, SearchRateThrottle):
            throttle_cls.num_requests = None
            throttle_cls.duration = None

        self.user = User.objects.create_user(
            username='throttleuser',
            email='throttle@example.com',
            password='password123'
        )
        self.token = Token.objects.create(user=self.user)
        
        self.another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='password123'
        )
        self.another_token = Token.objects.create(user=self.another_user)

    def tearDown(self):
        """Restore original rates on throttle classes."""
        CustomAnonRateThrottle.rate = self.orig_anon_rate
        CustomUserRateThrottle.rate = self.orig_user_rate
        SearchRateThrottle.rate = self.orig_search_rate
        
        for throttle_cls in (CustomAnonRateThrottle, CustomUserRateThrottle, SearchRateThrottle):
            throttle_cls.num_requests = None
            throttle_cls.duration = None
            
        cache.clear()

    def test_global_user_throttling(self):
        """Test that authenticated users are throttled after exceeding the 'user' rate limit."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Rate is 3/min. First 3 requests should succeed (200 OK)
        for _ in range(3):
            response = self.client.get('/api/v1/profile/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 4th request should be throttled (429 Too Many Requests)
        response = self.client.get('/api/v1/profile/')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertTrue('detalle' in response.data or 'detail' in response.data)
        
        # Verify the other user is not affected (throttling is per-user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.another_token.key}')
        response = self.client.get('/api/v1/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_global_anon_throttling(self):
        """Test that anonymous requests are throttled after exceeding the 'anon' rate limit."""
        from rest_framework.test import APIRequestFactory
        from rest_framework.views import APIView
        from rest_framework.permissions import AllowAny
        from rest_framework.response import Response

        class PublicView(APIView):
            permission_classes = [AllowAny]
            throttle_classes = [CustomAnonRateThrottle]
            
            def get(self, request):
                return Response({'detail': 'success'})

        factory = APIRequestFactory()
        view = PublicView.as_view()

        # Rate is 2/min. First 2 requests should succeed
        for _ in range(2):
            request = factory.get('/test-anon/')
            response = view(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 3rd request should be throttled (429 Too Many Requests)
        request = factory.get('/test-anon/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertTrue('detalle' in response.data or 'detail' in response.data)

    def test_search_endpoint_throttling(self):
        """Test that the search endpoint has a stricter rate limit of 2/min in test configuration."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # First 2 searches should succeed
        for _ in range(2):
            response = self.client.get('/api/v1/search/?q=demo')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 3rd search should be throttled
        response = self.client.get('/api/v1/search/?q=demo')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertTrue('detalle' in response.data or 'detail' in response.data)

    def test_disable_throttling_bypass(self):
        """Test that enabling DISABLE_THROTTLING bypasses rate limits."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        with patch('api.throttling.DISABLE_THROTTLING', True):
            # Send 5 requests (exceeding the 3/min limit). All should succeed.
            for _ in range(5):
                response = self.client.get('/api/v1/profile/')
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_throttling_spanish_translation(self):
        """Test that throttling error messages are translated to Spanish when requested."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Trigger throttling
        for _ in range(3):
            self.client.get('/api/v1/profile/')

        # 4th request with Spanish header
        response = self.client.get('/api/v1/profile/', HTTP_ACCEPT_LANGUAGE='es')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('detalle', response.data)
        self.assertRegex(response.data['detalle'], r'^Límite de solicitudes excedido\. Espere \d+ segund(o|os)\.$')

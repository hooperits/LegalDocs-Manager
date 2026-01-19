"""
Rate limiting configuration for API endpoints.

Provides DRF-compatible throttle classes that wrap django-ratelimit
for consistent rate limiting across the application.

Set DISABLE_THROTTLING=1 environment variable to disable rate limiting for testing.
"""

import os

from rest_framework.throttling import SimpleRateThrottle

# Check if throttling should be disabled (for testing)
DISABLE_THROTTLING = os.getenv('DISABLE_THROTTLING', '').lower() in ('1', 'true', 'yes')


class AuthRateThrottle(SimpleRateThrottle):
    """
    Throttle class for authentication endpoints.

    Limits login/register requests to prevent brute force attacks.
    Rate: 5 requests per minute per IP address (disabled if DISABLE_THROTTLING=1).
    """

    scope = 'auth'

    def get_rate(self):
        """Return rate limit, or very high value if throttling is disabled."""
        if DISABLE_THROTTLING:
            return '10000/min'
        return '5/min'

    def get_cache_key(self, request, view):
        """
        Generate cache key based on client IP address.

        Returns:
            str: Cache key for rate limiting, or None to skip throttling.
        """
        if DISABLE_THROTTLING:
            return None

        if request.user and request.user.is_authenticated:
            # Don't throttle authenticated users
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


class LoginRateThrottle(AuthRateThrottle):
    """
    Specific throttle for login endpoint.

    Inherits from AuthRateThrottle.
    """

    scope = 'login'


class RegisterRateThrottle(AuthRateThrottle):
    """
    Specific throttle for registration endpoint.

    Inherits from AuthRateThrottle.
    """

    scope = 'register'

"""
Rate limiting configuration for API endpoints.

Provides DRF-compatible throttle classes that wrap django-ratelimit
for consistent rate limiting across the application.
"""

from rest_framework.throttling import SimpleRateThrottle


class AuthRateThrottle(SimpleRateThrottle):
    """
    Throttle class for authentication endpoints.

    Limits login/register requests to prevent brute force attacks.
    Rate: 5 requests per minute per IP address.
    """

    scope = 'auth'
    rate = '5/min'

    def get_cache_key(self, request, view):
        """
        Generate cache key based on client IP address.

        Returns:
            str: Cache key for rate limiting, or None to skip throttling.
        """
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

    Inherits from AuthRateThrottle with same 5/min rate.
    """

    scope = 'login'


class RegisterRateThrottle(AuthRateThrottle):
    """
    Specific throttle for registration endpoint.

    Inherits from AuthRateThrottle with same 5/min rate.
    """

    scope = 'register'

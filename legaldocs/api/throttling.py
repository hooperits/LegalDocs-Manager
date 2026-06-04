"""
Rate limiting configuration for API endpoints.

Provides DRF-compatible throttle classes that wrap django-ratelimit
for consistent rate limiting across the application.

Set DISABLE_THROTTLING=1 environment variable to disable rate limiting for testing.
"""

import os

from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle, UserRateThrottle

# Check if throttling should be disabled (for testing)
DISABLE_THROTTLING = os.getenv('DISABLE_THROTTLING', '').lower() in ('1', 'true', 'yes')


class CustomAnonRateThrottle(AnonRateThrottle):
    """
    Custom Anonymous rate throttle that respects the DISABLE_THROTTLING setting.
    """

    def get_cache_key(self, request, view):
        if DISABLE_THROTTLING:
            return None
        return super().get_cache_key(request, view)


class CustomUserRateThrottle(UserRateThrottle):
    """
    Custom Authenticated User rate throttle that respects the DISABLE_THROTTLING setting.
    """

    def get_cache_key(self, request, view):
        if DISABLE_THROTTLING:
            return None
        return super().get_cache_key(request, view)


class SearchRateThrottle(UserRateThrottle):
    """
    Throttle class for the search endpoint.

    Limits search queries per authenticated user to prevent database abuse.
    Rate: 30 requests per minute per user (disabled if DISABLE_THROTTLING=1).
    """

    scope = 'search'

    def get_cache_key(self, request, view):
        if DISABLE_THROTTLING:
            return None
        return super().get_cache_key(request, view)



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


def axes_lockout_response(request, *args, **kwargs):
    """
    Custom lockout response for django-axes that returns JSON and is bilingual.
    """
    from django.http import JsonResponse
    from django.utils.translation import get_language

    lang = get_language()
    if lang and lang.startswith('es'):
        message = "Cuenta bloqueada temporalmente por exceso de intentos fallidos. Intente de nuevo en 15 minutos."
        data = {"detalle": message}
    else:
        message = "Account locked out due to too many failed login attempts. Please try again in 15 minutes."
        data = {"detail": message}
    return JsonResponse(data, status=403)


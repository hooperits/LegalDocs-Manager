"""
Cache utilities for the LegalDocs application.

Provides helper functions for caching dashboard statistics
and other frequently accessed data.
"""

from functools import wraps
from typing import Any, Callable, Optional

from django.core.cache import cache


# Default cache timeout: 5 minutes (300 seconds)
DASHBOARD_CACHE_TIMEOUT = 300

# Cache key prefix for dashboard stats
DASHBOARD_CACHE_KEY = 'dashboard_stats'


def get_dashboard_stats() -> Optional[dict]:
    """
    Retrieve cached dashboard statistics.

    Returns:
        dict: Cached dashboard stats, or None if not cached.
    """
    return cache.get(DASHBOARD_CACHE_KEY)


def set_dashboard_stats(stats: dict, timeout: int = DASHBOARD_CACHE_TIMEOUT) -> None:
    """
    Cache dashboard statistics.

    Args:
        stats: Dictionary of dashboard statistics to cache.
        timeout: Cache timeout in seconds (default: 5 minutes).
    """
    cache.set(DASHBOARD_CACHE_KEY, stats, timeout)


def invalidate_dashboard_stats() -> None:
    """
    Invalidate cached dashboard statistics.

    Call this when data changes that would affect dashboard stats.
    """
    cache.delete(DASHBOARD_CACHE_KEY)


def cached_view(cache_key: str, timeout: int = 300) -> Callable:
    """
    Decorator for caching view responses.

    Args:
        cache_key: The cache key to use for this view.
        timeout: Cache timeout in seconds (default: 5 minutes).

    Returns:
        Decorated function that caches its response.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response

            # Execute the function
            response = func(*args, **kwargs)

            # Cache the response data (not the Response object)
            cache.set(cache_key, response, timeout)

            return response
        return wrapper
    return decorator

"""
URL configuration for LegalDocs Manager API v1.

This module defines the URL patterns for the REST API, including:
- ViewSet registration via DRF router
- Authentication endpoints (login, logout, register, me)
- Dashboard, search, and profile endpoints
- API documentation endpoints (schema and Swagger UI)
"""

from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from cases.views import CaseViewSet
from clients.views import ClientViewSet
from documents.views import DocumentViewSet

from .views import (
    DashboardView,
    LoginView,
    LogoutView,
    MeView,
    ProfileView,
    RegisterView,
    SearchView,
)

# Create router for ViewSet registration
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'cases', CaseViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    # Router URLs (ViewSets)
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/me/', MeView.as_view(), name='auth_me'),

    # Dashboard endpoint
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Search endpoint
    path('search/', SearchView.as_view(), name='search'),

    # Profile endpoint
    path('profile/', ProfileView.as_view(), name='profile'),

    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

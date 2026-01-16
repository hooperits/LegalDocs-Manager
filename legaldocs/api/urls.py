"""
URL configuration for LegalDocs Manager API v1.

This module defines the URL patterns for the REST API, including:
- ViewSet registration via DRF router
- Token authentication endpoint
- API documentation endpoints (schema and Swagger UI)
"""

from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from cases.views import CaseViewSet
from clients.views import ClientViewSet
from documents.views import DocumentViewSet

# Create router for ViewSet registration
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'cases', CaseViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    # Router URLs (ViewSets)
    path('', include(router.urls)),

    # Token authentication endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Technical Research: Django REST Framework API

**Feature**: 004-rest-api | **Date**: 2026-01-16

## Research Summary

This document captures technical decisions for implementing a complete REST API using Django REST Framework, including authentication, serialization patterns, filtering, and API documentation.

## Key Decisions

### 1. Authentication Strategy

**Decision**: Use both TokenAuthentication and SessionAuthentication.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

**Rationale**:
- TokenAuthentication for API clients (mobile apps, external services)
- SessionAuthentication for browser-based access (DRF browsable API, testing)
- Both are required by the constitution for DRF projects

**Alternatives Considered**:
- JWT Authentication (djangorestframework-simplejwt): Rejected - overkill for POC, token rotation adds complexity
- OAuth2: Rejected - too complex for internal POC

### 2. Serializer Pattern (List vs Detail)

**Decision**: Use separate serializers for list and detail views.

```python
class ClientSerializer(serializers.ModelSerializer):
    # For list view - minimal fields, fast
    class Meta:
        fields = ['id', 'full_name', 'email', ...]  # excludes 'notes'

class ClientDetailSerializer(serializers.ModelSerializer):
    # For detail view - all fields, nested data
    case_count = serializers.SerializerMethodField()
    class Meta:
        fields = [..., 'notes', 'case_count']
```

**Rationale**:
- List views need to be fast with minimal data
- Detail views can include computed fields and nested data
- Follows DRF best practices for performance

**Alternative Considered**:
- Single serializer with `fields` parameter: Rejected - harder to maintain, mixes concerns

### 3. ViewSet vs APIView

**Decision**: Use ModelViewSet for all resources.

```python
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    # Automatic CRUD: list, create, retrieve, update, partial_update, destroy
```

**Rationale**:
- Provides all CRUD operations with minimal code
- Easy to add custom actions with @action decorator
- Works seamlessly with DRF routers
- Follows constitution's preference for class-based views

**Alternative Considered**:
- Generic views (ListCreateAPIView, etc.): Rejected - more boilerplate for same functionality
- Function-based views: Rejected - against constitution

### 4. Filtering Implementation

**Decision**: Use django-filter with DjangoFilterBackend.

```python
from django_filters.rest_framework import DjangoFilterBackend

class CaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'case_type', 'priority', 'client']
    search_fields = ['case_number', 'title', 'client__full_name']
    ordering_fields = ['start_date', 'priority']
```

**Rationale**:
- Standard DRF pattern for filtering
- Supports exact match, search, and ordering in one setup
- Query params are intuitive: `?status=en_proceso&search=García`

**Alternative Considered**:
- Custom filter logic in get_queryset(): Rejected - reinvents the wheel, error-prone

### 5. API Documentation Tool

**Decision**: Use drf-spectacular for OpenAPI 3.0 schema generation.

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

**Rationale**:
- OpenAPI 3.0 is the current standard
- Auto-generates schema from serializers and viewsets
- Swagger UI included for interactive testing
- Better maintained than drf-yasg

**Alternative Considered**:
- drf-yasg: Rejected - uses older OpenAPI 2.0 (Swagger), less actively maintained
- CoreAPI schema: Rejected - deprecated in DRF 3.14+

### 6. CORS Configuration

**Decision**: Use django-cors-headers with explicit allowed origins.

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
```

**Rationale**:
- Required for frontend development on different port
- Explicit origins are more secure than CORS_ALLOW_ALL_ORIGINS
- CORS_ALLOW_CREDENTIALS needed for session auth in browser

**Alternative Considered**:
- CORS_ALLOW_ALL_ORIGINS=True: Rejected - security risk, only acceptable in development

### 7. Pagination Strategy

**Decision**: Use PageNumberPagination with 20 items per page.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

**Rationale**:
- Simple, intuitive pagination with `?page=2`
- 20 items balances performance and UX
- Matches specification requirement

**Alternative Considered**:
- LimitOffsetPagination: Rejected - less intuitive for frontend developers
- CursorPagination: Rejected - overkill for POC, useful for infinite scroll

### 8. Custom Permission Structure

**Decision**: Create IsOwnerOrReadOnly permission for documents.

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return obj.uploaded_by == request.user or request.user.is_staff
        return True
```

**Rationale**:
- Allows reading by anyone authenticated
- Restricts deletion to document owner or admin
- Simple, single-responsibility permission class

**Alternative Considered**:
- Check permissions in view methods: Rejected - scattered logic, hard to test

### 9. File Upload Handling

**Decision**: Use MultiPartParser and FormParser for document uploads.

```python
class DocumentViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
```

**Rationale**:
- Standard way to handle file uploads in DRF
- Supports both multipart form data and regular forms
- Works with Django's file handling infrastructure

**File Size Limit**: Configure in Django settings:
```python
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
```

### 10. API Versioning

**Decision**: Use URL path versioning with /api/v1/ prefix.

```python
# urls.py
urlpatterns = [
    path('api/v1/', include('api.urls')),
]
```

**Rationale**:
- Simple and explicit
- Easy to add v2 later without breaking v1
- Clear in API documentation

**Alternative Considered**:
- Header versioning (Accept-Version): Rejected - less discoverable
- Query parameter versioning: Rejected - not RESTful

## Dependencies to Install

```bash
pip install djangorestframework
pip install django-filter
pip install drf-spectacular
pip install django-cors-headers
```

Add to requirements.txt:
```
djangorestframework>=3.15.0
django-filter>=24.0
drf-spectacular>=0.27.0
django-cors-headers>=4.3.0
```

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `legaldocs/settings.py` | MODIFY | Add REST_FRAMEWORK, CORS settings |
| `legaldocs/urls.py` | MODIFY | Add api/v1/ include |
| `api/__init__.py` | CREATE | Package marker |
| `api/urls.py` | CREATE | Router registration |
| `api/permissions.py` | CREATE | Custom permissions |
| `clients/serializers.py` | CREATE | Client serializers |
| `clients/views.py` | CREATE | ClientViewSet |
| `cases/serializers.py` | CREATE | Case serializers |
| `cases/views.py` | CREATE | CaseViewSet |
| `documents/serializers.py` | CREATE | Document serializer |
| `documents/views.py` | CREATE | DocumentViewSet |

## References

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [django-filter Documentation](https://django-filter.readthedocs.io/)
- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [django-cors-headers Documentation](https://github.com/adamchainz/django-cors-headers)

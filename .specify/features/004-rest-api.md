# Feature Specification: Django REST Framework API

**Feature Branch**: `004-rest-api`
**Created**: 2026-01-16
**Status**: Draft
**Input**: Build RESTful API with Django REST Framework for clients, cases, and documents management

## User Scenarios & Testing *(mandatory)*

### User Story 1 - API Setup and Authentication (Priority: P1)

As a developer, I want the API properly configured with authentication so that only authorized users can access the endpoints.

**Why this priority**: Authentication is foundational - all other endpoints depend on it.

**Independent Test**: Can be verified by attempting to access /api/v1/clients/ without and with authentication token.

**Acceptance Scenarios**:

1. **Given** I have no token, **When** I access any API endpoint, **Then** I receive 401 Unauthorized
2. **Given** I have valid credentials, **When** I POST to /api/v1/api-token-auth/, **Then** I receive an authentication token
3. **Given** I have a valid token, **When** I access /api/v1/clients/ with Authorization header, **Then** I receive 200 OK with data
4. **Given** I request a list endpoint, **When** results exceed 20 items, **Then** response is paginated with next/previous links
5. **Given** CORS is configured, **When** I make a request from localhost:3000, **Then** the request is allowed

---

### User Story 2 - Client API (Priority: P1)

As a frontend developer, I want a complete Client API so that I can build client management features.

**Why this priority**: Clients are the entry point for the legal workflow.

**Independent Test**: Can be verified by testing all CRUD operations on /api/v1/clients/.

**Acceptance Scenarios**:

1. **Given** I GET /api/v1/clients/, **When** I view the response, **Then** I see a paginated list of clients without notes field
2. **Given** I GET /api/v1/clients/1/, **When** I view the response, **Then** I see full client details including notes and case_count
3. **Given** I POST to /api/v1/clients/, **When** I provide valid data, **Then** a new client is created and returned
4. **Given** I GET /api/v1/clients/?is_active=true, **When** I view results, **Then** only active clients are shown
5. **Given** I GET /api/v1/clients/?search=García, **When** I view results, **Then** clients matching name or email are shown
6. **Given** I GET /api/v1/clients/1/cases/, **When** the client has cases, **Then** I see a list of that client's cases

---

### User Story 3 - Case API (Priority: P1)

As a frontend developer, I want a complete Case API so that I can build case management features with filtering and statistics.

**Why this priority**: Cases are the central business entity requiring comprehensive API support.

**Independent Test**: Can be verified by testing all CRUD operations and custom actions on /api/v1/cases/.

**Acceptance Scenarios**:

1. **Given** I GET /api/v1/cases/, **When** I view the response, **Then** I see cases with client name included
2. **Given** I GET /api/v1/cases/1/, **When** I view the response, **Then** I see nested client data and documents list
3. **Given** I GET /api/v1/cases/?status=en_proceso, **When** I filter, **Then** only cases with that status are shown
4. **Given** I GET /api/v1/cases/?client=1, **When** I filter by client, **Then** only that client's cases are shown
5. **Given** I POST /api/v1/cases/1/close/, **When** I close a case, **Then** status becomes 'cerrado' and closed_date is set
6. **Given** I GET /api/v1/cases/statistics/, **When** I request stats, **Then** I see counts by status, type, and priority
7. **Given** I GET /api/v1/cases/?ordering=-start_date, **When** I order results, **Then** cases are sorted by start_date descending

---

### User Story 4 - Document API (Priority: P1)

As a frontend developer, I want a Document API with file upload support so that I can manage legal documents.

**Why this priority**: Documents require special handling for file uploads and access control.

**Independent Test**: Can be verified by uploading a file and testing permission restrictions.

**Acceptance Scenarios**:

1. **Given** I GET /api/v1/documents/, **When** I view the response, **Then** I see documents with case info and uploader username
2. **Given** I POST to /api/v1/documents/ with multipart/form-data, **When** I upload a file, **Then** the document is created with uploaded_by auto-set
3. **Given** I GET /api/v1/documents/?case=1, **When** I filter by case, **Then** only that case's documents are shown
4. **Given** I uploaded a document, **When** I DELETE /api/v1/documents/1/, **Then** the document is deleted
5. **Given** another user uploaded a document, **When** I try to DELETE it, **Then** I receive 403 Forbidden (unless admin)
6. **Given** I GET /api/v1/documents/?is_confidential=true, **When** I filter, **Then** only confidential documents are shown

---

### User Story 5 - API Documentation (Priority: P2)

As a developer, I want API documentation so that I can understand available endpoints and their usage.

**Why this priority**: Documentation improves developer experience but is not required for functionality.

**Independent Test**: Can be verified by accessing /api/v1/schema/ and /api/v1/docs/.

**Acceptance Scenarios**:

1. **Given** I access /api/v1/schema/, **When** I download the schema, **Then** I receive OpenAPI 3.0 specification
2. **Given** I access /api/v1/docs/, **When** I view the page, **Then** I see interactive API documentation

---

### Edge Cases

- What happens when creating a case with non-existent client ID? → 400 Bad Request with validation error
- What happens when uploading a file larger than 10MB? → 413 Payload Too Large (configure in settings)
- What happens when filtering with invalid query params? → Ignore invalid params, return all results
- What happens when token expires? → 401 Unauthorized with "Token expired" message
- What happens when closing an already closed case? → 400 Bad Request with "Case already closed" message

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: API MUST require authentication for all endpoints
- **FR-002**: API MUST support both Token and Session authentication
- **FR-003**: API MUST paginate list responses to 20 items per page
- **FR-004**: ClientViewSet MUST support full CRUD operations
- **FR-005**: ClientViewSet MUST support filtering by is_active
- **FR-006**: ClientViewSet MUST support search by name and email
- **FR-007**: ClientViewSet MUST have custom action to get client's cases
- **FR-008**: CaseViewSet MUST support filtering by status, case_type, priority, client
- **FR-009**: CaseViewSet MUST support ordering by start_date and priority
- **FR-010**: CaseViewSet MUST have custom action to close case
- **FR-011**: CaseViewSet MUST have custom action for statistics
- **FR-012**: DocumentViewSet MUST auto-set uploaded_by on create
- **FR-013**: DocumentViewSet MUST restrict delete to uploader or admin
- **FR-014**: API MUST use /api/v1/ namespace
- **FR-015**: API MUST provide OpenAPI schema

### Non-Functional Requirements

- **NFR-001**: API responses MUST return within 500ms for list operations
- **NFR-002**: File uploads MUST be limited to 10MB
- **NFR-003**: CORS MUST be configured for development origins

### Key Entities

- **ClientSerializer/ClientDetailSerializer**: Client data serialization
- **CaseSerializer/CaseDetailSerializer**: Case data with nested relations
- **DocumentSerializer**: Document data with file handling
- **ClientViewSet**: Client CRUD with filters and custom actions
- **CaseViewSet**: Case CRUD with filters, ordering, and statistics
- **DocumentViewSet**: Document CRUD with permissions

## Technical Specification

### DRF Settings (legaldocs/settings.py)

```python
# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# CORS configuration for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
```

### Client Serializers (clients/serializers.py)

```python
from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client list view."""

    class Meta:
        model = Client
        fields = [
            'id',
            'full_name',
            'identification_number',
            'email',
            'phone',
            'address',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class ClientDetailSerializer(serializers.ModelSerializer):
    """Serializer for Client detail view with additional fields."""
    case_count = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id',
            'full_name',
            'identification_number',
            'email',
            'phone',
            'address',
            'is_active',
            'notes',
            'case_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_case_count(self, obj):
        return obj.cases.count()
```

### Case Serializers (cases/serializers.py)

```python
from rest_framework import serializers
from .models import Case
from clients.serializers import ClientSerializer
from documents.serializers import DocumentSerializer


class CaseSerializer(serializers.ModelSerializer):
    """Serializer for Case list view."""
    client_name = serializers.CharField(source='client.full_name', read_only=True)

    class Meta:
        model = Case
        fields = [
            'id',
            'case_number',
            'client',
            'client_name',
            'title',
            'description',
            'case_type',
            'status',
            'priority',
            'start_date',
            'deadline',
            'closed_date',
            'assigned_to',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['case_number', 'created_at', 'updated_at']


class CaseDetailSerializer(serializers.ModelSerializer):
    """Serializer for Case detail view with nested data."""
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source='client',
        write_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = [
            'id',
            'case_number',
            'client',
            'client_id',
            'title',
            'description',
            'case_type',
            'status',
            'priority',
            'start_date',
            'deadline',
            'closed_date',
            'assigned_to',
            'documents',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['case_number', 'created_at', 'updated_at']
```

### Document Serializers (documents/serializers.py)

```python
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    uploaded_by_username = serializers.CharField(
        source='uploaded_by.username',
        read_only=True
    )
    case_number = serializers.CharField(source='case.case_number', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'case',
            'case_number',
            'title',
            'document_type',
            'description',
            'file',
            'file_size',
            'is_confidential',
            'uploaded_by',
            'uploaded_by_username',
            'uploaded_at',
        ]
        read_only_fields = ['file_size', 'uploaded_by', 'uploaded_at']
```

### Custom Permissions (api/permissions.py)

```python
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a document to delete it.
    Admins can delete any document.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for owner or admin
        if request.method == 'DELETE':
            return obj.uploaded_by == request.user or request.user.is_staff

        return True


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to perform delete operations.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return request.user.is_staff

        return True
```

### Client ViewSet (clients/views.py)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Client
from .serializers import ClientSerializer, ClientDetailSerializer
from cases.serializers import CaseSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for Client CRUD operations."""
    queryset = Client.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['full_name', 'email', 'identification_number']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    @action(detail=True, methods=['get'])
    def cases(self, request, pk=None):
        """Get all cases for a specific client."""
        client = self.get_object()
        cases = client.cases.all()
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data)
```

### Case ViewSet (cases/views.py)

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db.models import Count

from .models import Case
from .serializers import CaseSerializer, CaseDetailSerializer


class CaseViewSet(viewsets.ModelViewSet):
    """ViewSet for Case CRUD operations."""
    queryset = Case.objects.select_related('client', 'assigned_to')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'case_type', 'priority', 'client']
    search_fields = ['case_number', 'title', 'client__full_name']
    ordering_fields = ['start_date', 'priority', 'created_at']
    ordering = ['-start_date']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CaseDetailSerializer
        return CaseSerializer

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close a case by setting status to 'cerrado' and closed_date."""
        case = self.get_object()
        if case.status == 'cerrado':
            return Response(
                {'error': 'Case already closed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        case.status = 'cerrado'
        case.closed_date = timezone.now().date()
        case.save()
        serializer = self.get_serializer(case)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get case statistics by status, type, and priority."""
        status_counts = Case.objects.values('status').annotate(count=Count('id'))
        type_counts = Case.objects.values('case_type').annotate(count=Count('id'))
        priority_counts = Case.objects.values('priority').annotate(count=Count('id'))

        return Response({
            'by_status': {item['status']: item['count'] for item in status_counts},
            'by_type': {item['case_type']: item['count'] for item in type_counts},
            'by_priority': {item['priority']: item['count'] for item in priority_counts},
            'total': Case.objects.count(),
        })
```

### Document ViewSet (documents/views.py)

```python
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Document
from .serializers import DocumentSerializer
from api.permissions import IsOwnerOrReadOnly


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Document CRUD operations with file upload support."""
    queryset = Document.objects.select_related('case', 'uploaded_by')
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['case', 'document_type', 'is_confidential']
    search_fields = ['title', 'case__case_number']
    ordering_fields = ['uploaded_at', 'title']
    ordering = ['-uploaded_at']

    def perform_create(self, serializer):
        """Auto-set uploaded_by to current user on create."""
        serializer.save(uploaded_by=self.request.user)
```

### URL Configuration (api/urls.py)

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from clients.views import ClientViewSet
from cases.views import CaseViewSet
from documents.views import DocumentViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'cases', CaseViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

### Main URL Configuration (legaldocs/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

from . import admin as admin_config  # noqa: F401

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Token authentication endpoint returns valid token for correct credentials
- **SC-002**: All endpoints return 401 for unauthenticated requests
- **SC-003**: List endpoints return paginated results with 20 items per page
- **SC-004**: ClientViewSet supports GET, POST, PUT, PATCH, DELETE operations
- **SC-005**: ClientViewSet filters by is_active and searches by name/email
- **SC-006**: ClientViewSet /clients/{id}/cases/ returns client's cases
- **SC-007**: CaseViewSet filters by status, case_type, priority, client
- **SC-008**: CaseViewSet /cases/{id}/close/ updates status and closed_date
- **SC-009**: CaseViewSet /cases/statistics/ returns counts by status/type/priority
- **SC-010**: DocumentViewSet accepts multipart/form-data for file uploads
- **SC-011**: DocumentViewSet auto-sets uploaded_by on create
- **SC-012**: DocumentViewSet restricts delete to owner or admin
- **SC-013**: OpenAPI schema available at /api/v1/schema/
- **SC-014**: Swagger UI available at /api/v1/docs/

## Verification Checklist

- [ ] DRF installed and configured in settings.py
- [ ] Token and Session authentication configured
- [ ] Pagination set to 20 items
- [ ] CORS configured for localhost:3000
- [ ] ClientSerializer excludes notes field
- [ ] ClientDetailSerializer includes notes and case_count
- [ ] CaseSerializer includes client_name
- [ ] CaseDetailSerializer has nested client and documents
- [ ] DocumentSerializer includes uploaded_by_username
- [ ] ClientViewSet with filter, search, and cases action
- [ ] CaseViewSet with filters, ordering, close and statistics actions
- [ ] DocumentViewSet with file upload and IsOwnerOrReadOnly permission
- [ ] API router registered at /api/v1/
- [ ] Token auth endpoint at /api/v1/api-token-auth/
- [ ] OpenAPI schema generation working
- [ ] All CRUD operations tested for each endpoint

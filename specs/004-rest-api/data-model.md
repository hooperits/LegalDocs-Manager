# API Data Model: Django REST Framework API

**Feature**: 004-rest-api | **Date**: 2026-01-16

## API Structure Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LegalDocs Manager API v1                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              Authentication                                   │
│  POST /api/v1/api-token-auth/  →  {"token": "abc123..."}                    │
│  Header: Authorization: Token abc123...                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   /api/v1/clients/  │  │   /api/v1/cases/    │  │  /api/v1/documents/ │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ GET    - List       │  │ GET    - List       │  │ GET    - List       │
│ POST   - Create     │  │ POST   - Create     │  │ POST   - Create     │
│ GET    - Retrieve   │  │ GET    - Retrieve   │  │ GET    - Retrieve   │
│ PUT    - Update     │  │ PUT    - Update     │  │ PUT    - Update     │
│ PATCH  - Partial    │  │ PATCH  - Partial    │  │ PATCH  - Partial    │
│ DELETE - Destroy    │  │ DELETE - Destroy    │  │ DELETE - Destroy    │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ Custom Actions:     │  │ Custom Actions:     │  │ Permissions:        │
│ GET /{id}/cases/    │  │ POST /{id}/close/   │  │ IsOwnerOrReadOnly   │
│                     │  │ GET /statistics/    │  │ (delete restricted) │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

## Serializer Specifications

### ClientSerializer (List View)

| Field | Type | Read-Only | Notes |
|-------|------|-----------|-------|
| id | integer | Yes | Primary key |
| full_name | string | No | Required, max 200 chars |
| identification_number | string | No | Required, unique, max 20 chars |
| email | email | No | Required, unique |
| phone | string | No | Optional, max 20 chars |
| address | text | No | Optional |
| is_active | boolean | No | Default: true |
| created_at | datetime | Yes | Auto-set on create |
| updated_at | datetime | Yes | Auto-set on update |

**Excludes**: `notes` (included only in detail view)

### ClientDetailSerializer (Detail View)

Extends ClientSerializer with:

| Field | Type | Read-Only | Notes |
|-------|------|-----------|-------|
| notes | text | No | Internal notes |
| case_count | integer | Yes | Computed: `obj.cases.count()` |

### CaseSerializer (List View)

| Field | Type | Read-Only | Notes |
|-------|------|-----------|-------|
| id | integer | Yes | Primary key |
| case_number | string | Yes | Auto-generated (CASO-YYYYMMDD-XXX) |
| client | integer | No | ForeignKey to Client |
| client_name | string | Yes | From `client.full_name` |
| title | string | No | Required, max 200 chars |
| description | text | No | Optional |
| case_type | string | No | Choices: civil, penal, laboral, familia, administrativo |
| status | string | No | Choices: en_proceso, pendiente_documentos, en_revision, cerrado |
| priority | string | No | Choices: alta, media, baja |
| start_date | date | No | Required |
| deadline | date | No | Optional |
| closed_date | date | No | Set when status='cerrado' |
| assigned_to | integer | No | ForeignKey to User (nullable) |
| created_at | datetime | Yes | Auto-set |
| updated_at | datetime | Yes | Auto-set |

### CaseDetailSerializer (Detail View)

Extends CaseSerializer with nested data:

| Field | Type | Read-Only | Notes |
|-------|------|-----------|-------|
| client | object | Yes | Nested ClientSerializer |
| client_id | integer | Write-only | For creating/updating |
| documents | array | Yes | Nested DocumentSerializer list |

### DocumentSerializer

| Field | Type | Read-Only | Notes |
|-------|------|-----------|-------|
| id | integer | Yes | Primary key |
| case | integer | No | ForeignKey to Case |
| case_number | string | Yes | From `case.case_number` |
| title | string | No | Required, max 200 chars |
| document_type | string | No | Choices: contrato, demanda, sentencia, etc. |
| description | text | No | Optional |
| file | file | No | Required on create |
| file_size | integer | Yes | Auto-calculated in bytes |
| is_confidential | boolean | No | Default: false |
| uploaded_by | integer | Yes | Auto-set to request.user |
| uploaded_by_username | string | Yes | From `uploaded_by.username` |
| uploaded_at | datetime | Yes | Auto-set |

## ViewSet Configuration

### ClientViewSet

| Attribute | Value |
|-----------|-------|
| **queryset** | `Client.objects.all()` |
| **serializer_class** | ClientSerializer (list), ClientDetailSerializer (retrieve) |
| **filter_backends** | DjangoFilterBackend, SearchFilter, OrderingFilter |
| **filterset_fields** | `['is_active']` |
| **search_fields** | `['full_name', 'email', 'identification_number']` |
| **ordering_fields** | `['full_name', 'created_at']` |
| **ordering** | `['-created_at']` |

**Custom Actions**:

| Action | Method | URL | Description |
|--------|--------|-----|-------------|
| cases | GET | `/clients/{id}/cases/` | Get all cases for a client |

### CaseViewSet

| Attribute | Value |
|-----------|-------|
| **queryset** | `Case.objects.select_related('client', 'assigned_to')` |
| **serializer_class** | CaseSerializer (list), CaseDetailSerializer (retrieve) |
| **filter_backends** | DjangoFilterBackend, SearchFilter, OrderingFilter |
| **filterset_fields** | `['status', 'case_type', 'priority', 'client']` |
| **search_fields** | `['case_number', 'title', 'client__full_name']` |
| **ordering_fields** | `['start_date', 'priority', 'created_at']` |
| **ordering** | `['-start_date']` |

**Custom Actions**:

| Action | Method | URL | Description |
|--------|--------|-----|-------------|
| close | POST | `/cases/{id}/close/` | Set status='cerrado', closed_date=today |
| statistics | GET | `/cases/statistics/` | Return counts by status/type/priority |

**Statistics Response**:
```json
{
  "by_status": {"en_proceso": 5, "cerrado": 3, ...},
  "by_type": {"civil": 4, "penal": 2, ...},
  "by_priority": {"alta": 2, "media": 4, ...},
  "total": 10
}
```

### DocumentViewSet

| Attribute | Value |
|-----------|-------|
| **queryset** | `Document.objects.select_related('case', 'uploaded_by')` |
| **serializer_class** | DocumentSerializer |
| **parser_classes** | MultiPartParser, FormParser |
| **permission_classes** | IsAuthenticated, IsOwnerOrReadOnly |
| **filter_backends** | DjangoFilterBackend, SearchFilter, OrderingFilter |
| **filterset_fields** | `['case', 'document_type', 'is_confidential']` |
| **search_fields** | `['title', 'case__case_number']` |
| **ordering_fields** | `['uploaded_at', 'title']` |
| **ordering** | `['-uploaded_at']` |

**Special Behavior**:
- `uploaded_by` auto-set in `perform_create()`
- DELETE restricted to owner or admin via IsOwnerOrReadOnly

## Permission Classes

### IsOwnerOrReadOnly

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    - SAFE_METHODS (GET, HEAD, OPTIONS): Allow for any authenticated user
    - DELETE: Allow only for uploaded_by user or staff
    - Other methods: Allow for any authenticated user
    """
```

## API Endpoints Summary

| Endpoint | Methods | Auth | Notes |
|----------|---------|------|-------|
| `/api/v1/api-token-auth/` | POST | No | Get token with username/password |
| `/api/v1/clients/` | GET, POST | Yes | List/Create clients |
| `/api/v1/clients/{id}/` | GET, PUT, PATCH, DELETE | Yes | Client detail |
| `/api/v1/clients/{id}/cases/` | GET | Yes | Client's cases |
| `/api/v1/cases/` | GET, POST | Yes | List/Create cases |
| `/api/v1/cases/{id}/` | GET, PUT, PATCH, DELETE | Yes | Case detail |
| `/api/v1/cases/{id}/close/` | POST | Yes | Close case |
| `/api/v1/cases/statistics/` | GET | Yes | Case statistics |
| `/api/v1/documents/` | GET, POST | Yes | List/Create documents |
| `/api/v1/documents/{id}/` | GET, PUT, PATCH, DELETE | Yes | Document detail (delete restricted) |
| `/api/v1/schema/` | GET | No | OpenAPI schema |
| `/api/v1/docs/` | GET | No | Swagger UI |

## Pagination

All list endpoints use PageNumberPagination:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/clients/?page=2",
  "previous": null,
  "results": [...]
}
```

- **PAGE_SIZE**: 20 items per page
- **Query param**: `?page=2`

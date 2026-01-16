# Data Model Reference: Testing and Documentation

**Feature**: 006-testing-docs
**Date**: 2026-01-16

## Overview

This feature does not introduce new models. This document serves as a reference for the existing models that require test coverage.

---

## Existing Models to Test

### Client (clients.models.Client)

```python
class Client(models.Model):
    full_name: CharField(max_length=200)           # Required
    identification_number: CharField(max_length=50, unique=True)  # Required, unique
    email: EmailField                               # Required, email format
    phone: CharField(max_length=20)                 # Required
    address: TextField(blank=True)                  # Optional
    is_active: BooleanField(default=True)           # Default: True
    notes: TextField(blank=True)                    # Optional
    created_at: DateTimeField(auto_now_add=True)    # Auto-set
    updated_at: DateTimeField(auto_now=True)        # Auto-update
```

**Test Scenarios**:
- Create client with valid data
- Create client with duplicate identification_number (should fail)
- Create client with invalid email format (should fail)
- Create client with minimum required fields
- Verify __str__ returns "full_name (identification_number)"
- Verify default ordering is -created_at

### Case (cases.models.Case)

```python
class Case(models.Model):
    client: ForeignKey(Client, on_delete=PROTECT)   # Required, protected delete
    case_number: CharField(max_length=20, unique=True, editable=False)  # Auto-generated
    title: CharField(max_length=200)                # Required
    description: TextField                          # Required
    case_type: CharField(choices=CASE_TYPE_CHOICES) # Required: civil|penal|laboral|mercantil|familia
    status: CharField(choices=STATUS_CHOICES, default='en_proceso')  # Default: en_proceso
    priority: CharField(choices=PRIORITY_CHOICES, default='media')   # Default: media
    start_date: DateField                           # Required
    deadline: DateField(null=True, blank=True)      # Optional
    closed_date: DateField(null=True, blank=True)   # Optional
    assigned_to: ForeignKey(User, null=True, on_delete=SET_NULL)  # Optional
    created_at: DateTimeField(auto_now_add=True)    # Auto-set
    updated_at: DateTimeField(auto_now=True)        # Auto-update
```

**Choice Values**:
- CASE_TYPE: civil, penal, laboral, mercantil, familia
- STATUS: en_proceso, pendiente_documentos, en_revision, cerrado
- PRIORITY: baja, media, alta, urgente

**Test Scenarios**:
- Create case with valid data
- Verify case_number auto-generates in format CASE-YYYY-NNNN
- Verify case_number increments correctly
- Test CaseManager.active() excludes closed cases
- Test CaseManager.by_status() filters correctly
- Verify client deletion is blocked (PROTECT)
- Verify __str__ returns "case_number - title"

### Document (documents.models.Document)

```python
class Document(models.Model):
    case: ForeignKey(Case, on_delete=CASCADE)       # Required, cascade delete
    document_type: CharField(choices=DOCUMENT_TYPE_CHOICES)  # Required
    title: CharField(max_length=200)                # Required
    description: TextField(blank=True)              # Optional
    file: FileField(upload_to='legal_documents/')   # Required
    file_size: IntegerField(editable=False)         # Auto-calculated
    uploaded_by: ForeignKey(User, null=True, on_delete=SET_NULL)  # Optional
    uploaded_at: DateTimeField(auto_now_add=True)   # Auto-set
    is_confidential: BooleanField(default=False)    # Default: False
```

**Choice Values**:
- DOCUMENT_TYPE: contrato, demanda, poder, sentencia, escritura, otro

**Test Scenarios**:
- Create document with valid file
- Verify file_size auto-calculates from file
- Verify documents deleted when case deleted (CASCADE)
- Verify __str__ returns "document_type_display: title"
- Test file upload with different file types

---

## Serializers to Test

### ClientSerializer / ClientDetailSerializer

| Field | List | Detail | Writable | Notes |
|-------|------|--------|----------|-------|
| id | ✓ | ✓ | No | Auto PK |
| full_name | ✓ | ✓ | Yes | |
| identification_number | ✓ | ✓ | Yes | Unique constraint |
| email | ✓ | ✓ | Yes | Email validation |
| phone | ✓ | ✓ | Yes | |
| address | ✓ | ✓ | Yes | |
| is_active | ✓ | ✓ | Yes | |
| notes | No | ✓ | Yes | Detail only |
| case_count | No | ✓ | No | Computed field |
| created_at | ✓ | ✓ | No | Read-only |
| updated_at | ✓ | ✓ | No | Read-only |

### CaseSerializer / CaseDetailSerializer

| Field | List | Detail | Writable | Notes |
|-------|------|--------|----------|-------|
| id | ✓ | ✓ | No | Auto PK |
| case_number | ✓ | ✓ | No | Auto-generated |
| client | ✓ | ✓ (nested) | No | Read in detail |
| client_id | No | ✓ | Yes | Write-only |
| client_name | ✓ | No | No | Computed |
| title | ✓ | ✓ | Yes | |
| description | ✓ | ✓ | Yes | |
| case_type | ✓ | ✓ | Yes | Choices |
| status | ✓ | ✓ | Yes | Choices |
| priority | ✓ | ✓ | Yes | Choices |
| start_date | ✓ | ✓ | Yes | |
| deadline | ✓ | ✓ | Yes | Optional |
| closed_date | ✓ | ✓ | Yes | Optional |
| assigned_to | ✓ | ✓ | Yes | FK to User |
| documents | No | ✓ | No | Nested list |
| created_at | ✓ | ✓ | No | Read-only |
| updated_at | ✓ | ✓ | No | Read-only |

### DocumentSerializer

| Field | Writable | Notes |
|-------|----------|-------|
| id | No | Auto PK |
| case | Yes | FK to Case |
| case_number | No | Computed from case |
| title | Yes | |
| document_type | Yes | Choices |
| description | Yes | Optional |
| file | Yes | FileField |
| file_size | No | Auto-calculated |
| is_confidential | Yes | |
| uploaded_by | No | Auto-set from request.user |
| uploaded_by_username | No | Computed |
| uploaded_at | No | Auto-set |

---

## ViewSets to Test

### ClientViewSet

| Action | Method | URL | Notes |
|--------|--------|-----|-------|
| list | GET | /api/v1/clients/ | Paginated, filterable |
| create | POST | /api/v1/clients/ | |
| retrieve | GET | /api/v1/clients/{id}/ | Uses DetailSerializer |
| update | PUT | /api/v1/clients/{id}/ | |
| partial_update | PATCH | /api/v1/clients/{id}/ | |
| destroy | DELETE | /api/v1/clients/{id}/ | |
| cases | GET | /api/v1/clients/{id}/cases/ | Custom action |

**Filters**: is_active
**Search**: full_name, email, identification_number
**Ordering**: full_name, created_at

### CaseViewSet

| Action | Method | URL | Notes |
|--------|--------|-----|-------|
| list | GET | /api/v1/cases/ | Paginated, filterable |
| create | POST | /api/v1/cases/ | |
| retrieve | GET | /api/v1/cases/{id}/ | Uses DetailSerializer |
| update | PUT | /api/v1/cases/{id}/ | |
| partial_update | PATCH | /api/v1/cases/{id}/ | |
| destroy | DELETE | /api/v1/cases/{id}/ | |
| close | POST | /api/v1/cases/{id}/close/ | Custom action |
| statistics | GET | /api/v1/cases/statistics/ | Custom action |

**Filters**: status, case_type, priority, client
**Search**: case_number, title, client__full_name
**Ordering**: start_date, priority, created_at

### DocumentViewSet

| Action | Method | URL | Notes |
|--------|--------|-----|-------|
| list | GET | /api/v1/documents/ | Paginated, filterable |
| create | POST | /api/v1/documents/ | Multipart form |
| retrieve | GET | /api/v1/documents/{id}/ | |
| update | PUT | /api/v1/documents/{id}/ | |
| partial_update | PATCH | /api/v1/documents/{id}/ | |
| destroy | DELETE | /api/v1/documents/{id}/ | Owner/staff only |

**Filters**: case, document_type, is_confidential
**Search**: title, description
**Ordering**: uploaded_at, title
**Permissions**: IsOwnerOrReadOnly

---

## Relationships

```
Client (1) ─────< Case (many)
                    │
                    └────< Document (many)
                    │
User (1) ──────────┤ (assigned_to)
                    │
User (1) ──────────┘ (uploaded_by on Document)
```

**Deletion Behavior**:
- Client deleted → Cases PROTECTED (blocked)
- Case deleted → Documents CASCADE (deleted)
- User deleted → assigned_to SET_NULL, uploaded_by SET_NULL

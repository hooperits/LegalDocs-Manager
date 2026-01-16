# Feature Specification: Authentication and Dashboard Views

**Feature Branch**: `005-auth-dashboard`
**Created**: 2026-01-16
**Status**: Draft
**Input**: Implement authentication flows, dashboard statistics, global search, and user profile endpoints

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authentication Endpoints (Priority: P1)

As a user, I want complete authentication functionality so that I can securely access the application.

**Why this priority**: Authentication is foundational - all other endpoints depend on secure user access.

**Independent Test**: Can be verified by testing login, logout, registration, and token flows.

**Acceptance Scenarios**:

1. **Given** I have valid credentials, **When** I POST to /api/v1/auth/login/, **Then** I receive an authentication token
2. **Given** I have an invalid password, **When** I POST to /api/v1/auth/login/, **Then** I receive 400 Bad Request with error message
3. **Given** I have a valid token, **When** I POST to /api/v1/auth/logout/, **Then** my token is deleted and I receive 200 OK
4. **Given** I provide valid registration data, **When** I POST to /api/v1/auth/register/, **Then** a new user is created and I receive a token
5. **Given** I try to register with an existing username, **When** I POST to /api/v1/auth/register/, **Then** I receive 400 Bad Request
6. **Given** I have a valid token, **When** I GET /api/v1/auth/me/, **Then** I receive my user information
7. **Given** I have no token, **When** I GET /api/v1/auth/me/, **Then** I receive 401 Unauthorized

---

### User Story 2 - Dashboard Statistics (Priority: P1)

As a legal professional, I want a dashboard with key metrics so that I can quickly understand my workload and case status.

**Why this priority**: Dashboard provides critical business overview for daily operations.

**Independent Test**: Can be verified by accessing /api/v1/dashboard/ and checking all returned statistics.

**Acceptance Scenarios**:

1. **Given** I am authenticated, **When** I GET /api/v1/dashboard/, **Then** I receive total_clients and active_clients counts
2. **Given** there are cases in the system, **When** I GET /api/v1/dashboard/, **Then** I see cases_by_status with count for each status
3. **Given** there are cases in the system, **When** I GET /api/v1/dashboard/, **Then** I see cases_by_type with count for each type
4. **Given** there are recent cases, **When** I GET /api/v1/dashboard/, **Then** I see recent_cases with the last 5 cases (id, case_number, title, status, client_name)
5. **Given** there are documents, **When** I GET /api/v1/dashboard/, **Then** I see documents_by_type with count for each document type
6. **Given** there are cases with deadlines, **When** I GET /api/v1/dashboard/, **Then** I see upcoming_deadlines with cases due in next 7 days
7. **Given** I am not authenticated, **When** I GET /api/v1/dashboard/, **Then** I receive 401 Unauthorized
8. **Given** I request dashboard, **When** the query runs, **Then** it uses optimized queries (annotate, select_related) for performance

---

### User Story 3 - Global Search (Priority: P2)

As a user, I want to search across all data so that I can quickly find clients, cases, or documents.

**Why this priority**: Search improves productivity but is not required for core functionality.

**Independent Test**: Can be verified by searching for terms that exist in different models.

**Acceptance Scenarios**:

1. **Given** I am authenticated, **When** I GET /api/v1/search/?q=García, **Then** I receive results from clients, cases, and documents
2. **Given** a client named "García" exists, **When** I search for "García", **Then** clients results include that client with type="client"
3. **Given** a case with title "García vs Smith" exists, **When** I search for "García", **Then** cases results include that case with type="case"
4. **Given** a document titled "Contrato García" exists, **When** I search for "García", **Then** documents results include that document with type="document"
5. **Given** many results exist, **When** I search, **Then** results are limited to 10 per model (max 30 total)
6. **Given** I search with empty query, **When** I GET /api/v1/search/?q=, **Then** I receive 400 Bad Request with error message
7. **Given** I am not authenticated, **When** I GET /api/v1/search/?q=test, **Then** I receive 401 Unauthorized

---

### User Story 4 - User Profile (Priority: P2)

As a user, I want to view and update my profile so that I can manage my account information.

**Why this priority**: Profile management is important but not critical for core legal workflows.

**Independent Test**: Can be verified by getting and updating user profile.

**Acceptance Scenarios**:

1. **Given** I am authenticated, **When** I GET /api/v1/profile/, **Then** I receive my profile with username, email, first_name, last_name, assigned_cases_count
2. **Given** I am authenticated, **When** I PATCH /api/v1/profile/ with new email, **Then** my email is updated
3. **Given** I am authenticated, **When** I PATCH /api/v1/profile/ with first_name and last_name, **Then** my name is updated
4. **Given** I try to change username, **When** I PATCH /api/v1/profile/, **Then** username remains unchanged (read-only)
5. **Given** I am not authenticated, **When** I access /api/v1/profile/, **Then** I receive 401 Unauthorized

---

### User Story 5 - Authentication Testing (Priority: P1)

As a developer, I want comprehensive tests for all authentication flows so that security is guaranteed.

**Why this priority**: Authentication testing is critical for security assurance.

**Independent Test**: Run pytest on authentication tests.

**Acceptance Scenarios**:

1. **Given** the test suite, **When** I run auth tests, **Then** login with valid/invalid credentials is tested
2. **Given** the test suite, **When** I run auth tests, **Then** logout flow is tested
3. **Given** the test suite, **When** I run auth tests, **Then** registration with valid/invalid/duplicate data is tested
4. **Given** the test suite, **When** I run auth tests, **Then** protected endpoint access is tested
5. **Given** the test suite, **When** I run auth tests, **Then** token expiration behavior is tested (if configured)

---

## Technical Requirements

### Authentication Configuration

```python
# Token authentication settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Optional: Token expiration (using django-rest-knox or custom)
# TOKEN_EXPIRED_AFTER_SECONDS = 86400  # 24 hours
```

### API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| /api/v1/auth/login/ | POST | Obtain auth token | No |
| /api/v1/auth/logout/ | POST | Delete auth token | Yes |
| /api/v1/auth/register/ | POST | Create new user | No |
| /api/v1/auth/me/ | GET | Get current user info | Yes |
| /api/v1/dashboard/ | GET | Get dashboard statistics | Yes |
| /api/v1/search/ | GET | Global search | Yes |
| /api/v1/profile/ | GET, PATCH | User profile | Yes |

### Dashboard Response Schema

```json
{
  "total_clients": 150,
  "active_clients": 120,
  "cases_by_status": {
    "abierto": 45,
    "en_proceso": 30,
    "cerrado": 75,
    "archivado": 10
  },
  "cases_by_type": {
    "civil": 50,
    "penal": 30,
    "laboral": 40,
    "familia": 25,
    "comercial": 15
  },
  "recent_cases": [
    {
      "id": 1,
      "case_number": "CASO-2026-0001",
      "title": "García vs. Martínez",
      "status": "en_proceso",
      "client_name": "Juan García"
    }
  ],
  "documents_by_type": {
    "contrato": 45,
    "demanda": 30,
    "poder": 25,
    "sentencia": 15,
    "escritura": 20,
    "otro": 10
  },
  "upcoming_deadlines": [
    {
      "id": 5,
      "case_number": "CASO-2026-0005",
      "title": "Caso urgente",
      "deadline": "2026-01-20",
      "days_remaining": 4,
      "client_name": "María López"
    }
  ]
}
```

### Search Response Schema

```json
{
  "query": "García",
  "results": {
    "clients": [
      {
        "id": 1,
        "type": "client",
        "full_name": "Juan García",
        "email": "juan.garcia@email.com"
      }
    ],
    "cases": [
      {
        "id": 5,
        "type": "case",
        "case_number": "CASO-2026-0005",
        "title": "García vs. Smith"
      }
    ],
    "documents": [
      {
        "id": 10,
        "type": "document",
        "title": "Contrato García",
        "document_type": "contrato"
      }
    ]
  },
  "counts": {
    "clients": 1,
    "cases": 1,
    "documents": 1,
    "total": 3
  }
}
```

### User Registration Request Schema

```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### User Profile Response Schema

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "assigned_cases_count": 15,
  "date_joined": "2026-01-01T00:00:00Z"
}
```

---

## Implementation Notes

1. **Authentication Views**: Create in `api/views.py` using DRF's ObtainAuthToken as base
2. **Token Deletion**: Use Token.objects.filter(user=request.user).delete() for logout
3. **Dashboard Queries**: Use Django ORM annotate() and values() for aggregations
4. **Search Implementation**: Use Q objects for OR queries across models
5. **Query Optimization**: Use select_related for foreign keys, prefetch_related for reverse relations
6. **Testing**: Use APITestCase from rest_framework.test with APIClient

---

## File Structure

```
legaldocs/
├── api/
│   ├── views.py          # Add auth views, dashboard, search, profile
│   ├── serializers.py    # Add auth and profile serializers
│   ├── urls.py           # Add new endpoint routes
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py      # Authentication tests
│       ├── test_dashboard.py # Dashboard tests
│       ├── test_search.py    # Search tests
│       └── test_profile.py   # Profile tests
```

---

## Dependencies

- djangorestframework (already installed)
- rest_framework.authtoken (already configured)

No additional dependencies required.

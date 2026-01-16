# LegalDocs Manager API Documentation

Complete API reference for LegalDocs Manager REST API.

**Base URL**: `/api/v1/`

## Table of Contents

- [Authentication](#authentication)
- [Clients](#clients)
- [Cases](#cases)
- [Documents](#documents)
- [Dashboard](#dashboard)
- [Search](#search)
- [Profile](#profile)
- [Error Responses](#error-responses)
- [Pagination](#pagination)

---

## Authentication

All endpoints (except registration and login) require authentication via Token Authentication.

Include the token in the `Authorization` header:

```
Authorization: Token <your-token>
```

### Register

Create a new user account.

**Endpoint**: `POST /api/v1/auth/register/`

**Authentication**: Not required

**Request Body**:

```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response** (201 Created):

```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Login

Authenticate and receive a token.

**Endpoint**: `POST /api/v1/auth/login/`

**Authentication**: Not required

**Request Body**:

```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

**Response** (200 OK):

```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "johndoe"
}
```

### Logout

Invalidate the current token.

**Endpoint**: `POST /api/v1/auth/logout/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "detail": "Successfully logged out."
}
```

### Get Current User

Retrieve information about the authenticated user.

**Endpoint**: `GET /api/v1/auth/me/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
}
```

---

## Clients

Manage client records.

### List Clients

Get a paginated list of clients.

**Endpoint**: `GET /api/v1/clients/`

**Authentication**: Required

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `is_active` | boolean | Filter by active status |
| `search` | string | Search by name, email, or ID number |
| `ordering` | string | Order by field (e.g., `full_name`, `-created_at`) |
| `page` | integer | Page number |

**Example**: `GET /api/v1/clients/?is_active=true&search=Garcia&ordering=full_name`

**Response** (200 OK):

```json
{
    "count": 25,
    "next": "http://localhost:8000/api/v1/clients/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "full_name": "Juan García Pérez",
            "identification_number": "12345678-9",
            "email": "juan.garcia@example.com",
            "phone": "+56 9 1234 5678",
            "address": "Av. Principal 123, Santiago",
            "is_active": true,
            "created_at": "2026-01-15T10:30:00Z",
            "updated_at": "2026-01-15T10:30:00Z"
        }
    ]
}
```

### Create Client

Create a new client.

**Endpoint**: `POST /api/v1/clients/`

**Authentication**: Required

**Request Body**:

```json
{
    "full_name": "María López Silva",
    "identification_number": "98765432-1",
    "email": "maria.lopez@example.com",
    "phone": "+56 9 8765 4321",
    "address": "Calle Secundaria 456, Valparaíso",
    "notes": "Referred by Juan García"
}
```

**Response** (201 Created):

```json
{
    "id": 2,
    "full_name": "María López Silva",
    "identification_number": "98765432-1",
    "email": "maria.lopez@example.com",
    "phone": "+56 9 8765 4321",
    "address": "Calle Secundaria 456, Valparaíso",
    "is_active": true,
    "created_at": "2026-01-16T14:00:00Z",
    "updated_at": "2026-01-16T14:00:00Z"
}
```

### Get Client Detail

Retrieve a specific client with additional details.

**Endpoint**: `GET /api/v1/clients/{id}/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "id": 1,
    "full_name": "Juan García Pérez",
    "identification_number": "12345678-9",
    "email": "juan.garcia@example.com",
    "phone": "+56 9 1234 5678",
    "address": "Av. Principal 123, Santiago",
    "notes": "VIP client",
    "is_active": true,
    "case_count": 3,
    "created_at": "2026-01-15T10:30:00Z",
    "updated_at": "2026-01-15T10:30:00Z"
}
```

### Update Client

Update a client (full update).

**Endpoint**: `PUT /api/v1/clients/{id}/`

**Authentication**: Required

**Request Body**: Same as Create Client (all fields required)

### Partial Update Client

Update specific fields of a client.

**Endpoint**: `PATCH /api/v1/clients/{id}/`

**Authentication**: Required

**Request Body**:

```json
{
    "phone": "+56 9 1111 2222"
}
```

### Delete Client

Delete a client.

**Endpoint**: `DELETE /api/v1/clients/{id}/`

**Authentication**: Required

**Response** (204 No Content)

### Get Client's Cases

List all cases for a specific client.

**Endpoint**: `GET /api/v1/clients/{id}/cases/`

**Authentication**: Required

**Response** (200 OK):

```json
[
    {
        "id": 1,
        "case_number": "CASE-20260115-0001",
        "title": "Demanda por incumplimiento de contrato",
        "case_type": "civil",
        "status": "en_proceso",
        "priority": "alta",
        "start_date": "2026-01-15"
    }
]
```

---

## Cases

Manage legal cases.

### List Cases

Get a paginated list of cases.

**Endpoint**: `GET /api/v1/cases/`

**Authentication**: Required

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status (`en_proceso`, `pendiente_documentos`, `en_revision`, `cerrado`) |
| `case_type` | string | Filter by type (`civil`, `penal`, `laboral`, `mercantil`, `familia`) |
| `priority` | string | Filter by priority (`baja`, `media`, `alta`, `urgente`) |
| `client` | integer | Filter by client ID |
| `search` | string | Search by title or case number |
| `ordering` | string | Order by field (e.g., `-start_date`, `title`) |

**Example**: `GET /api/v1/cases/?status=en_proceso&priority=alta`

**Response** (200 OK):

```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "case_number": "CASE-20260115-0001",
            "client": 1,
            "client_name": "Juan García Pérez",
            "title": "Demanda por incumplimiento de contrato",
            "description": "Cliente demanda a proveedor por incumplimiento...",
            "case_type": "civil",
            "status": "en_proceso",
            "priority": "alta",
            "start_date": "2026-01-15",
            "closed_date": null,
            "created_at": "2026-01-15T10:30:00Z",
            "updated_at": "2026-01-15T10:30:00Z"
        }
    ]
}
```

### Create Case

Create a new case.

**Endpoint**: `POST /api/v1/cases/`

**Authentication**: Required

**Request Body**:

```json
{
    "client": 1,
    "title": "Defensa penal por hurto",
    "description": "Cliente acusado de hurto en establecimiento comercial...",
    "case_type": "penal",
    "priority": "urgente",
    "start_date": "2026-01-16"
}
```

**Response** (201 Created):

```json
{
    "id": 2,
    "case_number": "CASE-20260116-0001",
    "client": 1,
    "client_name": "Juan García Pérez",
    "title": "Defensa penal por hurto",
    "description": "Cliente acusado de hurto en establecimiento comercial...",
    "case_type": "penal",
    "status": "en_proceso",
    "priority": "urgente",
    "start_date": "2026-01-16",
    "closed_date": null,
    "created_at": "2026-01-16T14:00:00Z",
    "updated_at": "2026-01-16T14:00:00Z"
}
```

### Get Case Detail

Retrieve a specific case with nested client and documents.

**Endpoint**: `GET /api/v1/cases/{id}/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "id": 1,
    "case_number": "CASE-20260115-0001",
    "client": {
        "id": 1,
        "full_name": "Juan García Pérez",
        "email": "juan.garcia@example.com",
        "phone": "+56 9 1234 5678"
    },
    "title": "Demanda por incumplimiento de contrato",
    "description": "Cliente demanda a proveedor por incumplimiento...",
    "case_type": "civil",
    "status": "en_proceso",
    "priority": "alta",
    "start_date": "2026-01-15",
    "closed_date": null,
    "documents": [
        {
            "id": 1,
            "title": "Contrato original",
            "document_type": "contrato",
            "uploaded_at": "2026-01-15T11:00:00Z"
        }
    ],
    "created_at": "2026-01-15T10:30:00Z",
    "updated_at": "2026-01-15T10:30:00Z"
}
```

### Update Case

Update a case (full update).

**Endpoint**: `PUT /api/v1/cases/{id}/`

### Partial Update Case

Update specific fields of a case.

**Endpoint**: `PATCH /api/v1/cases/{id}/`

**Request Body**:

```json
{
    "status": "en_revision",
    "priority": "media"
}
```

### Delete Case

Delete a case.

**Endpoint**: `DELETE /api/v1/cases/{id}/`

**Response** (204 No Content)

### Close Case

Close a case (sets status to "cerrado" and records closed_date).

**Endpoint**: `POST /api/v1/cases/{id}/close/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "id": 1,
    "case_number": "CASE-20260115-0001",
    "status": "cerrado",
    "closed_date": "2026-01-16"
}
```

**Error Response** (400 Bad Request - already closed):

```json
{
    "error": "Este caso ya está cerrado."
}
```

### Case Statistics

Get aggregate statistics about cases.

**Endpoint**: `GET /api/v1/cases/statistics/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "total": 45,
    "by_status": {
        "en_proceso": 20,
        "pendiente_documentos": 10,
        "en_revision": 5,
        "cerrado": 10
    },
    "by_type": {
        "civil": 15,
        "penal": 10,
        "laboral": 8,
        "mercantil": 7,
        "familia": 5
    },
    "by_priority": {
        "baja": 10,
        "media": 20,
        "alta": 10,
        "urgente": 5
    }
}
```

---

## Documents

Manage legal documents with file uploads.

### List Documents

Get a paginated list of documents.

**Endpoint**: `GET /api/v1/documents/`

**Authentication**: Required

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `case` | integer | Filter by case ID |
| `document_type` | string | Filter by type (`contrato`, `demanda`, `poder`, `sentencia`, `escritura`, `otro`) |
| `is_confidential` | boolean | Filter by confidentiality |
| `search` | string | Search by title or description |
| `ordering` | string | Order by field (e.g., `-uploaded_at`, `title`) |

**Response** (200 OK):

```json
{
    "count": 50,
    "next": "http://localhost:8000/api/v1/documents/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "case": 1,
            "case_number": "CASE-20260115-0001",
            "title": "Contrato de servicios",
            "document_type": "contrato",
            "description": "Contrato original firmado por ambas partes",
            "file": "/media/documents/contrato_servicios.pdf",
            "file_size": 524288,
            "is_confidential": false,
            "uploaded_by": 1,
            "uploaded_by_username": "johndoe",
            "uploaded_at": "2026-01-15T11:00:00Z"
        }
    ]
}
```

### Upload Document

Upload a new document.

**Endpoint**: `POST /api/v1/documents/`

**Authentication**: Required

**Content-Type**: `multipart/form-data`

**Request Body**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `case` | integer | Yes | Case ID |
| `title` | string | Yes | Document title |
| `document_type` | string | Yes | Type of document |
| `description` | string | No | Document description |
| `file` | file | Yes | The document file |
| `is_confidential` | boolean | No | Mark as confidential (default: false) |

**Example using cURL**:

```bash
curl -X POST http://localhost:8000/api/v1/documents/ \
  -H "Authorization: Token your-token" \
  -F "case=1" \
  -F "title=Demanda inicial" \
  -F "document_type=demanda" \
  -F "description=Demanda presentada ante el tribunal" \
  -F "file=@/path/to/demanda.pdf" \
  -F "is_confidential=false"
```

**Response** (201 Created):

```json
{
    "id": 2,
    "case": 1,
    "case_number": "CASE-20260115-0001",
    "title": "Demanda inicial",
    "document_type": "demanda",
    "description": "Demanda presentada ante el tribunal",
    "file": "/media/documents/demanda_inicial.pdf",
    "file_size": 1048576,
    "is_confidential": false,
    "uploaded_by": 1,
    "uploaded_by_username": "johndoe",
    "uploaded_at": "2026-01-16T14:30:00Z"
}
```

### Get Document Detail

Retrieve a specific document.

**Endpoint**: `GET /api/v1/documents/{id}/`

### Update Document

Update a document (requires re-uploading the file).

**Endpoint**: `PUT /api/v1/documents/{id}/`

**Content-Type**: `multipart/form-data`

### Partial Update Document

Update document metadata (without changing the file).

**Endpoint**: `PATCH /api/v1/documents/{id}/`

**Request Body**:

```json
{
    "is_confidential": true
}
```

### Delete Document

Delete a document.

**Endpoint**: `DELETE /api/v1/documents/{id}/`

**Authentication**: Required (Owner or Staff only)

**Response** (204 No Content)

**Error Response** (403 Forbidden - not owner):

```json
{
    "detail": "You do not have permission to perform this action."
}
```

---

## Dashboard

Get overview statistics for the dashboard.

**Endpoint**: `GET /api/v1/dashboard/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "clients": {
        "total": 25,
        "active": 20
    },
    "cases": {
        "total": 45,
        "active": 35,
        "by_status": {
            "en_proceso": 20,
            "pendiente_documentos": 10,
            "en_revision": 5,
            "cerrado": 10
        }
    },
    "documents": {
        "total": 150
    },
    "recent_cases": [
        {
            "id": 1,
            "case_number": "CASE-20260115-0001",
            "title": "Demanda por incumplimiento",
            "status": "en_proceso"
        }
    ]
}
```

---

## Search

Global search across clients, cases, and documents.

**Endpoint**: `GET /api/v1/search/`

**Authentication**: Required

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query (minimum 2 characters) |

**Example**: `GET /api/v1/search/?q=Garcia`

**Response** (200 OK):

```json
{
    "clients": [
        {
            "id": 1,
            "full_name": "Juan García Pérez",
            "email": "juan.garcia@example.com"
        }
    ],
    "cases": [
        {
            "id": 5,
            "case_number": "CASE-20260110-0003",
            "title": "García vs. Empresa ABC"
        }
    ],
    "documents": [
        {
            "id": 10,
            "title": "Poder García",
            "document_type": "poder"
        }
    ]
}
```

---

## Profile

Manage the current user's profile.

### Get Profile

**Endpoint**: `GET /api/v1/profile/`

**Authentication**: Required

**Response** (200 OK):

```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Update Profile

**Endpoint**: `PATCH /api/v1/profile/`

**Authentication**: Required

**Request Body**:

```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

---

## Error Responses

### Standard Error Format

```json
{
    "detail": "Error message here."
}
```

### Validation Errors

```json
{
    "field_name": [
        "Error message for this field."
    ]
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Delete successful |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

---

## Pagination

All list endpoints return paginated responses.

**Default page size**: 20 items

**Response format**:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/v1/endpoint/?page=2",
    "previous": null,
    "results": [...]
}
```

To navigate pages, use the `page` query parameter:

```
GET /api/v1/clients/?page=2
```

---

## Interactive Documentation

For interactive API documentation, visit:

- **Swagger UI**: `/api/v1/docs/`
- **OpenAPI Schema**: `/api/v1/schema/`

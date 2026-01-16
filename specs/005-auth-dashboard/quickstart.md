# Quickstart: Authentication and Dashboard Views

**Feature**: 005-auth-dashboard
**Date**: 2026-01-16

## Prerequisites

1. Django development server running: `python manage.py runserver`
2. Database migrated with existing Client, Case, Document data
3. At least one superuser created: `python manage.py createsuperuser`

## API Endpoints Summary

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| /api/v1/auth/login/ | POST | No | Obtain token |
| /api/v1/auth/logout/ | POST | Yes | Delete token |
| /api/v1/auth/register/ | POST | No | Create user |
| /api/v1/auth/me/ | GET | Yes | Current user info |
| /api/v1/dashboard/ | GET | Yes | Statistics |
| /api/v1/search/?q=term | GET | Yes | Global search |
| /api/v1/profile/ | GET, PATCH | Yes | User profile |

---

## Test Scenarios

### 1. Authentication Flow

#### 1.1 Login with Valid Credentials

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpassword"}'
```

**Expected Response (200 OK)**:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "username": "admin"
}
```

#### 1.2 Login with Invalid Credentials

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "wrongpassword"}'
```

**Expected Response (400 Bad Request)**:
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```

#### 1.3 Logout

```bash
curl -X POST http://localhost:8000/api/v1/auth/logout/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (200 OK)**:
```json
{
  "detail": "Successfully logged out."
}
```

#### 1.4 Get Current User Info

```bash
curl http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User"
}
```

#### 1.5 Access Protected Endpoint Without Token

```bash
curl http://localhost:8000/api/v1/auth/me/
```

**Expected Response (401 Unauthorized)**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 2. User Registration

#### 2.1 Register New User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "New",
    "last_name": "User"
  }'
```

**Expected Response (201 Created)**:
```json
{
  "token": "abc123def456...",
  "user": {
    "id": 2,
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "New",
    "last_name": "User"
  }
}
```

#### 2.2 Register with Existing Username

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "another@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

**Expected Response (400 Bad Request)**:
```json
{
  "username": ["A user with that username already exists."]
}
```

#### 2.3 Register with Mismatched Passwords

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser2",
    "email": "newuser2@example.com",
    "password": "securepass123",
    "password_confirm": "differentpass"
  }'
```

**Expected Response (400 Bad Request)**:
```json
{
  "non_field_errors": ["Passwords do not match."]
}
```

---

### 3. Dashboard Statistics

#### 3.1 Get Dashboard Data

```bash
curl http://localhost:8000/api/v1/dashboard/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (200 OK)**:
```json
{
  "total_clients": 150,
  "active_clients": 120,
  "cases_by_status": {
    "en_proceso": 45,
    "pendiente_documentos": 20,
    "en_revision": 15,
    "cerrado": 80
  },
  "cases_by_type": {
    "civil": 50,
    "penal": 30,
    "laboral": 40,
    "mercantil": 25,
    "familia": 15
  },
  "recent_cases": [
    {
      "id": 160,
      "case_number": "CASE-2026-0160",
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
      "id": 155,
      "case_number": "CASE-2026-0155",
      "title": "Caso urgente",
      "deadline": "2026-01-20",
      "days_remaining": 4,
      "client_name": "María López"
    }
  ]
}
```

#### 3.2 Dashboard Without Authentication

```bash
curl http://localhost:8000/api/v1/dashboard/
```

**Expected Response (401 Unauthorized)**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 4. Global Search

#### 4.1 Search with Results

```bash
curl "http://localhost:8000/api/v1/search/?q=García" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (200 OK)**:
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
        "case_number": "CASE-2026-0005",
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

#### 4.2 Search with No Results

```bash
curl "http://localhost:8000/api/v1/search/?q=nonexistent" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (200 OK)**:
```json
{
  "query": "nonexistent",
  "results": {
    "clients": [],
    "cases": [],
    "documents": []
  },
  "counts": {
    "clients": 0,
    "cases": 0,
    "documents": 0,
    "total": 0
  }
}
```

#### 4.3 Search with Empty Query

```bash
curl "http://localhost:8000/api/v1/search/?q=" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (400 Bad Request)**:
```json
{
  "error": "Query parameter 'q' is required and cannot be empty."
}
```

#### 4.4 Search Without Query Parameter

```bash
curl "http://localhost:8000/api/v1/search/" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (400 Bad Request)**:
```json
{
  "error": "Query parameter 'q' is required and cannot be empty."
}
```

---

### 5. User Profile

#### 5.1 Get Profile

```bash
curl http://localhost:8000/api/v1/profile/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "assigned_cases_count": 15,
  "date_joined": "2026-01-01T00:00:00Z"
}
```

#### 5.2 Update Profile (Partial)

```bash
curl -X PATCH http://localhost:8000/api/v1/profile/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Administrator", "last_name": "Supreme"}'
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Administrator",
  "last_name": "Supreme",
  "assigned_cases_count": 15,
  "date_joined": "2026-01-01T00:00:00Z"
}
```

#### 5.3 Update Email

```bash
curl -X PATCH http://localhost:8000/api/v1/profile/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"email": "newemail@example.com"}'
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "newemail@example.com",
  "first_name": "Administrator",
  "last_name": "Supreme",
  "assigned_cases_count": 15,
  "date_joined": "2026-01-01T00:00:00Z"
}
```

#### 5.4 Attempt to Update Username (Read-Only)

```bash
curl -X PATCH http://localhost:8000/api/v1/profile/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"username": "newadmin"}'
```

**Expected Response (200 OK)** - Username unchanged:
```json
{
  "id": 1,
  "username": "admin",
  "email": "newemail@example.com",
  "first_name": "Administrator",
  "last_name": "Supreme",
  "assigned_cases_count": 15,
  "date_joined": "2026-01-01T00:00:00Z"
}
```

---

## Verification Checklist

### Authentication (US1)
- [ ] POST /auth/login/ returns token with valid credentials
- [ ] POST /auth/login/ returns 400 with invalid credentials
- [ ] POST /auth/logout/ deletes token (subsequent requests fail)
- [ ] POST /auth/register/ creates user and returns token
- [ ] POST /auth/register/ returns 400 for duplicate username
- [ ] POST /auth/register/ returns 400 for mismatched passwords
- [ ] GET /auth/me/ returns user info with valid token
- [ ] GET /auth/me/ returns 401 without token

### Dashboard (US2)
- [ ] GET /dashboard/ returns total_clients count
- [ ] GET /dashboard/ returns active_clients count
- [ ] GET /dashboard/ returns cases_by_status object
- [ ] GET /dashboard/ returns cases_by_type object
- [ ] GET /dashboard/ returns recent_cases array (max 5)
- [ ] GET /dashboard/ returns documents_by_type object
- [ ] GET /dashboard/ returns upcoming_deadlines (next 7 days)
- [ ] GET /dashboard/ returns 401 without authentication

### Search (US3)
- [ ] GET /search/?q=term returns matching clients
- [ ] GET /search/?q=term returns matching cases
- [ ] GET /search/?q=term returns matching documents
- [ ] GET /search/?q=term limits results to 10 per model
- [ ] GET /search/?q= returns 400 for empty query
- [ ] GET /search/ returns 400 for missing query
- [ ] GET /search/ returns 401 without authentication

### Profile (US4)
- [ ] GET /profile/ returns user profile with assigned_cases_count
- [ ] PATCH /profile/ updates email
- [ ] PATCH /profile/ updates first_name and last_name
- [ ] PATCH /profile/ ignores username (read-only)
- [ ] GET /profile/ returns 401 without authentication

### Tests (US5)
- [ ] All authentication tests pass
- [ ] All dashboard tests pass
- [ ] All search tests pass
- [ ] All profile tests pass

# Quickstart Guide: Django REST Framework API

**Feature**: 004-rest-api | **Date**: 2026-01-16

## Prerequisites

- Virtual environment activated: `source venv/bin/activate`
- Database running with fixtures loaded
- Superuser account created (admin/admin123)
- Dependencies installed (see below)

## Install Dependencies

```bash
cd /home/juanca/proys/LegalDocs-Manager
source venv/bin/activate
pip install djangorestframework django-filter drf-spectacular django-cors-headers
```

## Starting the API

```bash
cd legaldocs
python manage.py runserver
```

## Getting an Authentication Token

```bash
# Get token with username/password
curl -X POST http://localhost:8000/api/v1/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Response: {"token": "abc123..."}

# Use token in subsequent requests
export TOKEN="your-token-here"
```

## Testing Checklist

### 1. Authentication

```bash
# Without token - should return 401
curl http://localhost:8000/api/v1/clients/

# With token - should return 200
curl http://localhost:8000/api/v1/clients/ \
  -H "Authorization: Token $TOKEN"
```

- [ ] Unauthenticated request returns 401
- [ ] Token auth endpoint returns valid token
- [ ] Authenticated request returns 200

### 2. Client API Testing

Navigate to: http://localhost:8000/api/v1/clients/

#### List Clients

```bash
# List all clients
curl http://localhost:8000/api/v1/clients/ \
  -H "Authorization: Token $TOKEN"

# Filter by is_active
curl "http://localhost:8000/api/v1/clients/?is_active=true" \
  -H "Authorization: Token $TOKEN"

# Search by name
curl "http://localhost:8000/api/v1/clients/?search=García" \
  -H "Authorization: Token $TOKEN"
```

- [ ] List returns paginated results (count, next, previous, results)
- [ ] Results don't include 'notes' field
- [ ] Filter by is_active works
- [ ] Search by name/email works

#### Create Client

```bash
curl -X POST http://localhost:8000/api/v1/clients/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Client",
    "identification_number": "TEST-001",
    "email": "test@example.com",
    "phone": "555-0000",
    "is_active": true
  }'
```

- [ ] POST creates client and returns 201
- [ ] created_at and updated_at are set automatically

#### Retrieve Client Detail

```bash
curl http://localhost:8000/api/v1/clients/1/ \
  -H "Authorization: Token $TOKEN"
```

- [ ] Detail view includes 'notes' field
- [ ] Detail view includes 'case_count' computed field

#### Get Client's Cases

```bash
curl http://localhost:8000/api/v1/clients/1/cases/ \
  -H "Authorization: Token $TOKEN"
```

- [ ] Returns array of cases for that client
- [ ] Returns 404 for non-existent client

### 3. Case API Testing

Navigate to: http://localhost:8000/api/v1/cases/

#### List Cases

```bash
# List all cases
curl http://localhost:8000/api/v1/cases/ \
  -H "Authorization: Token $TOKEN"

# Filter by status
curl "http://localhost:8000/api/v1/cases/?status=en_proceso" \
  -H "Authorization: Token $TOKEN"

# Filter by client
curl "http://localhost:8000/api/v1/cases/?client=1" \
  -H "Authorization: Token $TOKEN"

# Order by start_date descending
curl "http://localhost:8000/api/v1/cases/?ordering=-start_date" \
  -H "Authorization: Token $TOKEN"
```

- [ ] List includes client_name field
- [ ] Filter by status works
- [ ] Filter by case_type works
- [ ] Filter by priority works
- [ ] Filter by client works
- [ ] Ordering works

#### Create Case

```bash
curl -X POST http://localhost:8000/api/v1/cases/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client": 1,
    "title": "Test Case",
    "case_type": "civil",
    "status": "en_proceso",
    "priority": "media",
    "start_date": "2026-01-16"
  }'
```

- [ ] POST creates case with auto-generated case_number
- [ ] case_number follows format CASO-YYYYMMDD-XXX

#### Retrieve Case Detail

```bash
curl http://localhost:8000/api/v1/cases/1/ \
  -H "Authorization: Token $TOKEN"
```

- [ ] Detail view includes nested client object
- [ ] Detail view includes documents array

#### Close Case Action

```bash
curl -X POST http://localhost:8000/api/v1/cases/1/close/ \
  -H "Authorization: Token $TOKEN"
```

- [ ] Sets status to 'cerrado'
- [ ] Sets closed_date to today
- [ ] Returns 400 if already closed

#### Get Statistics

```bash
curl http://localhost:8000/api/v1/cases/statistics/ \
  -H "Authorization: Token $TOKEN"
```

- [ ] Returns by_status counts
- [ ] Returns by_type counts
- [ ] Returns by_priority counts
- [ ] Returns total count

### 4. Document API Testing

Navigate to: http://localhost:8000/api/v1/documents/

#### List Documents

```bash
curl http://localhost:8000/api/v1/documents/ \
  -H "Authorization: Token $TOKEN"

# Filter by case
curl "http://localhost:8000/api/v1/documents/?case=1" \
  -H "Authorization: Token $TOKEN"

# Filter by confidential
curl "http://localhost:8000/api/v1/documents/?is_confidential=true" \
  -H "Authorization: Token $TOKEN"
```

- [ ] List includes case_number field
- [ ] List includes uploaded_by_username field
- [ ] Filter by case works
- [ ] Filter by document_type works
- [ ] Filter by is_confidential works

#### Upload Document

```bash
curl -X POST http://localhost:8000/api/v1/documents/ \
  -H "Authorization: Token $TOKEN" \
  -F "case=1" \
  -F "title=Test Document" \
  -F "document_type=contrato" \
  -F "file=@/path/to/test.pdf"
```

- [ ] POST accepts multipart/form-data
- [ ] uploaded_by is auto-set to current user
- [ ] uploaded_at is auto-set
- [ ] file_size is calculated

#### Delete Document (Permissions)

```bash
# Owner can delete
curl -X DELETE http://localhost:8000/api/v1/documents/1/ \
  -H "Authorization: Token $TOKEN"

# Non-owner gets 403 (test with different user)
```

- [ ] Document owner can delete (204)
- [ ] Admin can delete any document (204)
- [ ] Non-owner gets 403 Forbidden

### 5. API Documentation

```bash
# Download OpenAPI schema
curl http://localhost:8000/api/v1/schema/ -o schema.yaml

# View Swagger UI
open http://localhost:8000/api/v1/docs/
```

- [ ] Schema endpoint returns OpenAPI 3.0 YAML
- [ ] Swagger UI is accessible and interactive

### 6. Pagination Testing

```bash
# First page (default)
curl http://localhost:8000/api/v1/clients/ \
  -H "Authorization: Token $TOKEN"

# Second page
curl "http://localhost:8000/api/v1/clients/?page=2" \
  -H "Authorization: Token $TOKEN"
```

- [ ] Response includes count, next, previous, results
- [ ] PAGE_SIZE is 20 items
- [ ] next/previous URLs are correct

### 7. CORS Testing (from browser)

Open browser console on http://localhost:3000 (if frontend exists):

```javascript
fetch('http://localhost:8000/api/v1/clients/', {
  headers: {
    'Authorization': 'Token your-token-here'
  }
})
.then(r => r.json())
.then(console.log)
```

- [ ] Request from localhost:3000 is allowed
- [ ] CORS headers present in response

## Using the Browsable API

DRF provides a web-based interface for testing:

1. Navigate to http://localhost:8000/api/v1/
2. Log in using session auth (top right)
3. Browse endpoints interactively
4. Use forms to POST/PUT/PATCH data

## Common Issues

### Issue: 401 Unauthorized

**Problem**: All requests return 401

**Solution**: Ensure token is correct and header format is `Authorization: Token <token>` (not `Bearer`)

### Issue: 403 Forbidden on DELETE

**Problem**: Cannot delete document

**Solution**: Verify you are the document owner or an admin user

### Issue: CORS error in browser

**Problem**: CORS policy blocking request

**Solution**: Ensure `django-cors-headers` is installed and configured:
```python
INSTALLED_APPS = [..., 'corsheaders', ...]
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
```

### Issue: Filtering not working

**Problem**: Query params ignored

**Solution**: Ensure `django-filter` is installed and DjangoFilterBackend is in filter_backends

## Next Steps

After verifying all API features work correctly:

1. Create API tests using DRF's APITestCase
2. Add rate limiting if needed
3. Implement caching for statistics endpoint
4. Proceed to frontend implementation

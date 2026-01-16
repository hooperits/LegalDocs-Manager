# Quickstart: Testing and Documentation Verification

**Feature**: 006-testing-docs
**Date**: 2026-01-16

## Prerequisites

```bash
cd /home/juanca/proys/LegalDocs-Manager
source venv/bin/activate
cd legaldocs
```

---

## 1. Verify Test Suite

### Run All Tests

```bash
python manage.py test --verbosity=2
```

**Expected**: All tests pass (100+ tests)

### Run Tests by App

```bash
# Client tests
python manage.py test clients.tests --verbosity=2

# Case tests
python manage.py test cases.tests --verbosity=2

# Document tests
python manage.py test documents.tests --verbosity=2

# API tests (existing + integration)
python manage.py test api.tests --verbosity=2
```

### Run with Coverage

```bash
# Install coverage if not present
pip install coverage

# Run tests with coverage
coverage run --source='clients,cases,documents,api' manage.py test

# View coverage report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

**Expected**: Coverage ≥ 70%

---

## 2. Verify Demo Data

### Load Demo Data

```bash
python manage.py load_demo_data
```

**Expected Output**:
```
Loading demo data...
Loaded 20 clients
Loaded 30 cases
Loaded 50 documents
Demo data loaded successfully!
```

### Verify Data Counts

```bash
python manage.py shell -c "
from clients.models import Client
from cases.models import Case
from documents.models import Document

print(f'Clients: {Client.objects.count()}')
print(f'Cases: {Case.objects.count()}')
print(f'Documents: {Document.objects.count()}')
"
```

**Expected**:
- Clients: ≥20
- Cases: ≥30
- Documents: ≥50

### Verify Data Relationships

```bash
python manage.py shell -c "
from clients.models import Client
from cases.models import Case

# Check all cases have clients
orphan_cases = Case.objects.filter(client__isnull=True).count()
print(f'Orphan cases: {orphan_cases}')

# Check case distribution by type
from django.db.models import Count
types = Case.objects.values('case_type').annotate(count=Count('id'))
for t in types:
    print(f'{t[\"case_type\"]}: {t[\"count\"]} cases')
"
```

**Expected**:
- Orphan cases: 0
- Cases distributed across all types

---

## 3. Verify Documentation

### README.md Checklist

Open `README.md` and verify these sections exist:

- [ ] Project description
- [ ] Features list
- [ ] Tech stack
- [ ] Installation instructions
- [ ] Environment variables
- [ ] Database setup
- [ ] Running migrations
- [ ] Creating superuser
- [ ] Loading fixtures
- [ ] Running tests
- [ ] API endpoints overview

### API_DOCS.md Checklist

Open `API_DOCS.md` and verify:

- [ ] Authentication section
- [ ] All endpoints listed with methods
- [ ] Request examples for each endpoint
- [ ] Response examples for each endpoint
- [ ] Error response formats
- [ ] Pagination info
- [ ] Filter parameters

### DEPLOYMENT.md Checklist

Open `DEPLOYMENT.md` and verify:

- [ ] Pre-deployment checklist
- [ ] Production settings (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- [ ] Environment variables list
- [ ] Database migration strategy
- [ ] Static files handling
- [ ] Security recommendations

---

## 4. API Endpoint Verification

### Start Server

```bash
python manage.py runserver
```

### Test Authentication

```bash
# Register a test user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testdoc","email":"testdoc@example.com","password":"testpass123","password_confirm":"testpass123"}'

# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testdoc","password":"testpass123"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token: $TOKEN"
```

### Test Endpoints with Token

```bash
# Get clients
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/v1/clients/

# Get cases
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/v1/cases/

# Get dashboard
curl -H "Authorization: Token $TOKEN" http://localhost:8000/api/v1/dashboard/

# Search
curl -H "Authorization: Token $TOKEN" "http://localhost:8000/api/v1/search/?q=Garcia"
```

### Verify Swagger Documentation

Open in browser: http://localhost:8000/api/v1/docs/

**Expected**: Interactive API documentation loads with all endpoints

---

## 5. Test Specific Scenarios

### Model Test Scenarios

```bash
# Test Client model
python manage.py test clients.tests.test_models -v2

# Test Case model (including case_number generation)
python manage.py test cases.tests.test_models -v2

# Test Document model (including file_size calculation)
python manage.py test documents.tests.test_models -v2
```

### ViewSet Test Scenarios

```bash
# Test CRUD operations
python manage.py test clients.tests.test_views.ClientViewSetTests -v2

# Test custom actions
python manage.py test cases.tests.test_views.CaseViewSetTests.test_close_case -v2
python manage.py test cases.tests.test_views.CaseViewSetTests.test_statistics -v2

# Test file upload
python manage.py test documents.tests.test_views.DocumentViewSetTests.test_create_document_with_file -v2
```

### Integration Test Scenarios

```bash
# Test complete workflow
python manage.py test api.tests.test_integration -v2
```

---

## 6. Coverage Report Analysis

After running `coverage html`, open `htmlcov/index.html` and verify:

| Module | Target | Status |
|--------|--------|--------|
| clients/models.py | 80%+ | [ ] |
| cases/models.py | 80%+ | [ ] |
| documents/models.py | 80%+ | [ ] |
| clients/serializers.py | 80%+ | [ ] |
| cases/serializers.py | 80%+ | [ ] |
| documents/serializers.py | 80%+ | [ ] |
| clients/views.py | 70%+ | [ ] |
| cases/views.py | 70%+ | [ ] |
| documents/views.py | 70%+ | [ ] |
| api/views.py | 70%+ | [ ] |
| **Overall** | **70%+** | [ ] |

---

## 7. Final Verification Checklist

- [ ] `python manage.py test` - All tests pass
- [ ] `coverage report` - Overall ≥70%
- [ ] `python manage.py load_demo_data` - Runs without errors
- [ ] README.md - Complete and accurate
- [ ] API_DOCS.md - All endpoints documented
- [ ] DEPLOYMENT.md - Production guidelines complete
- [ ] Swagger UI - Loads at /api/v1/docs/
- [ ] All API endpoints - Return expected responses

---

## Troubleshooting

### Tests Fail with Database Error

```bash
# Ensure SQLite is used for tests (should be automatic)
# Check settings.py has test database config
```

### Coverage Too Low

```bash
# Check which lines are not covered
coverage html
# Review htmlcov/index.html for red (uncovered) lines
```

### Demo Data Fails to Load

```bash
# Load fixtures manually in order
python manage.py loaddata fixtures/demo_clients.json
python manage.py loaddata fixtures/demo_cases.json
python manage.py loaddata fixtures/demo_documents.json
```

### File Upload Tests Fail

```bash
# Ensure media directory exists
mkdir -p media/legal_documents

# Check file permissions
ls -la media/
```

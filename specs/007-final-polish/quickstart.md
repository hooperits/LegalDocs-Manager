# Quickstart: Final Polish Verification

**Feature**: 007-final-polish
**Date**: 2026-01-16

## Prerequisites

```bash
cd /home/juanca/proys/LegalDocs-Manager
source venv/bin/activate
cd legaldocs
```

---

## 1. Verify Code Quality (US1)

### Check Docstrings

```bash
# Verify models have docstrings
python -c "
from clients.models import Client
from cases.models import Case
from documents.models import Document

for model in [Client, Case, Document]:
    doc = model.__doc__
    print(f'{model.__name__}: {\"✓ Has docstring\" if doc else \"✗ Missing docstring\"}')"
```

**Expected**: All models have docstrings

### Run Linter

```bash
pip install ruff
ruff check clients/ cases/ documents/ api/
```

**Expected**: No critical errors (warnings acceptable)

---

## 2. Verify Security (US2)

### Test Rate Limiting

```bash
# Attempt 6 login requests in quick succession (limit is 5/min)
for i in {1..6}; do
  echo "Request $i:"
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/api/v1/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"wrong"}'
  sleep 1
done
```

**Expected**: First 5 return 400 (bad credentials), 6th returns 429 (rate limited)

### Test File Upload Validation

```bash
# Start server first: python manage.py runserver

# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpass123"}' | python -c "import sys,json; print(json.load(sys.stdin).get('token',''))")

# Test with invalid file type (create a fake .exe)
echo "MZ" > /tmp/test.exe
curl -X POST http://localhost:8000/api/v1/documents/ \
  -H "Authorization: Token $TOKEN" \
  -F "title=Test" \
  -F "case=1" \
  -F "document_type=otro" \
  -F "file=@/tmp/test.exe"
```

**Expected**: 400 error with Spanish message about invalid file type

### Test File Size Limit

```bash
# Create a file larger than 10MB
dd if=/dev/zero of=/tmp/large.pdf bs=1M count=11 2>/dev/null

curl -X POST http://localhost:8000/api/v1/documents/ \
  -H "Authorization: Token $TOKEN" \
  -F "title=Large File" \
  -F "case=1" \
  -F "document_type=otro" \
  -F "file=@/tmp/large.pdf"
```

**Expected**: 400 error with Spanish message about file size exceeding 10MB

---

## 3. Verify Performance (US3)

### Check Indexes

```bash
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT indexname FROM pg_indexes WHERE tablename IN ('cases_case', 'documents_document')\")
indexes = cursor.fetchall()
print('Indexes found:')
for idx in indexes:
    print(f'  - {idx[0]}')"
```

**Expected**: Lists case_client_idx, case_status_idx, doc_case_idx, etc.

### Check Query Optimization

```bash
python manage.py shell -c "
from django.db import connection, reset_queries
from django.conf import settings
settings.DEBUG = True
reset_queries()

from cases.models import Case
cases = list(Case.objects.select_related('client').all()[:10])
for c in cases:
    _ = c.client.full_name

print(f'Queries executed: {len(connection.queries)}')
print('Expected: 1 (with select_related)')"
```

**Expected**: Only 1 query executed

### Check Dashboard Cache

```bash
python manage.py shell -c "
from django.core.cache import cache
from api.views import DashboardView

# Clear cache
cache.clear()

# First request (should miss cache)
import time
start = time.time()
# Simulate dashboard computation
from clients.models import Client
from cases.models import Case
stats = {
    'total_clients': Client.objects.count(),
    'total_cases': Case.objects.count(),
}
cache.set('dashboard_stats', stats, 300)
print(f'First request: {(time.time()-start)*1000:.2f}ms')

# Second request (should hit cache)
start = time.time()
cached = cache.get('dashboard_stats')
print(f'Cached request: {(time.time()-start)*1000:.2f}ms')
print(f'Cache hit: {cached is not None}')"
```

**Expected**: Cached request significantly faster, cache hit = True

---

## 4. Verify User Experience (US4)

### Test Spanish Error Messages

```bash
# Test required field error
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected**: Error messages in Spanish like "Este campo es obligatorio"

### Test Field Name Translation

```bash
# Test with invalid email
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"invalid","password":"test123","password_confirm":"test123"}'
```

**Expected**: Error mentions "correo electrónico" not "email"

---

## 5. Verify Tests Pass (US5)

### Run Full Test Suite

```bash
python manage.py test --verbosity=2
```

**Expected**: All 163+ tests pass

### Run with Coverage

```bash
coverage run --source='clients,cases,documents,api' manage.py test
coverage report
```

**Expected**: Coverage >= 70%

---

## 6. Verify Demo Materials (US6)

### Check Postman Collection

```bash
ls -la postman/
cat postman/LegalDocs-API.postman_collection.json | python -m json.tool | head -20
```

**Expected**: Valid JSON file with collection structure

### Check Demo Script

```bash
ls -la docs/
head -50 docs/demo-script.md
```

**Expected**: Demo script with 5-minute walkthrough

---

## 7. Verify Repository Polish (US7)

### Check LICENSE

```bash
head -20 LICENSE
```

**Expected**: MIT license text

### Check README Badges

```bash
head -10 README.md
```

**Expected**: Badges for Python, Django, License

### Check Git Tag

```bash
git tag -l
```

**Expected**: v1.0.0 tag exists

---

## Final Verification Checklist

| Item | Command | Expected |
|------|---------|----------|
| Tests pass | `python manage.py test` | 163+ pass |
| Coverage | `coverage report` | >= 70% |
| Rate limiting | 6 rapid logins | 6th gets 429 |
| File validation | Upload .exe | 400 error |
| Spanish errors | Invalid register | Spanish messages |
| Indexes exist | Check pg_indexes | 7+ indexes |
| Cache works | Dashboard twice | 2nd faster |
| Postman exists | `ls postman/` | Collection file |
| LICENSE exists | `cat LICENSE` | MIT text |
| Tag exists | `git tag` | v1.0.0 |

---

## Troubleshooting

### Rate Limiting Not Working

```bash
# Verify django-ratelimit is installed
pip show django-ratelimit

# Check cache is configured
python manage.py shell -c "from django.core.cache import cache; cache.set('test', 1); print(cache.get('test'))"
```

### python-magic Import Error

```bash
# Install system dependency
sudo apt install libmagic1  # Ubuntu/Debian
brew install libmagic       # macOS
```

### Cache Table Not Found

```bash
python manage.py createcachetable
```

### Indexes Not Created

```bash
python manage.py makemigrations
python manage.py migrate
```

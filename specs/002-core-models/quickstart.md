# Quickstart Guide: Core Data Models

**Feature**: 002-core-models | **Date**: 2026-01-16

## Prerequisites

- Virtual environment activated: `source venv/bin/activate`
- PostgreSQL database running with `legaldocs_db` created
- `.env` file configured with database credentials
- Initial migrations applied: `python manage.py migrate`

## Testing the Models

### 1. Apply Migrations

After implementing the models, create and apply migrations:

```bash
cd legaldocs

# Create migrations for all apps
python manage.py makemigrations clients cases documents

# Apply migrations
python manage.py migrate
```

### 2. Load Fixtures

Load sample data for testing:

```bash
# Load in correct order (clients → cases → documents)
python manage.py loaddata fixtures/clients.json
python manage.py loaddata fixtures/cases.json
python manage.py loaddata fixtures/documents.json

# Or load all at once
python manage.py loaddata fixtures/clients.json fixtures/cases.json fixtures/documents.json
```

### 3. Verify via Django Shell

```bash
python manage.py shell
```

```python
# Test Client model
from clients.models import Client

# List all clients
Client.objects.all()

# Get active clients
Client.objects.filter(is_active=True)

# Check __str__ method
client = Client.objects.first()
print(client)  # Should show: "María García López (12345678A)"

# Test Case model
from cases.models import Case

# List all cases
Case.objects.all()

# Test custom manager methods
Case.objects.active()  # Non-closed cases
Case.objects.by_status('en_proceso')  # Cases in process

# Verify case number format
case = Case.objects.first()
print(case.case_number)  # Should be: CASE-2026-0001

# Test relationship
print(case.client)  # Should show client name

# Test Document model
from documents.models import Document

# List all documents
Document.objects.all()

# Check document string representation
doc = Document.objects.first()
print(doc)  # Should show: "Contrato: Document Title"

# Test reverse relationship
case = Case.objects.first()
case.documents.all()  # Get all documents for this case

client = Client.objects.first()
client.cases.all()  # Get all cases for this client
```

### 4. Verify via Django Admin

1. Start development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to http://localhost:8000/admin/

3. Log in with superuser credentials (admin/admin123)

4. Verify:
   - [ ] Clients section shows all 5 sample clients
   - [ ] Cases section shows all 10 sample cases
   - [ ] Documents section shows all 15 sample documents
   - [ ] Client list displays: full_name, identification_number, email, is_active
   - [ ] Case list displays: case_number, title, client, case_type, status, priority
   - [ ] Document list displays: title, document_type, case, file_size, is_confidential

### 5. Test Business Rules

#### Test PROTECT on Client Deletion

```python
from clients.models import Client
from django.db.models import ProtectedError

client = Client.objects.first()
try:
    client.delete()
except ProtectedError as e:
    print("SUCCESS: Cannot delete client with cases")
```

#### Test CASCADE on Case Deletion

```python
from cases.models import Case
from documents.models import Document

case = Case.objects.first()
doc_count_before = Document.objects.count()
case_id = case.id

case.delete()

doc_count_after = Document.objects.count()
print(f"Documents reduced from {doc_count_before} to {doc_count_after}")
```

#### Test Auto-Generated Case Number

```python
from cases.models import Case
from clients.models import Client
from datetime import date

client = Client.objects.first()
new_case = Case(
    client=client,
    title="Nuevo Caso de Prueba",
    description="Descripción del caso",
    case_type="civil",
    start_date=date.today()
)
new_case.save()
print(f"Generated case number: {new_case.case_number}")
# Should be: CASE-2026-XXXX (next sequential number)
```

### 6. Verification Checklist

Run these checks to verify implementation:

```bash
# Check migrations are created
ls -la clients/migrations/
ls -la cases/migrations/
ls -la documents/migrations/

# Check no migration errors
python manage.py check

# Verify models are properly registered
python manage.py shell -c "from clients.models import Client; print(Client._meta.verbose_name)"
python manage.py shell -c "from cases.models import Case; print(Case._meta.verbose_name)"
python manage.py shell -c "from documents.models import Document; print(Document._meta.verbose_name)"
```

## Common Issues

### Issue: Import Error on Related Model

**Error**: `django.core.exceptions.ImproperlyConfigured`

**Solution**: Use string references for ForeignKeys to avoid circular imports:
```python
# Correct
client = models.ForeignKey('clients.Client', ...)

# Incorrect (causes import issues)
from clients.models import Client
client = models.ForeignKey(Client, ...)
```

### Issue: Fixture Load Order

**Error**: `IntegrityError: insert or update on table ... violates foreign key constraint`

**Solution**: Load fixtures in dependency order:
1. clients.json (no dependencies)
2. cases.json (depends on clients)
3. documents.json (depends on cases)

### Issue: File Size Not Calculated

**Error**: `file_size` is None or not set

**Solution**: The `file_size` is only calculated when an actual file is provided. For fixtures, you must manually set `file_size` values since fixtures don't include actual files.

## Next Steps

After verifying the models work correctly:

1. Run the Django development server to test Admin interface
2. Create additional test data if needed via Admin
3. Proceed to API implementation (future feature)

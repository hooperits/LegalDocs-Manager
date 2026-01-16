# Implementation Tasks: Core Data Models

**Feature**: 002-core-models | **Date**: 2026-01-16 | **Plan**: [plan.md](./plan.md)

## Task Overview

| Phase | Tasks | Focus |
|-------|-------|-------|
| 1. Setup | 2 | Branch and directory preparation |
| 2. Client Model | 3 | Client entity and admin |
| 3. Case Model | 4 | Case entity, manager, and admin |
| 4. Document Model | 3 | Document entity and admin |
| 5. Fixtures | 4 | Sample data creation |
| 6. Validation | 3 | Testing and verification |

**Total Tasks**: 19

---

## Phase 1: Setup

### Task 1.1: Create fixtures directory
- **File**: `legaldocs/fixtures/` (directory)
- **Action**: Create centralized fixtures directory for sample data
- [X] Create `legaldocs/fixtures/` directory
- [X] Add `__init__.py` if needed for Python package

### Task 1.2: Verify app structure
- **Files**: `legaldocs/clients/`, `legaldocs/cases/`, `legaldocs/documents/`
- **Action**: Confirm apps exist and have proper structure
- [X] Verify clients app has `models.py`, `admin.py`
- [X] Verify cases app has `models.py`, `admin.py`
- [X] Verify documents app has `models.py`, `admin.py`

---

## Phase 2: Client Model

### Task 2.1: Implement Client model
- **File**: `legaldocs/clients/models.py`
- **Action**: Create Client model with all specified fields
- [X] Define Client class with docstring
- [X] Add full_name CharField(200)
- [X] Add identification_number CharField(50) unique=True
- [X] Add email EmailField
- [X] Add phone CharField(20)
- [X] Add address TextField blank=True
- [X] Add created_at DateTimeField auto_now_add=True
- [X] Add updated_at DateTimeField auto_now=True
- [X] Add is_active BooleanField default=True
- [X] Add notes TextField blank=True
- [X] Add Meta class with ordering, verbose_name, verbose_name_plural
- [X] Add __str__ method returning name and ID

### Task 2.2: Register Client in admin
- **File**: `legaldocs/clients/admin.py`
- **Action**: Configure Django Admin for Client model
- [X] Import Client model
- [X] Create ClientAdmin class with @admin.register decorator
- [X] Configure list_display: full_name, identification_number, email, is_active, created_at
- [X] Configure list_filter: is_active, created_at
- [X] Configure search_fields: full_name, identification_number, email

### Task 2.3: Create Client migration
- **Command**: `python manage.py makemigrations clients`
- **Action**: Generate initial migration for clients app
- [X] Run makemigrations for clients app
- [X] Verify migration file created in clients/migrations/
- [X] Apply migration with `python manage.py migrate clients`

---

## Phase 3: Case Model

### Task 3.1: Implement CaseManager
- **File**: `legaldocs/cases/models.py`
- **Action**: Create custom manager for Case filtering
- [X] Define CaseManager class inheriting from models.Manager
- [X] Add docstring explaining purpose
- [X] Implement active() method excluding status='cerrado'
- [X] Implement by_status(status) method filtering by status

### Task 3.2: Implement Case model
- **File**: `legaldocs/cases/models.py`
- **Action**: Create Case model with all specified fields and choices
- [X] Define CASE_TYPE_CHOICES (civil, penal, laboral, mercantil, familia)
- [X] Define STATUS_CHOICES (en_proceso, pendiente_documentos, en_revision, cerrado)
- [X] Define PRIORITY_CHOICES (baja, media, alta, urgente)
- [X] Define Case class with docstring
- [X] Add client ForeignKey to 'clients.Client' with PROTECT, related_name='cases'
- [X] Add case_number CharField(20) unique=True, editable=False
- [X] Add title CharField(200)
- [X] Add description TextField
- [X] Add case_type CharField(20) with choices
- [X] Add status CharField(30) with choices, default='en_proceso'
- [X] Add priority CharField(20) with choices, default='media'
- [X] Add start_date DateField
- [X] Add deadline DateField null=True, blank=True
- [X] Add closed_date DateField null=True, blank=True
- [X] Add assigned_to ForeignKey to 'auth.User' SET_NULL, null=True, blank=True
- [X] Add created_at DateTimeField auto_now_add=True
- [X] Add updated_at DateTimeField auto_now=True
- [X] Assign objects = CaseManager()
- [X] Add Meta class with ordering, verbose_name, verbose_name_plural
- [X] Add __str__ method returning case_number and title

### Task 3.3: Implement Case.generate_case_number
- **File**: `legaldocs/cases/models.py`
- **Action**: Add auto-generation logic for case numbers
- [X] Override save() method to generate case_number if not set
- [X] Implement generate_case_number() classmethod
- [X] Use format CASE-YYYY-NNNN with zero-padded sequential number
- [X] Query for last case number of current year
- [X] Increment and return new number

### Task 3.4: Register Case in admin
- **File**: `legaldocs/cases/admin.py`
- **Action**: Configure Django Admin for Case model
- [X] Import Case model
- [X] Create CaseAdmin class with @admin.register decorator
- [X] Configure list_display: case_number, title, client, case_type, status, priority, start_date
- [X] Configure list_filter: status, case_type, priority, created_at
- [X] Configure search_fields: case_number, title, client__full_name
- [X] Configure readonly_fields: case_number

---

## Phase 4: Document Model

### Task 4.1: Implement Document model
- **File**: `legaldocs/documents/models.py`
- **Action**: Create Document model with all specified fields
- [X] Define DOCUMENT_TYPE_CHOICES (contrato, demanda, poder, sentencia, escritura, otro)
- [X] Define Document class with docstring
- [X] Add case ForeignKey to 'cases.Case' with CASCADE, related_name='documents'
- [X] Add document_type CharField(20) with choices
- [X] Add title CharField(200)
- [X] Add description TextField blank=True
- [X] Add file FileField upload_to='legal_documents/'
- [X] Add file_size IntegerField editable=False
- [X] Add uploaded_by ForeignKey to 'auth.User' SET_NULL, null=True
- [X] Add uploaded_at DateTimeField auto_now_add=True
- [X] Add is_confidential BooleanField default=False
- [X] Add Meta class with ordering, verbose_name, verbose_name_plural
- [X] Add __str__ method returning document type display and title
- [X] Override save() to calculate file_size from file.size

### Task 4.2: Register Document in admin
- **File**: `legaldocs/documents/admin.py`
- **Action**: Configure Django Admin for Document model
- [X] Import Document model
- [X] Create DocumentAdmin class with @admin.register decorator
- [X] Configure list_display: title, document_type, case, file_size, uploaded_at, is_confidential
- [X] Configure list_filter: document_type, is_confidential, uploaded_at
- [X] Configure search_fields: title, case__case_number, case__title
- [X] Configure readonly_fields: file_size

### Task 4.3: Create migrations for cases and documents
- **Commands**: `makemigrations cases documents` + `migrate`
- **Action**: Generate and apply migrations for all new models
- [X] Run makemigrations for cases app
- [X] Run makemigrations for documents app
- [X] Apply all migrations with `python manage.py migrate`
- [X] Verify all migrations applied successfully

---

## Phase 5: Fixtures

### Task 5.1: Create clients fixture
- **File**: `legaldocs/fixtures/clients.json`
- **Action**: Create 5 sample clients with realistic Spanish data
- [X] Create JSON array with 5 client objects
- [X] Include varied Spanish names and ID formats
- [X] Mix of active and inactive clients
- [X] Include addresses in Madrid, Barcelona, Valencia, etc.

### Task 5.2: Create cases fixture
- **File**: `legaldocs/fixtures/cases.json`
- **Action**: Create 10 sample cases linked to clients
- [X] Create JSON array with 10 case objects
- [X] Distribute 2 cases per client (average)
- [X] Include all case_type values
- [X] Include all status values
- [X] Set case_number manually in format CASE-2026-XXXX
- [X] Include realistic Spanish legal case titles

### Task 5.3: Create documents fixture
- **File**: `legaldocs/fixtures/documents.json`
- **Action**: Create 15 sample documents linked to cases
- [X] Create JSON array with 15 document objects
- [X] Distribute ~1-2 documents per case
- [X] Include all document_type values
- [X] Use placeholder file paths (actual files not included)
- [X] Set file_size to realistic values (e.g., 50000-500000 bytes)
- [X] Mix of confidential and non-confidential

### Task 5.4: Test fixture loading
- **Command**: `python manage.py loaddata`
- **Action**: Verify all fixtures load correctly
- [X] Load clients.json
- [X] Load cases.json
- [X] Load documents.json
- [X] Verify record counts: 5 clients, 10 cases, 15 documents
- [X] Verify relationships are correct

---

## Phase 6: Validation

### Task 6.1: Verify model functionality
- **Tool**: Django shell
- **Action**: Test all model methods and relationships
- [X] Test Client.__str__ output
- [X] Test Case.__str__ output
- [X] Test Document.__str__ output
- [X] Test Case.objects.active()
- [X] Test Case.objects.by_status('en_proceso')
- [X] Test client.cases.all() relationship
- [X] Test case.documents.all() relationship

### Task 6.2: Verify business rules
- **Tool**: Django shell
- **Action**: Test deletion protection and cascade behavior
- [X] Attempt to delete client with cases - should raise ProtectedError
- [X] Delete case with documents - should cascade delete documents
- [X] Create new case - should auto-generate case_number

### Task 6.3: Verify admin configuration
- **Tool**: Browser + runserver
- **Action**: Check Django Admin displays correctly
- [X] Start development server
- [X] Log into admin
- [X] Verify Client list display and filters
- [X] Verify Case list display and filters
- [X] Verify Document list display and filters
- [X] Verify readonly fields work (case_number, file_size)

---

## Completion Checklist

After all tasks are complete:

- [X] All models created with specified fields
- [X] All models have __str__, Meta, verbose_name
- [X] CaseManager with active() and by_status()
- [X] Case.generate_case_number() works correctly
- [X] Document auto-calculates file_size
- [X] All models registered in admin
- [X] Migrations created and applied
- [X] Fixtures load successfully (30 total records)
- [X] All relationships work via related_name
- [X] PROTECT/CASCADE behaviors verified

## Git Commit

After completing all tasks:

```bash
git add .
git commit -m "feat(modelos): implementar modelos Client, Case y Document

- Agregar modelo Client con campos de contacto y timestamps
- Agregar modelo Case con generación automática de número
- Agregar modelo Document con cálculo de tamaño de archivo
- Implementar CaseManager con métodos active() y by_status()
- Configurar Django Admin para los tres modelos
- Crear fixtures con datos de ejemplo (5 clientes, 10 casos, 15 documentos)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

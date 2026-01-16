# Technical Research: Core Data Models

**Feature**: 002-core-models | **Date**: 2026-01-16

## Research Summary

This document captures technical decisions and research for implementing the core Django models (Client, Case, Document) for LegalDocs Manager.

## Key Decisions

### 1. Model Relationship Strategy

**Decision**: Use Django's built-in relationship types with explicit `on_delete` behaviors.

| Relationship | on_delete | Rationale |
|--------------|-----------|-----------|
| Case → Client | PROTECT | Prevent orphaned cases; clients can only be deleted when they have no cases |
| Document → Case | CASCADE | Documents are owned by cases; deleting a case removes all its documents |
| Case → User (assigned_to) | SET_NULL | User deletion shouldn't affect case history |
| Document → User (uploaded_by) | SET_NULL | User deletion shouldn't affect document records |

**Alternative Considered**: Using RESTRICT instead of PROTECT for Client deletion.
**Rejected Because**: PROTECT provides clearer error messages and is the Django convention for this use case.

### 2. Auto-Generated Case Numbers

**Decision**: Generate case numbers in `save()` method using format `CASE-YYYY-NNNN`.

**Implementation Approach**:
```python
@classmethod
def generate_case_number(cls):
    year = timezone.now().year
    prefix = f"CASE-{year}-"
    last_case = cls.objects.filter(
        case_number__startswith=prefix
    ).order_by('-case_number').first()
    # Extract and increment number
```

**Concurrency Consideration**: In high-concurrency scenarios, database-level UNIQUE constraint on `case_number` field prevents duplicates. If collision occurs, Django will raise IntegrityError which should be caught and retried.

**Alternative Considered**: Using database sequences or UUID.
**Rejected Because**: The `CASE-YYYY-NNNN` format is human-readable and matches legal industry conventions.

### 3. File Size Calculation

**Decision**: Calculate `file_size` automatically in Document's `save()` method.

```python
def save(self, *args, **kwargs):
    if self.file:
        self.file_size = self.file.size
    super().save(*args, **kwargs)
```

**Note**: The `file.size` attribute is available from Django's `FieldFile` after the file is assigned, even before saving to storage.

### 4. Custom Manager for Cases

**Decision**: Implement `CaseManager` with filtering methods instead of model methods.

**Rationale**:
- `Case.objects.active()` reads naturally and chains with other querysets
- `Case.objects.by_status('en_proceso')` provides consistent API for filtering
- Follows Django convention of fat managers for query logic

### 5. Timestamp Fields

**Decision**: Use Django's auto timestamp fields on all models.

| Field | Behavior |
|-------|----------|
| `created_at` | `auto_now_add=True` - Set once on creation |
| `updated_at` | `auto_now=True` - Updated on every save |

**Note**: For Document model, using `uploaded_at` instead of `created_at` for semantic clarity.

### 6. Choices Implementation

**Decision**: Define choices as class constants using list of tuples.

```python
STATUS_CHOICES = [
    ('en_proceso', 'En Proceso'),
    ('pendiente_documentos', 'Pendiente Documentos'),
    ('en_revision', 'En Revisión'),
    ('cerrado', 'Cerrado'),
]
```

**Alternative Considered**: Using Django 3.0+ TextChoices enum.
**Decision**: Use simple list of tuples for clarity and backwards compatibility. TextChoices can be adopted in future refactoring if needed.

### 7. File Upload Path

**Decision**: Store documents in `legal_documents/` subdirectory under MEDIA_ROOT.

```python
file = models.FileField(upload_to='legal_documents/')
```

**Security Considerations**:
- MEDIA_ROOT is already in .gitignore
- File validation will be added in API layer (future feature)
- Consider adding `upload_to` function for organized subdirectories by case in future

### 8. Verbose Names (Spanish)

**Decision**: All field `verbose_name` attributes in Spanish to match target user base.

This ensures Django Admin and form labels display correctly for Spanish-speaking users.

## Fixtures Strategy

### Data Generation Approach

**Decision**: Create realistic but fictional sample data for Spanish legal context.

| Entity | Count | Naming Convention |
|--------|-------|-------------------|
| Clients | 5 | Spanish names, Spanish ID formats |
| Cases | 10 | 2 cases per client, varied types/statuses |
| Documents | 15 | ~1-2 documents per case |

**Fixture Load Order**: `clients.json` → `cases.json` → `documents.json`

**Note**: Documents fixture will NOT include actual files; `file` field will use placeholder paths. Real file upload testing requires manual testing or test factory.

## Database Considerations

### Indexes

**Implicit Indexes** (created automatically by Django):
- `Client.identification_number` (unique=True)
- `Case.case_number` (unique=True)
- All ForeignKey fields

**Future Consideration**: Add explicit indexes on frequently filtered fields (status, case_type) if performance issues arise.

### Migration Strategy

Each model will be created in its respective app:
1. `clients` app: Client model
2. `cases` app: Case model with CaseManager
3. `documents` app: Document model

**Order matters**: Cases depend on Clients, Documents depend on Cases. Run migrations in correct order.

## Admin Configuration

### Registration Strategy

Register all models with basic admin configuration:

```python
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = [...]
    list_filter = [...]
    search_fields = [...]
```

**List Display Fields**:
- Client: full_name, identification_number, email, is_active, created_at
- Case: case_number, title, client, case_type, status, priority, start_date
- Document: title, document_type, case, file_size, uploaded_at, is_confidential

## References

- [Django Model Field Reference](https://docs.djangoproject.com/en/5.0/ref/models/fields/)
- [Django Managers](https://docs.djangoproject.com/en/5.0/topics/db/managers/)
- [Django Fixtures](https://docs.djangoproject.com/en/5.0/topics/db/fixtures/)

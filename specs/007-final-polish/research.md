# Research: Final Polish

**Feature**: 007-final-polish
**Date**: 2026-01-16

## Research Tasks

### 1. Rate Limiting with Django

**Decision**: Use `django-ratelimit` library

**Rationale**:
- Well-maintained, Django-native solution
- Decorator-based for easy application to views
- Supports multiple backends (cache, database)
- Configurable per-view rate limits
- Clear error responses (HTTP 429)

**Alternatives Considered**:
- DRF's built-in throttling: Good but less flexible for per-endpoint control
- django-axes: Focused on login attempts only, not general rate limiting
- Custom middleware: More work, reinventing the wheel

**Implementation**:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    ...
```

---

### 2. File Type Validation

**Decision**: Use `python-magic` for MIME type detection

**Rationale**:
- Validates actual file content, not just extension
- Prevents bypass by renaming malicious files
- Industry standard (libmagic wrapper)
- Cross-platform support

**Alternatives Considered**:
- Extension-only validation: Easily bypassed, insecure
- `filetype` library: Less comprehensive than python-magic
- PIL/Pillow for images: Only works for images, not documents

**Implementation**:
```python
import magic

def validate_file_type(file):
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)  # Reset file pointer
    if mime not in ALLOWED_MIME_TYPES:
        raise ValidationError(f"Tipo de archivo no permitido: {mime}")
```

**Note**: Requires `libmagic` system library:
- Ubuntu/Debian: `apt install libmagic1`
- macOS: `brew install libmagic`
- Windows: Included in python-magic-bin package

---

### 3. Django Caching Strategy

**Decision**: Use database cache backend for dashboard statistics

**Rationale**:
- No additional infrastructure (Redis not required for POC)
- Persistent across server restarts
- Works with existing PostgreSQL setup
- Easy to switch to Redis later if needed

**Alternatives Considered**:
- LocMem cache: Lost on restart, not shared across workers
- Redis: Overkill for POC, adds infrastructure complexity
- File-based cache: I/O overhead, permission issues

**Implementation**:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# Create cache table
# python manage.py createcachetable
```

**Cache Invalidation Strategy**:
- 5-minute TTL for dashboard stats
- Manual invalidation on Case status changes (optional)

---

### 4. Spanish Error Messages

**Decision**: Custom DRF exception handler with Spanish translations

**Rationale**:
- Centralized error handling
- Consistent response format
- No need for full i18n setup (single language)
- Field name mapping to Spanish labels

**Alternatives Considered**:
- Django's full i18n: Overkill for single-language app
- Per-serializer error messages: Repetitive, hard to maintain
- Third-party translation services: Unnecessary complexity

**Implementation**:
```python
# api/exceptions.py
FIELD_TRANSLATIONS = {
    'username': 'nombre de usuario',
    'email': 'correo electrónico',
    'password': 'contraseña',
    'full_name': 'nombre completo',
    ...
}

ERROR_TRANSLATIONS = {
    'This field is required.': 'Este campo es obligatorio.',
    'This field may not be blank.': 'Este campo no puede estar vacío.',
    ...
}
```

---

### 5. Database Indexes

**Decision**: Add indexes for frequently filtered/sorted fields

**Rationale**:
- Case.client, Case.status, Case.case_type: Used in filters
- Document.case, Document.uploaded_at: Used in filters and ordering
- Small index overhead for significant query improvement

**Implementation**:
```python
class Case(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['client'], name='case_client_idx'),
            models.Index(fields=['status'], name='case_status_idx'),
            models.Index(fields=['case_type'], name='case_type_idx'),
            models.Index(fields=['-created_at'], name='case_created_idx'),
        ]
```

**Note**: Run `python manage.py makemigrations` and `python manage.py migrate` after adding indexes.

---

### 6. Query Optimization

**Decision**: Use `select_related` and `prefetch_related` in ViewSets

**Rationale**:
- Eliminates N+1 query problem
- Significant performance improvement for list views
- Django ORM best practice

**Current Issues Identified**:
- CaseViewSet: Fetching client for each case separately
- DocumentViewSet: Fetching case and uploaded_by separately

**Implementation**:
```python
class CaseViewSet(ModelViewSet):
    def get_queryset(self):
        return Case.objects.select_related('client').all()

class DocumentViewSet(ModelViewSet):
    def get_queryset(self):
        return Document.objects.select_related('case', 'uploaded_by').all()
```

---

### 7. Docstring Style

**Decision**: Google-style docstrings

**Rationale**:
- Clear, readable format
- Well-supported by documentation tools
- Consistent with Django/Python community
- Separates Args, Returns, Raises clearly

**Example**:
```python
def get_active_cases(self, client_id: int) -> QuerySet[Case]:
    """
    Retrieve all active cases for a specific client.

    Args:
        client_id: The primary key of the client.

    Returns:
        QuerySet of Case objects with status 'abierto' or 'en_progreso'.

    Raises:
        Client.DoesNotExist: If client_id is not found.
    """
    return self.filter(client_id=client_id, status__in=['abierto', 'en_progreso'])
```

---

### 8. Postman Collection Structure

**Decision**: Organize by resource with environment variables

**Structure**:
```
LegalDocs API
├── Auth
│   ├── Register
│   ├── Login
│   ├── Logout
│   └── Get Current User
├── Clients
│   ├── List Clients
│   ├── Create Client
│   ├── Get Client
│   ├── Update Client
│   ├── Delete Client
│   └── Get Client Cases
├── Cases
│   ├── List Cases
│   ├── Create Case
│   ├── Get Case
│   ├── Update Case
│   ├── Delete Case
│   ├── Close Case
│   └── Statistics
├── Documents
│   ├── List Documents
│   ├── Upload Document
│   ├── Get Document
│   ├── Update Document
│   └── Delete Document
└── Other
    ├── Dashboard
    └── Search
```

**Environment Variables**:
- `{{base_url}}`: http://localhost:8000/api/v1
- `{{token}}`: Auto-set from login response

---

## Dependencies Summary

| Package | Version | Purpose |
|---------|---------|---------|
| django-ratelimit | >=4.1.0 | Rate limiting for auth endpoints |
| python-magic | >=0.4.27 | File type validation |

**System Requirements**:
- libmagic1 (Ubuntu/Debian) or libmagic (macOS) for python-magic

---

## Risks Identified

1. **python-magic system dependency**: May need documentation for different OS
2. **Cache invalidation**: Dashboard stats may be stale for up to 5 minutes
3. **Rate limiting false positives**: Shared IP (NAT) may affect multiple users

**Mitigations**:
1. Document installation steps for each platform
2. Accept 5-minute staleness as acceptable for POC
3. Use reasonable limits (5/min) and clear error messages

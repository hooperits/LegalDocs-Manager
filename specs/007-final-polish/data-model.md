# Data Model: Final Polish

**Feature**: 007-final-polish
**Date**: 2026-01-16

## Overview

No new models are created in this feature. This document describes index additions and model enhancements for existing models.

---

## Index Additions

### Case Model

**Current State**: No explicit indexes (only implicit PK and FK indexes)

**New Indexes**:

| Index Name | Fields | Purpose |
|------------|--------|---------|
| case_client_idx | client | Filter cases by client |
| case_status_idx | status | Filter cases by status (abierto, cerrado, etc.) |
| case_type_idx | case_type | Filter cases by type (civil, penal, etc.) |
| case_created_idx | -created_at | Order by creation date (descending) |

**Implementation**:
```python
class Case(models.Model):
    # ... existing fields ...

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Caso'
        verbose_name_plural = 'Casos'
        indexes = [
            models.Index(fields=['client'], name='case_client_idx'),
            models.Index(fields=['status'], name='case_status_idx'),
            models.Index(fields=['case_type'], name='case_type_idx'),
            models.Index(fields=['-created_at'], name='case_created_idx'),
        ]
```

---

### Document Model

**Current State**: No explicit indexes (only implicit PK and FK indexes)

**New Indexes**:

| Index Name | Fields | Purpose |
|------------|--------|---------|
| doc_case_idx | case | Filter documents by case |
| doc_uploaded_idx | -uploaded_at | Order by upload date (descending) |
| doc_type_idx | document_type | Filter documents by type |

**Implementation**:
```python
class Document(models.Model):
    # ... existing fields ...

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        indexes = [
            models.Index(fields=['case'], name='doc_case_idx'),
            models.Index(fields=['-uploaded_at'], name='doc_uploaded_idx'),
            models.Index(fields=['document_type'], name='doc_type_idx'),
        ]
```

---

### Client Model

**Current State**: No explicit indexes needed

**Rationale**: Client is typically the starting point for queries, not filtered by other fields frequently. The existing PK index is sufficient.

---

## Migration Plan

After adding indexes to models:

```bash
# Generate migration
python manage.py makemigrations cases documents --name add_performance_indexes

# Review migration
python manage.py showmigrations

# Apply migration
python manage.py migrate
```

**Expected Migration**:
```python
# cases/migrations/XXXX_add_performance_indexes.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='case',
            index=models.Index(fields=['client'], name='case_client_idx'),
        ),
        migrations.AddIndex(
            model_name='case',
            index=models.Index(fields=['status'], name='case_status_idx'),
        ),
        migrations.AddIndex(
            model_name='case',
            index=models.Index(fields=['case_type'], name='case_type_idx'),
        ),
        migrations.AddIndex(
            model_name='case',
            index=models.Index(fields=['-created_at'], name='case_created_idx'),
        ),
    ]
```

---

## Query Optimization

### Before (N+1 Problem)

```python
# CaseViewSet - fetches client separately for each case
cases = Case.objects.all()
for case in cases:
    print(case.client.full_name)  # N additional queries
```

### After (Optimized)

```python
# CaseViewSet - single query with JOIN
cases = Case.objects.select_related('client').all()
for case in cases:
    print(case.client.full_name)  # No additional queries
```

---

## Cache Table

For dashboard caching, a cache table is required:

```bash
python manage.py createcachetable
```

This creates a table named `cache_table` (as configured in settings).

---

## Validation Rules

### File Upload Validation

| Rule | Value | Error Message (Spanish) |
|------|-------|------------------------|
| Max size | 10 MB | El archivo excede el tamaño máximo de 10 MB |
| Allowed types | PDF, DOC, DOCX, TXT, JPG, PNG | Tipo de archivo no permitido |

**MIME Types Allowed**:
- `application/pdf`
- `application/msword`
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- `text/plain`
- `image/jpeg`
- `image/png`

---

## No Schema Changes

This feature does not change:
- Model fields
- Model relationships
- Database constraints
- Foreign key behaviors

Only adds:
- Indexes for query performance
- Cache table for dashboard caching

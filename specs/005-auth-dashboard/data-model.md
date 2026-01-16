# Data Model: Authentication and Dashboard Views

**Feature**: 005-auth-dashboard
**Date**: 2026-01-16

## Overview

This feature does not create new database models. It interacts with existing models:
- **User** (Django's built-in `auth.User`)
- **Token** (DRF's `authtoken.Token`)
- **Client** (from `clients` app)
- **Case** (from `cases` app)
- **Document** (from `documents` app)

## Existing Models Used

### User (django.contrib.auth.models.User)

Django's built-in User model, used for authentication and profile.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| username | CharField(150) | Unique username |
| email | EmailField | Email address |
| password | CharField | Hashed password |
| first_name | CharField(150) | First name |
| last_name | CharField(150) | Last name |
| is_active | BooleanField | Account active status |
| is_staff | BooleanField | Admin access |
| date_joined | DateTimeField | Registration date |

**Relationships**:
- `assigned_cases` → Case (reverse FK via `assigned_to`)

---

### Token (rest_framework.authtoken.models.Token)

DRF's built-in Token model for authentication.

| Field | Type | Description |
|-------|------|-------------|
| key | CharField(40) | Token string (primary key) |
| user | OneToOneField(User) | Token owner |
| created | DateTimeField | Creation timestamp |

**Operations in this feature**:
- `Token.objects.get_or_create(user=user)` - Login
- `Token.objects.filter(user=user).delete()` - Logout

---

### Client (clients.models.Client)

Legal client entity.

| Field | Type | Dashboard/Search Usage |
|-------|------|----------------------|
| id | AutoField | - |
| full_name | CharField(200) | Search field, displayed in results |
| email | EmailField | Search field |
| is_active | BooleanField | Dashboard: active_clients count |
| created_at | DateTimeField | - |

**Dashboard Queries**:
```python
# Total and active counts
Client.objects.aggregate(
    total=Count('id'),
    active=Count('id', filter=Q(is_active=True))
)
```

**Search Queries**:
```python
Client.objects.filter(
    Q(full_name__icontains=query) | Q(email__icontains=query)
)[:10]
```

---

### Case (cases.models.Case)

Legal case entity.

| Field | Type | Dashboard/Search Usage |
|-------|------|----------------------|
| id | AutoField | Returned in results |
| case_number | CharField(20) | Search field, displayed |
| title | CharField(200) | Search field, displayed |
| status | CharField(30) | Dashboard: cases_by_status aggregation |
| case_type | CharField(20) | Dashboard: cases_by_type aggregation |
| deadline | DateField | Dashboard: upcoming_deadlines filter |
| client | ForeignKey(Client) | Dashboard: client_name in recent_cases |
| assigned_to | ForeignKey(User) | Profile: assigned_cases_count |
| created_at | DateTimeField | Dashboard: recent_cases ordering |

**Status Choices** (for dashboard aggregation):
- `en_proceso` - En Proceso
- `pendiente_documentos` - Pendiente Documentos
- `en_revision` - En Revisión
- `cerrado` - Cerrado

**Case Type Choices** (for dashboard aggregation):
- `civil` - Civil
- `penal` - Penal
- `laboral` - Laboral
- `mercantil` - Mercantil
- `familia` - Familia

**Dashboard Queries**:
```python
# Cases by status
Case.objects.values('status').annotate(count=Count('id'))

# Cases by type
Case.objects.values('case_type').annotate(count=Count('id'))

# Recent cases (last 5)
Case.objects.select_related('client').order_by('-created_at')[:5]

# Upcoming deadlines (next 7 days)
Case.objects.select_related('client').filter(
    deadline__lte=today + timedelta(days=7),
    deadline__gte=today
).exclude(status='cerrado')
```

**Search Queries**:
```python
Case.objects.filter(
    Q(title__icontains=query) | Q(case_number__icontains=query)
).select_related('client')[:10]
```

**Profile Queries**:
```python
Case.objects.filter(assigned_to=user).count()
```

---

### Document (documents.models.Document)

Legal document entity.

| Field | Type | Dashboard/Search Usage |
|-------|------|----------------------|
| id | AutoField | Returned in results |
| title | CharField(200) | Search field, displayed |
| document_type | CharField(20) | Dashboard: documents_by_type aggregation |
| case | ForeignKey(Case) | Search: case context |

**Document Type Choices** (for dashboard aggregation):
- `contrato` - Contrato
- `demanda` - Demanda
- `poder` - Poder
- `sentencia` - Sentencia
- `escritura` - Escritura
- `otro` - Otro

**Dashboard Queries**:
```python
# Documents by type
Document.objects.values('document_type').annotate(count=Count('id'))
```

**Search Queries**:
```python
Document.objects.filter(
    Q(title__icontains=query)
).select_related('case')[:10]
```

---

## Query Optimization Notes

### Dashboard View

All dashboard queries are optimized:

1. **Client counts**: Single `aggregate()` call with conditional `Count`
2. **Case aggregations**: Uses `values().annotate()` for GROUP BY at database level
3. **Document aggregations**: Uses `values().annotate()` for GROUP BY at database level
4. **Recent cases**: Uses `select_related('client')` to avoid N+1 for client names
5. **Upcoming deadlines**: Uses `select_related('client')` and database-level date filtering

### Search View

All search queries are optimized:

1. **Result limiting**: `[:10]` applied at query level, not Python level
2. **Related data**: `select_related()` used for FK access (client, case)
3. **Index usage**: Searches use `icontains` which benefits from trigram indexes (if added)

### Profile View

1. **Assigned cases count**: Single `count()` query, not loading all cases

---

## Index Recommendations (Future)

For improved search performance at scale, consider adding:

```python
# In future migration
class Meta:
    indexes = [
        # Client search
        models.Index(fields=['full_name']),
        models.Index(fields=['email']),

        # Case search and dashboard
        models.Index(fields=['title']),
        models.Index(fields=['case_number']),
        models.Index(fields=['status']),
        models.Index(fields=['deadline']),

        # Document search
        models.Index(fields=['title']),
    ]
```

For PostgreSQL full-text search (future enhancement):
```sql
CREATE INDEX client_fullname_gin ON clients_client
USING gin(to_tsvector('spanish', full_name));
```

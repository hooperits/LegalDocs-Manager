# Admin Configuration Model: Django Admin Customization

**Feature**: 003-admin-interface | **Date**: 2026-01-16

## Admin Configuration Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LegalDocs Manager Admin Structure                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            Admin Site                                        │
│  site_header: "LegalDocs Manager"                                           │
│  site_title: "LegalDocs Manager"                                            │
│  index_title: "Panel de Administración"                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│    ClientAdmin      │  │     CaseAdmin       │  │   DocumentAdmin     │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ list_display:       │  │ list_display:       │  │ list_display:       │
│  • full_name        │  │  • case_number      │  │  • title            │
│  • identification   │  │  • title            │  │  • case             │
│  • email            │  │  • client           │  │  • document_type    │
│  • phone            │  │  • case_type        │  │  • uploaded_by      │
│  • is_active        │  │  • colored_status   │  │  • uploaded_at      │
├─────────────────────┤  │  • priority         │  │  • formatted_size   │
│ fieldsets:          │  │  • start_date       │  │  • is_confidential  │
│  • Personal Info    │  │  • assigned_to      │  ├─────────────────────┤
│  • Contact          │  ├─────────────────────┤  │ fieldsets:          │
│  • Status           │  │ fieldsets:          │  │  • Documento        │
├─────────────────────┤  │  • Info Básica      │  │  • Archivo          │
│ actions:            │  │  • Detalles         │  │  • Metadatos        │
│  • activate         │  │  • Fechas           │  ├─────────────────────┤
│  • deactivate       │  │  • Asignación       │  │ methods:            │
└─────────────────────┘  ├─────────────────────┤  │  • formatted_size() │
                         │ inlines:            │  │  • save_model()     │
                         │  • DocumentInline   │  └─────────────────────┘
                         ├─────────────────────┤
                         │ actions:            │
                         │  • mark_as_closed   │
                         ├─────────────────────┤
                         │ methods:            │
                         │  • colored_status() │
                         └─────────────────────┘
```

## ClientAdmin Configuration

| Attribute | Value |
|-----------|-------|
| **list_display** | full_name, identification_number, email, phone, is_active |
| **list_filter** | is_active, created_at |
| **search_fields** | full_name, identification_number, email |
| **readonly_fields** | created_at, updated_at |
| **ordering** | -created_at |

### Fieldsets

| Section | Fields |
|---------|--------|
| Información Personal | full_name, identification_number |
| Contacto | email, phone, address |
| Estado | is_active, notes, created_at, updated_at |

### Actions

| Action | Description | Effect |
|--------|-------------|--------|
| activate_clients | Activar clientes seleccionados | Set is_active=True |
| deactivate_clients | Desactivar clientes seleccionados | Set is_active=False |

## CaseAdmin Configuration

| Attribute | Value |
|-----------|-------|
| **list_display** | case_number, title, client, case_type, colored_status, priority, start_date, assigned_to |
| **list_filter** | status, case_type, priority, start_date |
| **search_fields** | case_number, title, client__full_name |
| **readonly_fields** | case_number, created_at, updated_at |
| **ordering** | -start_date |
| **date_hierarchy** | start_date |

### Fieldsets

| Section | Fields |
|---------|--------|
| Información Básica | case_number, client, title, description |
| Detalles | case_type, status, priority |
| Fechas | start_date, deadline, closed_date, created_at, updated_at |
| Asignación | assigned_to |

### DocumentInline

| Attribute | Value |
|-----------|-------|
| **model** | Document |
| **extra** | 0 |
| **fields** | title, document_type, file, is_confidential, uploaded_at |
| **readonly_fields** | uploaded_at |
| **show_change_link** | True |

### Actions

| Action | Description | Effect |
|--------|-------------|--------|
| mark_as_closed | Marcar como Cerrado | Set status='cerrado', closed_date=today |

### Custom Methods

| Method | Description |
|--------|-------------|
| colored_status() | Returns HTML span with colored background based on status |

### Status Colors

| Status | Color | Hex |
|--------|-------|-----|
| en_proceso | Blue | #3498db |
| pendiente_documentos | Orange | #f39c12 |
| en_revision | Purple | #9b59b6 |
| cerrado | Green | #27ae60 |

## DocumentAdmin Configuration

| Attribute | Value |
|-----------|-------|
| **list_display** | title, case, document_type, uploaded_by, uploaded_at, formatted_file_size, is_confidential |
| **list_filter** | document_type, is_confidential, uploaded_at |
| **search_fields** | title, case__case_number |
| **readonly_fields** | file_size, uploaded_by, uploaded_at |
| **ordering** | -uploaded_at |

### Fieldsets

| Section | Fields | Classes |
|---------|--------|---------|
| Documento | case, title, document_type, description | - |
| Archivo | file, file_size, is_confidential | - |
| Metadatos | uploaded_by, uploaded_at | collapse |

### Custom Methods

| Method | Description |
|--------|-------------|
| formatted_file_size() | Converts bytes to human-readable format (KB, MB, GB) |
| save_model() | Auto-sets uploaded_by to request.user on create |

### File Size Format

| Size Range | Display Format |
|------------|---------------|
| < 1 KB | "123 B" |
| < 1 MB | "245.5 KB" |
| < 1 GB | "1.2 MB" |
| >= 1 GB | "2.5 GB" |

## Admin Site Configuration

```python
# legaldocs/legaldocs/admin.py
from django.contrib import admin

admin.site.site_header = "LegalDocs Manager"
admin.site.site_title = "LegalDocs Manager"
admin.site.index_title = "Panel de Administración"
```

Import in urls.py to ensure it loads:
```python
from . import admin  # Add this import
```

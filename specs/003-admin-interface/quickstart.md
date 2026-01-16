# Quickstart Guide: Django Admin Customization

**Feature**: 003-admin-interface | **Date**: 2026-01-16

## Prerequisites

- Virtual environment activated: `source venv/bin/activate`
- Database running with fixtures loaded
- Superuser account created (admin/admin123)

## Starting the Admin Interface

```bash
cd legaldocs
python manage.py runserver
```

Navigate to: http://localhost:8000/admin/

## Testing Checklist

### 1. Admin Site Branding

- [ ] Header shows "LegalDocs Manager"
- [ ] Browser tab title shows "LegalDocs Manager | Admin"
- [ ] Index page title shows "Panel de Administración"

### 2. ClientAdmin Testing

Navigate to: http://localhost:8000/admin/clients/client/

#### List View
- [ ] Columns displayed: full_name, identification_number, email, phone, is_active
- [ ] Filter sidebar shows: is_active, created_at
- [ ] Search box works for name, ID, and email

#### Bulk Actions
1. Select multiple clients using checkboxes
2. Choose "Activar clientes seleccionados" from action dropdown
3. Click "Go"
- [ ] Success message shows count of activated clients
- [ ] Selected clients now have is_active=True

Repeat for "Desactivar clientes seleccionados":
- [ ] Success message shows count of deactivated clients
- [ ] Selected clients now have is_active=False

#### Form View (Click any client)
- [ ] Fields organized in 3 sections:
  - "Información Personal": full_name, identification_number
  - "Contacto": email, phone, address
  - "Estado": is_active, notes, created_at, updated_at
- [ ] created_at and updated_at are readonly (greyed out)

### 3. CaseAdmin Testing

Navigate to: http://localhost:8000/admin/cases/case/

#### List View
- [ ] Columns displayed: case_number, title, client, case_type, status (colored), priority, start_date, assigned_to
- [ ] Status shows as colored badge:
  - Blue for "En Proceso"
  - Orange for "Pendiente Documentos"
  - Purple for "En Revisión"
  - Green for "Cerrado"
- [ ] Filter sidebar shows: status, case_type, priority, start_date
- [ ] Date hierarchy appears below filters for start_date
- [ ] Cases ordered by start_date descending (newest first)

#### Bulk Action - Mark as Closed
1. Select one or more active cases
2. Choose "Marcar como Cerrado" from action dropdown
3. Click "Go"
- [ ] Success message shows count of closed cases
- [ ] Selected cases now have status="Cerrado" (green badge)
- [ ] closed_date is set to today's date

#### Form View (Click any case)
- [ ] Fields organized in 4 sections:
  - "Información Básica": case_number, client, title, description
  - "Detalles": case_type, status, priority
  - "Fechas": start_date, deadline, closed_date, created_at, updated_at
  - "Asignación": assigned_to
- [ ] case_number is readonly
- [ ] created_at and updated_at are readonly

#### Inline Documents
At bottom of case form:
- [ ] "Documentos" section shows related documents in table format
- [ ] Each document row shows: title, document_type, file, is_confidential, uploaded_at
- [ ] "Change" link available to edit document in new tab
- [ ] Can add new document directly from case form

### 4. DocumentAdmin Testing

Navigate to: http://localhost:8000/admin/documents/document/

#### List View
- [ ] Columns displayed: title, case, document_type, uploaded_by, uploaded_at, file size (formatted), is_confidential
- [ ] File sizes shown as human-readable (e.g., "245.5 KB", "1.2 MB")
- [ ] Filter sidebar shows: document_type, is_confidential, uploaded_at
- [ ] Search works for title and case number

#### Form View (Click any document)
- [ ] Fields organized in 3 sections:
  - "Documento": case, title, document_type, description
  - "Archivo": file, file_size, is_confidential
  - "Metadatos": uploaded_by, uploaded_at (collapsed by default)
- [ ] file_size is readonly and shows bytes
- [ ] uploaded_by is readonly
- [ ] uploaded_at is readonly

#### Auto-Set uploaded_by
1. Click "Add Document" to create new document
2. Fill required fields (case, title, document_type, file)
3. Save
- [ ] uploaded_by automatically set to your admin user
- [ ] uploaded_at automatically set to current timestamp

### 5. Integration Testing

#### Case with Documents
1. Go to Cases list
2. Click a case that has documents
3. Scroll to Documents inline
- [ ] Documents for this case are displayed
- [ ] Can add new document from inline
- [ ] Can remove document from inline

#### Delete Cascade
1. Note a case with documents
2. Delete the case
- [ ] Confirmation shows documents will be deleted too
- [ ] After delete, documents are also removed

## Common Issues

### Issue: Admin site header not showing

**Problem**: Site header still shows "Django administration"

**Solution**: Ensure `legaldocs/legaldocs/admin.py` exists with site configuration, and it's imported in `urls.py`:
```python
# In urls.py
from . import admin  # Add this import
```

### Issue: Colored status not displaying

**Problem**: Status shows plain text instead of colored badge

**Solution**: Verify `colored_status` method uses `format_html()` and is in `list_display`:
```python
list_display = [..., 'colored_status', ...]  # Not 'status'
```

### Issue: uploaded_by not auto-setting

**Problem**: uploaded_by is blank after saving document

**Solution**: Verify `save_model` override only sets on create:
```python
def save_model(self, request, obj, form, change):
    if not change:  # Only on CREATE, not update
        obj.uploaded_by = request.user
    super().save_model(request, obj, form, change)
```

### Issue: DocumentInline not appearing

**Problem**: No documents section in case edit form

**Solution**: Verify inline is properly defined and added:
```python
class DocumentInline(admin.TabularInline):
    model = Document  # Must import Document model
    ...

class CaseAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]
```

## Next Steps

After verifying all admin features work correctly:

1. Test with different user roles (if applicable)
2. Create additional test data through admin
3. Proceed to API implementation (next feature)

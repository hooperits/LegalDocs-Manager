# Feature Specification: Django Admin Customization

**Feature Branch**: `003-admin-interface`
**Created**: 2026-01-16
**Status**: Draft
**Input**: Customize Django Admin for legal workflow with enhanced list displays, filters, fieldsets, inlines, and custom actions

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Client Administration (Priority: P1)

As an admin user, I want an organized client management interface so that I can efficiently view, search, and manage client records.

**Why this priority**: Client management is a core daily task requiring quick access to client information.

**Independent Test**: Can be verified by accessing /admin/clients/client/ and testing all list features, filters, and bulk actions.

**Acceptance Scenarios**:

1. **Given** I am in the client list, **When** I view the list, **Then** I see full_name, identification_number, email, phone, is_active columns
2. **Given** clients exist, **When** I filter by is_active, **Then** only matching clients are shown
3. **Given** I search for "García", **When** results appear, **Then** clients with matching name, ID, or email are shown
4. **Given** I select multiple clients, **When** I choose "Activate clients" action, **Then** all selected clients have is_active=True
5. **Given** I edit a client, **When** I view the form, **Then** fields are organized in Personal Info, Contact, and Status sections

---

### User Story 2 - Case Administration (Priority: P1)

As a lawyer, I want a comprehensive case management interface so that I can view case status at a glance and manage related documents.

**Why this priority**: Cases are the central business entity requiring detailed oversight and quick status identification.

**Independent Test**: Can be verified by accessing /admin/cases/case/ and testing list display, inline documents, and status actions.

**Acceptance Scenarios**:

1. **Given** I am in the case list, **When** I view cases, **Then** I see colored status badges for quick identification
2. **Given** a case exists, **When** I edit it, **Then** I see related documents as inline items
3. **Given** I select multiple active cases, **When** I choose "Mark as Cerrado" action, **Then** all selected cases have status='cerrado' and closed_date set
4. **Given** cases exist, **When** I filter by status and case_type, **Then** only matching cases are shown
5. **Given** I view the case list, **When** I observe ordering, **Then** cases are sorted by start_date descending

---

### User Story 3 - Document Administration (Priority: P1)

As a legal assistant, I want document management that auto-tracks uploads so that I don't have to manually enter upload metadata.

**Why this priority**: Documents require accurate tracking of who uploaded them and when.

**Independent Test**: Can be verified by uploading a document and confirming uploaded_by is auto-set and file_size is human-readable.

**Acceptance Scenarios**:

1. **Given** I upload a document, **When** it saves, **Then** uploaded_by is automatically set to my user account
2. **Given** I view the document list, **When** I see file_size column, **Then** sizes are shown as "245 KB" or "1.2 MB"
3. **Given** I view a document form, **When** I check readonly fields, **Then** file_size, uploaded_by, and uploaded_at cannot be edited
4. **Given** documents exist, **When** I filter by document_type and is_confidential, **Then** only matching documents are shown

---

### User Story 4 - Admin Site Branding (Priority: P2)

As the system owner, I want the admin site branded with "LegalDocs Manager" so that users know they're in the correct application.

**Why this priority**: Branding improves user experience and professionalism.

**Independent Test**: Can be verified by accessing /admin/ and checking page title and header.

**Acceptance Scenarios**:

1. **Given** I access the admin site, **When** I view the header, **Then** it shows "LegalDocs Manager"
2. **Given** I view the browser tab, **When** I check the title, **Then** it shows "LegalDocs Manager | Admin"

---

### Edge Cases

- What happens when deactivating a client with active cases? → Action should proceed (cases remain linked)
- What happens when closing a case with documents? → Documents remain attached to closed case
- What happens when uploaded_by user is deleted? → SET_NULL preserves document record
- What happens with very large files (GB)? → Display as GB with 2 decimal places

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: ClientAdmin MUST display organized list with 5 specified columns
- **FR-002**: ClientAdmin MUST provide bulk activate/deactivate actions
- **FR-003**: ClientAdmin MUST organize form with 3 fieldsets
- **FR-004**: CaseAdmin MUST display colored status badges in list
- **FR-005**: CaseAdmin MUST include DocumentInline for related documents
- **FR-006**: CaseAdmin MUST provide "Mark as Cerrado" bulk action
- **FR-007**: DocumentAdmin MUST auto-set uploaded_by on save
- **FR-008**: DocumentAdmin MUST display human-readable file sizes
- **FR-009**: Admin site MUST have custom header "LegalDocs Manager"
- **FR-010**: All admin classes MUST have appropriate search_fields and list_filter

### Key Entities

- **ClientAdmin**: Enhanced admin for Client model
- **CaseAdmin**: Enhanced admin for Case model with inline documents
- **DocumentAdmin**: Enhanced admin for Document model with auto-fields
- **DocumentInline**: TabularInline for documents within CaseAdmin

## Technical Specification

### ClientAdmin (clients/admin.py)

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Enhanced admin for Client model with fieldsets and bulk actions."""

    list_display = [
        'full_name',
        'identification_number',
        'email',
        'phone',
        'is_active',
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['full_name', 'identification_number', 'email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = [
        ('Información Personal', {
            'fields': ['full_name', 'identification_number']
        }),
        ('Contacto', {
            'fields': ['email', 'phone', 'address']
        }),
        ('Estado', {
            'fields': ['is_active', 'notes', 'created_at', 'updated_at']
        }),
    ]

    actions = ['activate_clients', 'deactivate_clients']

    @admin.action(description="Activar clientes seleccionados")
    def activate_clients(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} cliente(s) activado(s).")

    @admin.action(description="Desactivar clientes seleccionados")
    def deactivate_clients(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} cliente(s) desactivado(s).")
```

### CaseAdmin with DocumentInline (cases/admin.py)

```python
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import Case
from documents.models import Document


class DocumentInline(admin.TabularInline):
    """Inline display of documents within case admin."""
    model = Document
    extra = 0
    fields = ['title', 'document_type', 'file', 'is_confidential', 'uploaded_at']
    readonly_fields = ['uploaded_at']
    show_change_link = True


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Enhanced admin for Case model with status badges and inline documents."""

    list_display = [
        'case_number',
        'title',
        'client',
        'case_type',
        'colored_status',
        'priority',
        'start_date',
        'assigned_to',
    ]
    list_filter = ['status', 'case_type', 'priority', 'start_date']
    search_fields = ['case_number', 'title', 'client__full_name']
    readonly_fields = ['case_number', 'created_at', 'updated_at']
    ordering = ['-start_date']
    date_hierarchy = 'start_date'

    fieldsets = [
        ('Información Básica', {
            'fields': ['case_number', 'client', 'title', 'description']
        }),
        ('Detalles', {
            'fields': ['case_type', 'status', 'priority']
        }),
        ('Fechas', {
            'fields': ['start_date', 'deadline', 'closed_date', 'created_at', 'updated_at']
        }),
        ('Asignación', {
            'fields': ['assigned_to']
        }),
    ]

    inlines = [DocumentInline]
    actions = ['mark_as_closed']

    @admin.display(description="Estado")
    def colored_status(self, obj):
        """Display status with colored badge."""
        colors = {
            'en_proceso': '#3498db',      # Blue
            'pendiente_documentos': '#f39c12',  # Orange
            'en_revision': '#9b59b6',     # Purple
            'cerrado': '#27ae60',         # Green
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description="Marcar como Cerrado")
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(
            status='cerrado',
            closed_date=timezone.now().date()
        )
        self.message_user(request, f"{updated} caso(s) marcado(s) como cerrado.")
```

### DocumentAdmin (documents/admin.py)

```python
from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Enhanced admin for Document model with auto-upload tracking."""

    list_display = [
        'title',
        'case',
        'document_type',
        'uploaded_by',
        'uploaded_at',
        'formatted_file_size',
        'is_confidential',
    ]
    list_filter = ['document_type', 'is_confidential', 'uploaded_at']
    search_fields = ['title', 'case__case_number']
    readonly_fields = ['file_size', 'uploaded_by', 'uploaded_at']
    ordering = ['-uploaded_at']

    fieldsets = [
        ('Documento', {
            'fields': ['case', 'title', 'document_type', 'description']
        }),
        ('Archivo', {
            'fields': ['file', 'file_size', 'is_confidential']
        }),
        ('Metadatos', {
            'fields': ['uploaded_by', 'uploaded_at'],
            'classes': ['collapse']
        }),
    ]

    @admin.display(description="Tamaño")
    def formatted_file_size(self, obj):
        """Display file size in human-readable format."""
        if obj.file_size is None:
            return "-"

        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}" if unit != 'B' else f"{size} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def save_model(self, request, obj, form, change):
        """Auto-set uploaded_by to current user on create."""
        if not change:  # Only on create, not update
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
```

### Admin Site Configuration (legaldocs/admin.py or urls.py)

```python
from django.contrib import admin

# Customize admin site
admin.site.site_header = "LegalDocs Manager"
admin.site.site_title = "LegalDocs Manager"
admin.site.index_title = "Panel de Administración"
```

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: ClientAdmin list shows 5 columns with proper filters and search
- **SC-002**: ClientAdmin bulk actions activate/deactivate work correctly
- **SC-003**: ClientAdmin form shows 3 organized fieldsets
- **SC-004**: CaseAdmin list shows colored status badges
- **SC-005**: CaseAdmin includes DocumentInline with add/edit capability
- **SC-006**: CaseAdmin "Mark as Cerrado" action updates status and closed_date
- **SC-007**: DocumentAdmin auto-sets uploaded_by on new document save
- **SC-008**: DocumentAdmin displays file sizes as "245 KB", "1.2 MB" format
- **SC-009**: Admin header shows "LegalDocs Manager"
- **SC-010**: All search and filter functionality works correctly

## Verification Checklist

- [ ] ClientAdmin with 5 list_display columns
- [ ] ClientAdmin with list_filter and search_fields
- [ ] ClientAdmin with 3 fieldsets (Personal, Contact, Status)
- [ ] ClientAdmin with activate/deactivate actions
- [ ] CaseAdmin with colored_status method
- [ ] CaseAdmin with DocumentInline
- [ ] CaseAdmin with mark_as_closed action
- [ ] CaseAdmin ordering by -start_date
- [ ] DocumentAdmin with formatted_file_size method
- [ ] DocumentAdmin save_model sets uploaded_by
- [ ] DocumentAdmin readonly_fields configured
- [ ] Admin site header customized
- [ ] All admin pages accessible and functional

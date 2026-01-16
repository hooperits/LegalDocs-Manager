# Technical Research: Django Admin Customization

**Feature**: 003-admin-interface | **Date**: 2026-01-16

## Research Summary

This document captures technical decisions for enhancing Django Admin with custom fieldsets, actions, inline editing, and display methods.

## Key Decisions

### 1. Fieldset Organization Strategy

**Decision**: Use Django's `fieldsets` attribute to organize form fields into logical groups.

```python
fieldsets = [
    ('Section Name', {
        'fields': ['field1', 'field2'],
        'classes': ['collapse'],  # Optional: collapsible section
    }),
]
```

**Rationale**: Improves usability by grouping related fields (Personal Info, Contact, Status).

### 2. Colored Status Badges

**Decision**: Use custom `@admin.display` method with `format_html` for colored badges.

```python
@admin.display(description="Estado")
def colored_status(self, obj):
    colors = {'en_proceso': '#3498db', ...}
    return format_html(
        '<span style="background-color: {}; ...">{}</span>',
        colors.get(obj.status, '#95a5a6'),
        obj.get_status_display()
    )
```

**Alternative Considered**: Using CSS classes and external stylesheet.
**Rejected Because**: Inline styles work without additional configuration and are sufficient for POC.

### 3. Inline Document Editing

**Decision**: Use `TabularInline` for documents within CaseAdmin.

```python
class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0  # No empty forms by default
    show_change_link = True  # Link to full document edit
```

**Alternative Considered**: `StackedInline` for vertical layout.
**Rejected Because**: `TabularInline` is more compact and suitable for document lists.

### 4. Bulk Actions Implementation

**Decision**: Use `@admin.action` decorator for custom actions.

```python
@admin.action(description="Activar clientes seleccionados")
def activate_clients(self, request, queryset):
    updated = queryset.update(is_active=True)
    self.message_user(request, f"{updated} cliente(s) activado(s).")
```

**Rationale**: Clean syntax, proper message feedback, follows Django conventions.

### 5. Auto-Setting uploaded_by

**Decision**: Override `save_model()` to set `uploaded_by` from request.user.

```python
def save_model(self, request, obj, form, change):
    if not change:  # Only on create
        obj.uploaded_by = request.user
    super().save_model(request, obj, form, change)
```

**Rationale**: Ensures audit trail without manual user selection. Only set on create, not update.

### 6. Human-Readable File Sizes

**Decision**: Create custom display method with unit conversion.

```python
@admin.display(description="Tamaño")
def formatted_file_size(self, obj):
    size = obj.file_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
```

**Alternative Considered**: Using `django.template.defaultfilters.filesizeformat`.
**Decision**: Custom method gives more control over format and handles edge cases.

### 7. Admin Site Branding

**Decision**: Customize admin.site attributes in project's admin.py or urls.py.

```python
admin.site.site_header = "LegalDocs Manager"
admin.site.site_title = "LegalDocs Manager"
admin.site.index_title = "Panel de Administración"
```

**Location**: Add to `legaldocs/legaldocs/admin.py` (create if needed) and import in urls.py.

### 8. Import Strategy for DocumentInline

**Decision**: Import Document model in cases/admin.py for inline.

```python
from documents.models import Document
```

**Consideration**: This creates a cross-app import at the admin level, which is acceptable per constitution (only model-level circular imports are prohibited).

## Django Admin Best Practices Applied

### List Display Optimization

- Use `list_select_related` for ForeignKey fields to avoid N+1 queries
- Keep list_display columns reasonable (5-8 columns)
- Use `@admin.display` decorator for computed fields

### Search and Filter

- `search_fields` supports `__` lookups for related models
- `list_filter` can use `SimpleListFilter` for custom filtering
- `date_hierarchy` provides quick date navigation

### Readonly Fields

- Timestamp fields should always be readonly
- Auto-generated fields (case_number, file_size) should be readonly
- Use `readonly_fields` attribute, not `editable=False` on model (different purpose)

## Files to Modify

| File | Changes |
|------|---------|
| `clients/admin.py` | Add fieldsets, actions, enhance list_display |
| `cases/admin.py` | Add DocumentInline, colored_status, mark_as_closed action |
| `documents/admin.py` | Add formatted_file_size, override save_model |
| `legaldocs/admin.py` | NEW - site header/title configuration |

## References

- [Django Admin Documentation](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/)
- [Django Admin Actions](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/actions/)
- [Admin Inlines](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#inlinemodeladmin-objects)

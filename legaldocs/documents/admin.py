from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin configuration for Document model."""

    list_display = [
        'title',
        'case',
        'document_type',
        'uploaded_by',
        'uploaded_at',
        'formatted_file_size',
        'is_confidential',
    ]
    list_filter = [
        'document_type',
        'is_confidential',
        'uploaded_at',
    ]
    search_fields = [
        'title',
        'case__case_number',
    ]
    readonly_fields = [
        'file_size',
        'uploaded_by',
        'uploaded_at',
    ]
    ordering = ['-uploaded_at']

    fieldsets = [
        ('Documento', {
            'fields': ['case', 'title', 'document_type', 'description'],
        }),
        ('Archivo', {
            'fields': ['file', 'file_size', 'is_confidential'],
        }),
        ('Metadatos', {
            'fields': ['uploaded_by', 'uploaded_at'],
            'classes': ['collapse'],
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
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def save_model(self, request, obj, form, change):
        """Auto-set uploaded_by to current user on create."""
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

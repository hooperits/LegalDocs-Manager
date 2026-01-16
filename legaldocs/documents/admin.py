from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin configuration for Document model."""

    list_display = [
        'title',
        'document_type',
        'case',
        'file_size',
        'uploaded_at',
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
        'case__title',
    ]
    readonly_fields = [
        'file_size',
        'uploaded_at',
    ]

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from documents.models import Document

from .models import Case


class DocumentInline(admin.TabularInline):
    """Inline document editing within Case admin."""

    model = Document
    extra = 0
    fields = ['title', 'document_type', 'file', 'is_confidential', 'uploaded_at']
    readonly_fields = ['uploaded_at']
    show_change_link = True


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Admin configuration for Case model."""

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
    list_filter = [
        'status',
        'case_type',
        'priority',
        'start_date',
    ]
    search_fields = [
        'case_number',
        'title',
        'client__full_name',
    ]
    readonly_fields = [
        'case_number',
        'created_at',
        'updated_at',
    ]
    ordering = ['-start_date']
    date_hierarchy = 'start_date'

    fieldsets = [
        ('Información Básica', {
            'fields': ['case_number', 'client', 'title', 'description'],
        }),
        ('Detalles', {
            'fields': ['case_type', 'status', 'priority'],
        }),
        ('Fechas', {
            'fields': ['start_date', 'deadline', 'closed_date', 'created_at', 'updated_at'],
        }),
        ('Asignación', {
            'fields': ['assigned_to'],
        }),
    ]

    inlines = [DocumentInline]
    actions = ['mark_as_closed']

    @admin.display(description="Estado")
    def colored_status(self, obj):
        """Display status with colored badge."""
        colors = {
            'en_proceso': '#3498db',
            'pendiente_documentos': '#f39c12',
            'en_revision': '#9b59b6',
            'cerrado': '#27ae60',
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )

    @admin.action(description="Marcar como Cerrado")
    def mark_as_closed(self, request, queryset):
        """Bulk action to mark selected cases as closed."""
        updated = queryset.update(status='cerrado', closed_date=timezone.now().date())
        self.message_user(request, f"{updated} caso(s) marcado(s) como cerrado(s).")

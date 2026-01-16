from django.contrib import admin

from .models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    """Admin configuration for Case model."""

    list_display = [
        'case_number',
        'title',
        'client',
        'case_type',
        'status',
        'priority',
        'start_date',
    ]
    list_filter = [
        'status',
        'case_type',
        'priority',
        'created_at',
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
    date_hierarchy = 'start_date'

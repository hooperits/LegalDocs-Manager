from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin configuration for Client model."""

    list_display = [
        'full_name',
        'identification_number',
        'email',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'created_at',
    ]
    search_fields = [
        'full_name',
        'identification_number',
        'email',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]

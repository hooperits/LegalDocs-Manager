from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin configuration for Client model."""

    list_display = [
        'full_name',
        'identification_number',
        'email',
        'phone',
        'is_active',
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
    ordering = ['-created_at']

    fieldsets = [
        ('Información Personal', {
            'fields': ['full_name', 'identification_number'],
        }),
        ('Contacto', {
            'fields': ['email', 'phone', 'address'],
        }),
        ('Estado', {
            'fields': ['is_active', 'notes', 'created_at', 'updated_at'],
        }),
    ]

    actions = ['activate_clients', 'deactivate_clients']

    @admin.action(description="Activar clientes seleccionados")
    def activate_clients(self, request, queryset):
        """Bulk action to activate selected clients."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} cliente(s) activado(s).")

    @admin.action(description="Desactivar clientes seleccionados")
    def deactivate_clients(self, request, queryset):
        """Bulk action to deactivate selected clients."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} cliente(s) desactivado(s).")

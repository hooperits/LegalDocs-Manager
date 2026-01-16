"""
Serializers for the Client model.

Provides two serializers:
- ClientSerializer: For list views (excludes notes field for performance)
- ClientDetailSerializer: For detail views (includes notes and computed case_count)
"""

from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for Client list view.

    Excludes the 'notes' field to keep list responses lightweight.
    Used for list and create operations.
    """

    class Meta:
        model = Client
        fields = [
            'id',
            'full_name',
            'identification_number',
            'email',
            'phone',
            'address',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class ClientDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Client detail view.

    Includes all fields plus a computed 'case_count' field showing
    the number of cases associated with this client.
    """

    case_count = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id',
            'full_name',
            'identification_number',
            'email',
            'phone',
            'address',
            'is_active',
            'notes',
            'case_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_case_count(self, obj):
        """Return the number of cases associated with this client."""
        return obj.cases.count()

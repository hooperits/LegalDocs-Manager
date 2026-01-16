"""
Serializers for the Case model.

Provides two serializers:
- CaseSerializer: For list views (includes client_name)
- CaseDetailSerializer: For detail views (nested client data and documents list)
"""

from rest_framework import serializers

from clients.models import Client
from clients.serializers import ClientSerializer
from documents.serializers import DocumentSerializer

from .models import Case


class CaseSerializer(serializers.ModelSerializer):
    """
    Serializer for Case list view.

    Includes client_name for display without nested data.
    Used for list and create operations.
    """

    client_name = serializers.CharField(
        source='client.full_name',
        read_only=True
    )

    class Meta:
        model = Case
        fields = [
            'id',
            'case_number',
            'client',
            'client_name',
            'title',
            'description',
            'case_type',
            'status',
            'priority',
            'start_date',
            'deadline',
            'closed_date',
            'assigned_to',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['case_number', 'created_at', 'updated_at']


class CaseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Case detail view with nested data.

    Includes:
    - Nested client object (read-only)
    - client_id for write operations
    - List of related documents
    """

    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source='client',
        write_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = [
            'id',
            'case_number',
            'client',
            'client_id',
            'title',
            'description',
            'case_type',
            'status',
            'priority',
            'start_date',
            'deadline',
            'closed_date',
            'assigned_to',
            'documents',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['case_number', 'created_at', 'updated_at']

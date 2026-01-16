"""
Serializers for the Document model.

Provides DocumentSerializer with case info and uploader username
for comprehensive document data representation in API responses.
"""

from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for Document model.

    Includes computed fields:
    - case_number: The case number from the related case
    - uploaded_by_username: The username of the user who uploaded the document

    Read-only fields: file_size, uploaded_by, uploaded_at
    """

    uploaded_by_username = serializers.CharField(
        source='uploaded_by.username',
        read_only=True
    )
    case_number = serializers.CharField(
        source='case.case_number',
        read_only=True
    )

    class Meta:
        model = Document
        fields = [
            'id',
            'case',
            'case_number',
            'title',
            'document_type',
            'description',
            'file',
            'file_size',
            'is_confidential',
            'uploaded_by',
            'uploaded_by_username',
            'uploaded_at',
        ]
        read_only_fields = ['file_size', 'uploaded_by', 'uploaded_at']

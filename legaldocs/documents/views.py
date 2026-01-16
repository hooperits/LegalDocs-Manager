"""
ViewSets for the Document API.

Provides DocumentViewSet with:
- Full CRUD operations via ModelViewSet
- File upload support via MultiPartParser and FormParser
- Filtering by case, document_type, is_confidential
- Search by title, description
- Ordering by uploaded_at, title
- Owner-based delete permissions via IsOwnerOrReadOnly
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwnerOrReadOnly

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Document CRUD operations with file upload support.

    Provides list, create, retrieve, update, partial_update, and destroy actions.

    Filtering:
        - case: Filter by case ID
        - document_type: Filter by document type
        - is_confidential: Filter by confidentiality status

    Search:
        - Searches across title and description

    Ordering:
        - uploaded_at, title (default: -uploaded_at)

    Permissions:
        - IsOwnerOrReadOnly: Only document owner or staff can delete
        - uploaded_by is automatically set to the current user on create
    """

    queryset = Document.objects.select_related('case', 'uploaded_by')
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['case', 'document_type', 'is_confidential']
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title']
    ordering = ['-uploaded_at']

    def perform_create(self, serializer):
        """
        Auto-set uploaded_by to the current user when creating a document.

        This ensures the document is always associated with the user who
        uploaded it, which is required for the IsOwnerOrReadOnly permission.
        """
        serializer.save(uploaded_by=self.request.user)

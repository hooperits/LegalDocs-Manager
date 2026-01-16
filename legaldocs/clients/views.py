"""
ViewSets for the Client API.

Provides ClientViewSet with:
- Full CRUD operations via ModelViewSet
- Filtering by is_active
- Search by full_name, email, identification_number
- Ordering by full_name, created_at
- Custom action to retrieve a client's cases
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import Client
from .serializers import ClientDetailSerializer, ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Client CRUD operations.

    Provides list, create, retrieve, update, partial_update, and destroy actions.

    Filtering:
        - is_active: Filter by active status (true/false)

    Search:
        - Searches across full_name, email, and identification_number

    Ordering:
        - full_name, created_at (default: -created_at)

    Custom Actions:
        - cases: GET /clients/{id}/cases/ - Returns all cases for the client
    """

    queryset = Client.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['full_name', 'email', 'identification_number']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    @action(detail=True, methods=['get'])
    def cases(self, request, pk=None):
        """
        Get all cases for a specific client.

        Returns a list of cases associated with this client.
        """
        from cases.serializers import CaseSerializer

        client = self.get_object()
        cases = client.cases.all()
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data)

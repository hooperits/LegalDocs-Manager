"""
ViewSets for the Case API.

Provides CaseViewSet with:
- Full CRUD operations via ModelViewSet
- Filtering by status, case_type, priority, client
- Search by case_number, title, client__full_name
- Ordering by start_date, priority, created_at
- Custom actions: close (mark case as closed), statistics (aggregate counts)
"""

from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import Case
from .serializers import CaseDetailSerializer, CaseSerializer


class CaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Case CRUD operations.

    Provides list, create, retrieve, update, partial_update, and destroy actions.

    Filtering:
        - status: Filter by case status
        - case_type: Filter by case type
        - priority: Filter by priority level
        - client: Filter by client ID

    Search:
        - Searches across case_number, title, and client__full_name

    Ordering:
        - start_date, priority, created_at (default: -start_date)

    Custom Actions:
        - close: POST /cases/{id}/close/ - Marks the case as closed
        - statistics: GET /cases/statistics/ - Returns aggregate case statistics
    """

    queryset = Case.objects.select_related('client', 'assigned_to')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'case_type', 'priority', 'client']
    search_fields = ['case_number', 'title', 'client__full_name']
    ordering_fields = ['start_date', 'priority', 'created_at']
    ordering = ['-start_date']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return CaseDetailSerializer
        return CaseSerializer

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """
        Close a case by setting status to 'cerrado' and closed_date to today.

        Returns:
            - 200 OK with updated case data on success
            - 400 Bad Request if case is already closed
        """
        case = self.get_object()

        if case.status == 'cerrado':
            return Response(
                {'error': 'Case already closed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        case.status = 'cerrado'
        case.closed_date = timezone.now().date()
        case.save()

        serializer = self.get_serializer(case)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get aggregate case statistics.

        Returns counts grouped by:
        - by_status: Count of cases per status
        - by_type: Count of cases per case_type
        - by_priority: Count of cases per priority
        - total: Total number of cases
        """
        status_counts = Case.objects.values('status').annotate(count=Count('id'))
        type_counts = Case.objects.values('case_type').annotate(count=Count('id'))
        priority_counts = Case.objects.values('priority').annotate(count=Count('id'))

        return Response({
            'by_status': {item['status']: item['count'] for item in status_counts},
            'by_type': {item['case_type']: item['count'] for item in type_counts},
            'by_priority': {item['priority']: item['count'] for item in priority_counts},
            'total': Case.objects.count(),
        })

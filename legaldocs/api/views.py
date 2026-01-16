"""
API views for authentication, dashboard, search, and profile.

Provides:
- LoginView: Obtain authentication token
- LogoutView: Delete authentication token
- RegisterView: Create new user account
- MeView: Get current user info
- DashboardView: Aggregated statistics
- SearchView: Global search across models
- ProfileView: User profile management
"""

from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileSerializer, RegisterSerializer, UserInfoSerializer


class LoginView(ObtainAuthToken):
    """
    Obtain authentication token.

    POST /api/v1/auth/login/
    Request: {"username": "...", "password": "..."}
    Response: {"token": "...", "user_id": ..., "username": "..."}
    """

    def post(self, request, *args, **kwargs):
        """Authenticate user and return token."""
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


class LogoutView(APIView):
    """
    Delete authentication token (logout).

    POST /api/v1/auth/logout/
    Request: (empty, requires Authorization header)
    Response: {"detail": "Successfully logged out."}
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete the user's token."""
        Token.objects.filter(user=request.user).delete()
        return Response(
            {'detail': 'Successfully logged out.'},
            status=status.HTTP_200_OK
        )


class RegisterView(APIView):
    """
    Register a new user account.

    POST /api/v1/auth/register/
    Request: {"username": "...", "email": "...", "password": "...", "password_confirm": "..."}
    Response: {"token": "...", "user": {...}}
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Create new user and return token."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserInfoSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class MeView(APIView):
    """
    Get current authenticated user info.

    GET /api/v1/auth/me/
    Response: {"id": ..., "username": "...", "email": "...", ...}
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return current user's information."""
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)


class DashboardView(APIView):
    """
    Get dashboard statistics with aggregated data.

    GET /api/v1/dashboard/
    Response: {
        "total_clients": ...,
        "active_clients": ...,
        "cases_by_status": {...},
        "cases_by_type": {...},
        "recent_cases": [...],
        "documents_by_type": {...},
        "upcoming_deadlines": [...]
    }
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return aggregated dashboard statistics."""
        from datetime import timedelta

        from cases.models import Case
        from clients.models import Client
        from documents.models import Document

        today = timezone.now().date()
        seven_days_later = today + timedelta(days=7)

        # Client counts - single aggregate query
        client_stats = Client.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(is_active=True))
        )

        # Cases by status - single query with values()
        cases_by_status = dict(
            Case.objects.values('status')
            .annotate(count=Count('id'))
            .values_list('status', 'count')
        )

        # Cases by type - single query with values()
        cases_by_type = dict(
            Case.objects.values('case_type')
            .annotate(count=Count('id'))
            .values_list('case_type', 'count')
        )

        # Recent cases (last 5) with select_related for client name
        recent_cases_qs = (
            Case.objects.select_related('client')
            .order_by('-created_at')[:5]
        )
        recent_cases = [
            {
                'id': case.id,
                'case_number': case.case_number,
                'title': case.title,
                'status': case.status,
                'client_name': case.client.full_name
            }
            for case in recent_cases_qs
        ]

        # Documents by type - single query with values()
        documents_by_type = dict(
            Document.objects.values('document_type')
            .annotate(count=Count('id'))
            .values_list('document_type', 'count')
        )

        # Upcoming deadlines (next 7 days) with select_related
        upcoming_qs = (
            Case.objects.select_related('client')
            .filter(
                deadline__gte=today,
                deadline__lte=seven_days_later
            )
            .exclude(status='cerrado')
            .order_by('deadline')
        )
        upcoming_deadlines = [
            {
                'id': case.id,
                'case_number': case.case_number,
                'title': case.title,
                'deadline': case.deadline.isoformat(),
                'days_remaining': (case.deadline - today).days,
                'client_name': case.client.full_name
            }
            for case in upcoming_qs
        ]

        return Response({
            'total_clients': client_stats['total'],
            'active_clients': client_stats['active'],
            'cases_by_status': cases_by_status,
            'cases_by_type': cases_by_type,
            'recent_cases': recent_cases,
            'documents_by_type': documents_by_type,
            'upcoming_deadlines': upcoming_deadlines,
        })


class SearchView(APIView):
    """
    Global search across clients, cases, and documents.

    GET /api/v1/search/?q=<query>
    Response: {
        "query": "...",
        "results": {
            "clients": [...],
            "cases": [...],
            "documents": [...]
        },
        "counts": {
            "clients": ...,
            "cases": ...,
            "documents": ...,
            "total": ...
        }
    }
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Search across all models and return unified results."""
        from cases.models import Case
        from clients.models import Client
        from documents.models import Document

        query = request.query_params.get('q', '').strip()

        if not query:
            return Response(
                {'error': "Query parameter 'q' is required and cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Search clients (by full_name, email)
        clients_qs = Client.objects.filter(
            Q(full_name__icontains=query) | Q(email__icontains=query)
        )[:10]
        clients = [
            {
                'id': c.id,
                'type': 'client',
                'full_name': c.full_name,
                'email': c.email
            }
            for c in clients_qs
        ]

        # Search cases (by title, case_number)
        cases_qs = Case.objects.filter(
            Q(title__icontains=query) | Q(case_number__icontains=query)
        ).select_related('client')[:10]
        cases = [
            {
                'id': c.id,
                'type': 'case',
                'case_number': c.case_number,
                'title': c.title
            }
            for c in cases_qs
        ]

        # Search documents (by title)
        documents_qs = Document.objects.filter(
            Q(title__icontains=query)
        ).select_related('case')[:10]
        documents = [
            {
                'id': d.id,
                'type': 'document',
                'title': d.title,
                'document_type': d.document_type
            }
            for d in documents_qs
        ]

        return Response({
            'query': query,
            'results': {
                'clients': clients,
                'cases': cases,
                'documents': documents
            },
            'counts': {
                'clients': len(clients),
                'cases': len(cases),
                'documents': len(documents),
                'total': len(clients) + len(cases) + len(documents)
            }
        })


class ProfileView(APIView):
    """
    User profile management.

    GET /api/v1/profile/
    Response: {"id": ..., "username": "...", "email": "...", "assigned_cases_count": ...}

    PATCH /api/v1/profile/
    Request: {"email": "...", "first_name": "...", "last_name": "..."}
    Response: Updated profile data
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return current user's profile."""
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Update current user's profile (partial update)."""
        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

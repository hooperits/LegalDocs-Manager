# Research: Authentication and Dashboard Views

**Feature**: 005-auth-dashboard
**Date**: 2026-01-16
**Status**: Complete

## Research Topics

### 1. DRF Token Authentication Patterns

**Decision**: Use DRF's built-in `ObtainAuthToken` view as base for login, custom views for logout/register/me.

**Rationale**:
- `ObtainAuthToken` is battle-tested and handles credential validation
- Token model is already configured via `rest_framework.authtoken`
- Custom views needed for logout (token deletion) and registration (user creation + token)
- `/auth/me/` endpoint follows common API patterns for "who am I" functionality

**Alternatives Considered**:
- **django-rest-knox**: Provides token expiration and multiple tokens per user. Rejected for POC - adds complexity, can be added later if needed.
- **JWT (djangorestframework-simplejwt)**: Stateless tokens with expiration. Rejected - requires additional dependency, token invalidation is more complex.
- **Session-only**: Already configured as fallback for browsable API. Not sufficient for API-first design.

**Implementation Pattern**:
```python
# Login: Extend ObtainAuthToken for consistent response format
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk})

# Logout: Delete user's token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)
```

---

### 2. User Registration Best Practices

**Decision**: Create custom registration serializer with password confirmation and validation.

**Rationale**:
- DRF doesn't provide built-in registration - must be custom
- Password confirmation prevents typos
- Username uniqueness validated by Django's User model
- Return token on successful registration for immediate login

**Alternatives Considered**:
- **dj-rest-auth**: Full-featured auth package. Rejected - overkill for POC, adds unnecessary complexity.
- **django-allauth**: Social auth support. Rejected - not needed for legal document system.

**Implementation Pattern**:
```python
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)
```

---

### 3. Dashboard Query Optimization

**Decision**: Use Django ORM's `annotate()`, `values()`, and `Count()` for all aggregations. Use `select_related()` for recent cases.

**Rationale**:
- Single query per aggregation type (status, type, priority, document_type)
- Avoids N+1 queries for recent cases with `select_related('client')`
- Database-level aggregation is more efficient than Python-level
- PostgreSQL handles these aggregations efficiently

**Alternatives Considered**:
- **Raw SQL**: More control but violates constitution's "avoid raw SQL" rule.
- **Caching (Redis)**: Would improve performance but adds infrastructure complexity for POC.
- **Materialized views**: PostgreSQL feature for pre-computed aggregates. Overkill for POC scale.

**Implementation Pattern**:
```python
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

class DashboardView(APIView):
    def get(self, request):
        # Client counts - single query
        client_stats = Client.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(is_active=True))
        )

        # Cases by status - single query with values()
        cases_by_status = dict(
            Case.objects.values('status').annotate(count=Count('id'))
            .values_list('status', 'count')
        )

        # Recent cases with select_related for client name
        recent_cases = Case.objects.select_related('client') \
            .order_by('-created_at')[:5]

        # Upcoming deadlines - filter in database
        seven_days = timezone.now().date() + timedelta(days=7)
        upcoming = Case.objects.select_related('client') \
            .filter(deadline__lte=seven_days, deadline__gte=timezone.now().date()) \
            .exclude(status='cerrado')
```

---

### 4. Global Search Implementation

**Decision**: Use Django's `Q` objects for OR queries across models, limit results per model.

**Rationale**:
- `Q` objects allow combining conditions with OR logic
- `icontains` for case-insensitive partial matching
- Separate queries per model allows different field searches
- Limit to 10 per model prevents overwhelming results

**Alternatives Considered**:
- **PostgreSQL Full-Text Search**: Better relevance ranking. Rejected - requires schema changes, overkill for POC.
- **Elasticsearch**: Advanced search features. Rejected - significant infrastructure overhead.
- **django-haystack**: Abstraction over search backends. Rejected - additional dependency not needed.

**Implementation Pattern**:
```python
from django.db.models import Q

class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'error': 'Query parameter required'}, status=400)

        # Search clients
        clients = Client.objects.filter(
            Q(full_name__icontains=query) | Q(email__icontains=query)
        )[:10]

        # Search cases
        cases = Case.objects.filter(
            Q(title__icontains=query) | Q(case_number__icontains=query)
        ).select_related('client')[:10]

        # Search documents
        documents = Document.objects.filter(
            Q(title__icontains=query)
        ).select_related('case')[:10]
```

---

### 5. User Profile Management

**Decision**: Create a dedicated ProfileView with GET/PATCH, use serializer for field validation.

**Rationale**:
- Separate from `/auth/me/` which is read-only basic info
- PATCH allows partial updates (email, first_name, last_name)
- Username is read-only to prevent identity confusion
- Include `assigned_cases_count` via annotation

**Alternatives Considered**:
- **Using UserViewSet**: Would expose user list and other users. Rejected for security.
- **Combining with /auth/me/**: Would mix concerns. Rejected for clarity.

**Implementation Pattern**:
```python
class ProfileSerializer(serializers.ModelSerializer):
    assigned_cases_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'assigned_cases_count', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']

    def get_assigned_cases_count(self, obj):
        return Case.objects.filter(assigned_to=obj).count()

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

---

### 6. Testing Strategy

**Decision**: Use DRF's `APITestCase` with `APIClient` for all endpoint tests. Organize tests by feature in `api/tests/` directory.

**Rationale**:
- `APITestCase` provides `self.client` pre-configured for API testing
- `force_authenticate()` simplifies authenticated test setup
- Separate test files per feature improves maintainability
- Test both success and error cases for security assurance

**Test Organization**:
```
api/tests/
├── __init__.py
├── test_auth.py       # Login, logout, register, me
├── test_dashboard.py  # Dashboard statistics
├── test_search.py     # Global search
└── test_profile.py    # Profile get/update
```

**Implementation Pattern**:
```python
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_login_success(self):
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/v1/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
```

---

## Summary

All technical decisions align with the constitution's principles:
- **Django Best Practices**: Using built-in DRF features, Django ORM for queries
- **No External Dependencies**: All functionality implemented with existing stack
- **Security**: Token-based auth, permission checks, input validation
- **Performance**: Optimized queries with annotate/select_related
- **Testing**: Comprehensive test coverage using DRF's test utilities

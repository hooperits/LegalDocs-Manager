"""
Tests for CaseViewSet.

Tests CRUD operations, filtering, and custom actions (close, statistics).
"""

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from cases.models import Case
from clients.models import Client


class CaseViewSetTests(APITestCase):
    """Tests for CaseViewSet."""

    def setUp(self):
        """Create test user, client, and cases."""
        self.user = User.objects.create_user(
            username='caseuser',
            email='caseuser@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.client_obj = Client.objects.create(
            full_name='Case Test Client',
            identification_number='CTC001',
            email='ctc@example.com',
            phone='555-0000'
        )

        self.case1 = Case.objects.create(
            client=self.client_obj,
            title='Civil Case',
            description='Civil case description',
            case_type='civil',
            status='en_proceso',
            priority='alta',
            start_date=timezone.now().date()
        )
        self.case2 = Case.objects.create(
            client=self.client_obj,
            title='Penal Case',
            description='Penal case description',
            case_type='penal',
            status='cerrado',
            priority='baja',
            start_date=timezone.now().date()
        )

    def test_list_cases(self):
        """Test listing all cases."""
        response = self.client.get('/api/v1/cases/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_create_case(self):
        """Test creating a new case."""
        data = {
            'client': self.client_obj.id,
            'title': 'New Case',
            'description': 'New case description',
            'case_type': 'laboral',
            'start_date': timezone.now().date().isoformat()
        }
        response = self.client.post('/api/v1/cases/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Case')
        self.assertIn('case_number', response.data)

    def test_retrieve_case(self):
        """Test retrieving a single case."""
        response = self.client.get(f'/api/v1/cases/{self.case1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Civil Case')
        # Detail view should include nested client and documents
        self.assertIn('client', response.data)
        self.assertIn('documents', response.data)

    def test_update_case(self):
        """Test updating a case with PUT."""
        data = {
            'client': self.client_obj.id,
            'title': 'Updated Civil Case',
            'description': 'Updated description',
            'case_type': 'civil',
            'status': 'en_revision',
            'start_date': timezone.now().date().isoformat()
        }
        response = self.client.put(f'/api/v1/cases/{self.case1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Civil Case')
        self.assertEqual(response.data['status'], 'en_revision')

    def test_partial_update_case(self):
        """Test partially updating a case with PATCH."""
        data = {'priority': 'urgente'}
        response = self.client.patch(f'/api/v1/cases/{self.case1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority'], 'urgente')

    def test_delete_case(self):
        """Test deleting a case."""
        response = self.client.delete(f'/api/v1/cases/{self.case2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Case.objects.filter(id=self.case2.id).exists())

    def test_filter_by_status(self):
        """Test filtering cases by status."""
        response = self.client.get('/api/v1/cases/?status=en_proceso')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Civil Case')

    def test_filter_by_case_type(self):
        """Test filtering cases by case_type."""
        response = self.client.get('/api/v1/cases/?case_type=penal')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Penal Case')

    def test_filter_by_priority(self):
        """Test filtering cases by priority."""
        response = self.client.get('/api/v1/cases/?priority=alta')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_client(self):
        """Test filtering cases by client ID."""
        response = self.client.get(f'/api/v1/cases/?client={self.client_obj.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_search_by_title(self):
        """Test searching cases by title."""
        response = self.client.get('/api/v1/cases/?search=Civil')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_by_case_number(self):
        """Test searching cases by case_number."""
        response = self.client.get(f'/api/v1/cases/?search={self.case1.case_number}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_close_case_action(self):
        """Test the close custom action."""
        response = self.client.post(f'/api/v1/cases/{self.case1.id}/close/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'cerrado')
        self.assertIsNotNone(response.data['closed_date'])

    def test_close_already_closed_case(self):
        """Test closing an already closed case returns 400."""
        response = self.client.post(f'/api/v1/cases/{self.case2.id}/close/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_statistics_action(self):
        """Test the statistics custom action."""
        response = self.client.get('/api/v1/cases/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('by_status', response.data)
        self.assertIn('by_type', response.data)
        self.assertIn('by_priority', response.data)
        self.assertIn('total', response.data)
        self.assertEqual(response.data['total'], 2)


class CaseViewSetUnauthenticatedTests(APITestCase):
    """Tests for unauthenticated access to CaseViewSet."""

    def test_list_cases_unauthenticated(self):
        """Test that unauthenticated users cannot list cases."""
        response = self.client.get('/api/v1/cases/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_case_unauthenticated(self):
        """Test that unauthenticated users cannot create cases."""
        client_obj = Client.objects.create(
            full_name='Unauth Client',
            identification_number='UC001',
            email='uc@example.com',
            phone='555-0000'
        )
        data = {
            'client': client_obj.id,
            'title': 'Unauthorized Case',
            'description': 'Test',
            'case_type': 'civil',
            'start_date': timezone.now().date().isoformat()
        }
        response = self.client.post('/api/v1/cases/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_statistics_unauthenticated(self):
        """Test that unauthenticated users cannot access statistics."""
        response = self.client.get('/api/v1/cases/statistics/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

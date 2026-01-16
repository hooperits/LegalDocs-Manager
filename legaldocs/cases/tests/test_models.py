"""
Tests for Case model.

Tests case creation, auto-generated case numbers, and custom manager methods.
"""

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from cases.models import Case
from clients.models import Client


class CaseModelTests(TestCase):
    """Tests for the Case model."""

    def setUp(self):
        """Create test client for case relationships."""
        self.client_obj = Client.objects.create(
            full_name='Test Client',
            identification_number='CLIENT001',
            email='client@example.com',
            phone='555-0000'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def test_create_case_with_valid_data(self):
        """Test creating a case with all valid data."""
        case = Case.objects.create(
            client=self.client_obj,
            title='Test Case Title',
            description='Test case description',
            case_type='civil',
            status='en_proceso',
            priority='media',
            start_date=timezone.now().date(),
            assigned_to=self.user
        )
        self.assertEqual(case.title, 'Test Case Title')
        self.assertEqual(case.case_type, 'civil')
        self.assertEqual(case.status, 'en_proceso')
        self.assertIsNotNone(case.case_number)

    def test_case_number_auto_generated(self):
        """Test that case_number is auto-generated on save."""
        case = Case.objects.create(
            client=self.client_obj,
            title='Auto Number Test',
            description='Testing auto case number',
            case_type='penal',
            start_date=timezone.now().date()
        )
        year = timezone.now().year
        self.assertTrue(case.case_number.startswith(f'CASE-{year}-'))
        self.assertEqual(len(case.case_number), 14)  # CASE-YYYY-NNNN

    def test_case_number_increments_correctly(self):
        """Test that case numbers increment sequentially."""
        case1 = Case.objects.create(
            client=self.client_obj,
            title='Case 1',
            description='First case',
            case_type='civil',
            start_date=timezone.now().date()
        )
        case2 = Case.objects.create(
            client=self.client_obj,
            title='Case 2',
            description='Second case',
            case_type='civil',
            start_date=timezone.now().date()
        )
        # Extract sequence numbers
        seq1 = int(case1.case_number.split('-')[-1])
        seq2 = int(case2.case_number.split('-')[-1])
        self.assertEqual(seq2, seq1 + 1)

    def test_case_number_unique(self):
        """Test that case numbers are unique."""
        case1 = Case.objects.create(
            client=self.client_obj,
            title='Unique Test 1',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )
        case2 = Case.objects.create(
            client=self.client_obj,
            title='Unique Test 2',
            description='Test',
            case_type='civil',
            start_date=timezone.now().date()
        )
        self.assertNotEqual(case1.case_number, case2.case_number)

    def test_case_str_method(self):
        """Test the __str__ method returns expected format."""
        case = Case.objects.create(
            client=self.client_obj,
            title='String Test Case',
            description='Test',
            case_type='laboral',
            start_date=timezone.now().date()
        )
        expected = f'{case.case_number} - String Test Case'
        self.assertEqual(str(case), expected)

    def test_case_default_status_en_proceso(self):
        """Test that default status is 'en_proceso'."""
        case = Case.objects.create(
            client=self.client_obj,
            title='Default Status Test',
            description='Test',
            case_type='mercantil',
            start_date=timezone.now().date()
        )
        self.assertEqual(case.status, 'en_proceso')

    def test_case_default_priority_media(self):
        """Test that default priority is 'media'."""
        case = Case.objects.create(
            client=self.client_obj,
            title='Default Priority Test',
            description='Test',
            case_type='familia',
            start_date=timezone.now().date()
        )
        self.assertEqual(case.priority, 'media')

    def test_case_with_deadline(self):
        """Test creating a case with a deadline."""
        today = timezone.now().date()
        deadline = today + timezone.timedelta(days=30)
        case = Case.objects.create(
            client=self.client_obj,
            title='Deadline Test',
            description='Test',
            case_type='civil',
            start_date=today,
            deadline=deadline
        )
        self.assertEqual(case.deadline, deadline)

    def test_case_with_closed_date(self):
        """Test creating a closed case."""
        today = timezone.now().date()
        case = Case.objects.create(
            client=self.client_obj,
            title='Closed Case Test',
            description='Test',
            case_type='civil',
            status='cerrado',
            start_date=today,
            closed_date=today
        )
        self.assertEqual(case.status, 'cerrado')
        self.assertEqual(case.closed_date, today)


class CaseManagerTests(TestCase):
    """Tests for the CaseManager custom manager."""

    def setUp(self):
        """Create test client and cases with different statuses."""
        self.client_obj = Client.objects.create(
            full_name='Manager Test Client',
            identification_number='MANAGER001',
            email='manager@example.com',
            phone='555-9999'
        )
        today = timezone.now().date()

        # Create cases with different statuses
        self.case_en_proceso = Case.objects.create(
            client=self.client_obj,
            title='En Proceso',
            description='Test',
            case_type='civil',
            status='en_proceso',
            start_date=today
        )
        self.case_pendiente = Case.objects.create(
            client=self.client_obj,
            title='Pendiente',
            description='Test',
            case_type='civil',
            status='pendiente_documentos',
            start_date=today
        )
        self.case_revision = Case.objects.create(
            client=self.client_obj,
            title='En Revision',
            description='Test',
            case_type='civil',
            status='en_revision',
            start_date=today
        )
        self.case_cerrado = Case.objects.create(
            client=self.client_obj,
            title='Cerrado',
            description='Test',
            case_type='civil',
            status='cerrado',
            start_date=today
        )

    def test_manager_active_excludes_closed_cases(self):
        """Test that active() excludes cases with status 'cerrado'."""
        active_cases = Case.objects.active()
        self.assertEqual(active_cases.count(), 3)
        self.assertNotIn(self.case_cerrado, active_cases)
        self.assertIn(self.case_en_proceso, active_cases)
        self.assertIn(self.case_pendiente, active_cases)
        self.assertIn(self.case_revision, active_cases)

    def test_manager_by_status_filters_correctly(self):
        """Test that by_status() filters by the given status."""
        en_proceso = Case.objects.by_status('en_proceso')
        self.assertEqual(en_proceso.count(), 1)
        self.assertIn(self.case_en_proceso, en_proceso)

        cerrado = Case.objects.by_status('cerrado')
        self.assertEqual(cerrado.count(), 1)
        self.assertIn(self.case_cerrado, cerrado)

    def test_manager_by_status_empty_result(self):
        """Test by_status() returns empty queryset for unused status."""
        # All our test cases use 'civil' type, not testing status here
        # but ensuring the query works with no matches
        result = Case.objects.by_status('nonexistent_status')
        self.assertEqual(result.count(), 0)

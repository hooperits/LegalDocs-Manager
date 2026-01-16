"""
Tests for Client serializers.

Tests ClientSerializer and ClientDetailSerializer with valid and invalid data.
"""

from django.test import TestCase

from clients.models import Client
from clients.serializers import ClientDetailSerializer, ClientSerializer


class ClientSerializerTests(TestCase):
    """Tests for ClientSerializer."""

    def test_serialize_client(self):
        """Test serializing a client instance."""
        client = Client.objects.create(
            full_name='Serialize Test',
            identification_number='SER001',
            email='serialize@example.com',
            phone='555-0001',
            address='Test Address'
        )
        serializer = ClientSerializer(client)
        data = serializer.data

        self.assertEqual(data['full_name'], 'Serialize Test')
        self.assertEqual(data['identification_number'], 'SER001')
        self.assertEqual(data['email'], 'serialize@example.com')
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        # Notes should not be in list serializer
        self.assertNotIn('notes', data)

    def test_deserialize_valid_data(self):
        """Test deserializing valid client data."""
        data = {
            'full_name': 'New Client',
            'identification_number': 'NEW001',
            'email': 'new@example.com',
            'phone': '555-0002',
            'address': 'New Address',
            'is_active': True
        }
        serializer = ClientSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        client = serializer.save()
        self.assertEqual(client.full_name, 'New Client')

    def test_deserialize_invalid_email(self):
        """Test that invalid email format is rejected."""
        data = {
            'full_name': 'Invalid Email',
            'identification_number': 'INV001',
            'email': 'not-an-email',
            'phone': '555-0003'
        }
        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_deserialize_missing_required_fields(self):
        """Test that missing required fields cause validation errors."""
        data = {
            'full_name': 'Missing Fields'
            # Missing identification_number, email, phone
        }
        serializer = ClientSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('identification_number', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('phone', serializer.errors)

    def test_created_at_read_only(self):
        """Test that created_at is read-only."""
        data = {
            'full_name': 'Read Only Test',
            'identification_number': 'RO001',
            'email': 'readonly@example.com',
            'phone': '555-0004',
            'created_at': '2020-01-01T00:00:00Z'
        }
        serializer = ClientSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        client = serializer.save()
        # created_at should be auto-set, not the provided value
        self.assertNotEqual(str(client.created_at), '2020-01-01T00:00:00Z')


class ClientDetailSerializerTests(TestCase):
    """Tests for ClientDetailSerializer."""

    def test_serialize_includes_notes(self):
        """Test that detail serializer includes notes field."""
        client = Client.objects.create(
            full_name='Detail Test',
            identification_number='DET001',
            email='detail@example.com',
            phone='555-0005',
            notes='Important notes here'
        )
        serializer = ClientDetailSerializer(client)
        data = serializer.data

        self.assertIn('notes', data)
        self.assertEqual(data['notes'], 'Important notes here')

    def test_serialize_includes_case_count(self):
        """Test that detail serializer includes case_count."""
        from cases.models import Case
        from django.utils import timezone

        client = Client.objects.create(
            full_name='Case Count Test',
            identification_number='CC001',
            email='casecount@example.com',
            phone='555-0006'
        )
        # Create some cases
        for i in range(3):
            Case.objects.create(
                client=client,
                title=f'Case {i}',
                description='Test',
                case_type='civil',
                start_date=timezone.now().date()
            )

        serializer = ClientDetailSerializer(client)
        data = serializer.data

        self.assertIn('case_count', data)
        self.assertEqual(data['case_count'], 3)

    def test_serialize_case_count_zero_for_new_client(self):
        """Test that case_count is 0 for client with no cases."""
        client = Client.objects.create(
            full_name='No Cases',
            identification_number='NC001',
            email='nocases@example.com',
            phone='555-0007'
        )
        serializer = ClientDetailSerializer(client)
        data = serializer.data

        self.assertEqual(data['case_count'], 0)

    def test_deserialize_valid_data_with_notes(self):
        """Test deserializing data with notes field."""
        data = {
            'full_name': 'With Notes',
            'identification_number': 'WN001',
            'email': 'withnotes@example.com',
            'phone': '555-0008',
            'notes': 'Test notes'
        }
        serializer = ClientDetailSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        client = serializer.save()
        self.assertEqual(client.notes, 'Test notes')

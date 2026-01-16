"""
Tests for Client model.

Tests client creation, validation, and model methods.
"""

from django.db import IntegrityError
from django.test import TestCase

from clients.models import Client


class ClientModelTests(TestCase):
    """Tests for the Client model."""

    def test_create_client_with_valid_data(self):
        """Test creating a client with all valid data."""
        client = Client.objects.create(
            full_name='Juan García López',
            identification_number='12345678-A',
            email='juan.garcia@example.com',
            phone='555-1234',
            address='Calle Principal 123, Ciudad',
            is_active=True,
            notes='Cliente importante'
        )
        self.assertEqual(client.full_name, 'Juan García López')
        self.assertEqual(client.identification_number, '12345678-A')
        self.assertEqual(client.email, 'juan.garcia@example.com')
        self.assertTrue(client.is_active)
        self.assertIsNotNone(client.created_at)
        self.assertIsNotNone(client.updated_at)

    def test_create_client_with_minimum_required_fields(self):
        """Test creating a client with only required fields."""
        client = Client.objects.create(
            full_name='María López',
            identification_number='87654321-B',
            email='maria@example.com',
            phone='555-5678'
        )
        self.assertEqual(client.full_name, 'María López')
        self.assertEqual(client.address, '')
        self.assertEqual(client.notes, '')
        self.assertTrue(client.is_active)  # Default value

    def test_create_client_duplicate_identification_number_fails(self):
        """Test that duplicate identification numbers raise an error."""
        Client.objects.create(
            full_name='First Client',
            identification_number='UNIQUE123',
            email='first@example.com',
            phone='555-0001'
        )
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                full_name='Second Client',
                identification_number='UNIQUE123',
                email='second@example.com',
                phone='555-0002'
            )

    def test_client_str_method(self):
        """Test the __str__ method returns expected format."""
        client = Client.objects.create(
            full_name='Test Client',
            identification_number='TEST001',
            email='test@example.com',
            phone='555-0000'
        )
        self.assertEqual(str(client), 'Test Client (TEST001)')

    def test_client_default_is_active_true(self):
        """Test that is_active defaults to True."""
        client = Client.objects.create(
            full_name='New Client',
            identification_number='NEW001',
            email='new@example.com',
            phone='555-1111'
        )
        self.assertTrue(client.is_active)

    def test_client_ordering_by_created_at_descending(self):
        """Test that clients are ordered by created_at descending."""
        client1 = Client.objects.create(
            full_name='First',
            identification_number='FIRST001',
            email='first@example.com',
            phone='555-1111'
        )
        client2 = Client.objects.create(
            full_name='Second',
            identification_number='SECOND001',
            email='second@example.com',
            phone='555-2222'
        )
        clients = list(Client.objects.all())
        # Most recent first
        self.assertEqual(clients[0], client2)
        self.assertEqual(clients[1], client1)

    def test_client_updated_at_changes_on_save(self):
        """Test that updated_at changes when the client is modified."""
        client = Client.objects.create(
            full_name='Update Test',
            identification_number='UPDATE001',
            email='update@example.com',
            phone='555-3333'
        )
        original_updated_at = client.updated_at
        client.full_name = 'Updated Name'
        client.save()
        client.refresh_from_db()
        self.assertGreaterEqual(client.updated_at, original_updated_at)

    def test_client_blank_optional_fields(self):
        """Test that optional fields can be blank."""
        client = Client.objects.create(
            full_name='Blank Fields',
            identification_number='BLANK001',
            email='blank@example.com',
            phone='555-4444',
            address='',
            notes=''
        )
        self.assertEqual(client.address, '')
        self.assertEqual(client.notes, '')

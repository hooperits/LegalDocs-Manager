/**
 * Clients API E2E Tests
 *
 * Tests for:
 * - CRUD operations on clients
 * - Filtering and searching
 * - Pagination
 * - Client cases endpoint
 * - Validation
 */

import { test, expect, API_BASE, generateTestClient } from '../fixtures/auth';

test.describe('Clients API', () => {
  test.describe('List Clients', () => {
    test('should list clients with pagination', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/clients/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      // DRF returns paginated response or array depending on pagination settings
      expect(Array.isArray(body) || body.results !== undefined).toBeTruthy();
    });

    test('should filter clients by is_active', async ({ auth }) => {
      await auth.register();

      // Create an active client
      const activeClient = generateTestClient();
      activeClient.is_active = true;
      await auth.post(`${API_BASE}/clients/`, activeClient);

      // Create an inactive client
      const inactiveClient = generateTestClient();
      inactiveClient.is_active = false;
      await auth.post(`${API_BASE}/clients/`, inactiveClient);

      // Filter by active
      const activeResponse = await auth.get(`${API_BASE}/clients/?is_active=true`);
      expect(activeResponse.status()).toBe(200);
      const activeBody = await activeResponse.json();
      const activeResults = Array.isArray(activeBody) ? activeBody : activeBody.results;
      activeResults.forEach((client: any) => {
        expect(client.is_active).toBe(true);
      });

      // Filter by inactive
      const inactiveResponse = await auth.get(`${API_BASE}/clients/?is_active=false`);
      expect(inactiveResponse.status()).toBe(200);
      const inactiveBody = await inactiveResponse.json();
      const inactiveResults = Array.isArray(inactiveBody) ? inactiveBody : inactiveBody.results;
      inactiveResults.forEach((client: any) => {
        expect(client.is_active).toBe(false);
      });
    });

    test('should search clients by full_name', async ({ auth }) => {
      await auth.register();

      // Create a client with a unique name
      const uniqueName = `Unique Client Name ${Date.now()}`;
      const clientData = generateTestClient();
      clientData.full_name = uniqueName;
      await auth.post(`${API_BASE}/clients/`, clientData);

      // Search by name
      const response = await auth.get(`${API_BASE}/clients/?search=${encodeURIComponent(uniqueName)}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      expect(results.length).toBeGreaterThan(0);
      expect(results[0].full_name).toBe(uniqueName);
    });

    test('should search clients by email', async ({ auth }) => {
      await auth.register();

      // Create a client with a unique email
      const uniqueEmail = `unique_email_${Date.now()}@test.com`;
      const clientData = generateTestClient();
      clientData.email = uniqueEmail;
      await auth.post(`${API_BASE}/clients/`, clientData);

      // Search by email
      const response = await auth.get(`${API_BASE}/clients/?search=${encodeURIComponent(uniqueEmail)}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      expect(results.length).toBeGreaterThan(0);
      expect(results[0].email).toBe(uniqueEmail);
    });
  });

  test.describe('Create Client', () => {
    test('should create a new client successfully', async ({ auth }) => {
      await auth.register();
      const clientData = generateTestClient();

      const response = await auth.post(`${API_BASE}/clients/`, clientData);
      expect(response.status()).toBe(201);

      const body = await response.json();
      expect(body.id).toBeDefined();
      expect(body.full_name).toBe(clientData.full_name);
      expect(body.identification_number).toBe(clientData.identification_number);
      expect(body.email).toBe(clientData.email);
      expect(body.phone).toBe(clientData.phone);
      expect(body.is_active).toBe(clientData.is_active);
    });

    test('should reject duplicate identification_number', async ({ auth }) => {
      await auth.register();

      // Use a fixed unique identification number for this test
      const sharedId = `DUPLICATE-TEST-${Date.now()}`;

      // Create first client with explicit identification_number
      const clientData = generateTestClient();
      clientData.identification_number = sharedId;
      const firstResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      expect(firstResponse.status()).toBe(201);

      // Try to create another client with same identification_number
      const duplicateClient = generateTestClient();
      duplicateClient.identification_number = sharedId;

      const response = await auth.post(`${API_BASE}/clients/`, duplicateClient);
      expect(response.status()).toBe(400);

      const body = await response.json();
      // Error should contain identification_number (Spanish or English key)
      const bodyStr = JSON.stringify(body);
      expect(bodyStr).toMatch(/identification_number|número de identificación/i);
    });

    test('should reject client with missing required fields', async ({ auth }) => {
      await auth.register();

      const response = await auth.post(`${API_BASE}/clients/`, {
        full_name: 'Test Name',
        // Missing required fields
      });

      expect(response.status()).toBe(400);
    });
  });

  test.describe('Retrieve Client', () => {
    test('should get client by ID', async ({ auth }) => {
      await auth.register();

      // Create a client
      const clientData = generateTestClient();
      const createResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const createdClient = await createResponse.json();

      // Retrieve the client
      const response = await auth.get(`${API_BASE}/clients/${createdClient.id}/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.id).toBe(createdClient.id);
      expect(body.full_name).toBe(clientData.full_name);
    });

    test('should return 404 for non-existent client', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/clients/99999/`);
      expect(response.status()).toBe(404);
    });
  });

  test.describe('Update Client', () => {
    test('should update client with PUT', async ({ auth }) => {
      await auth.register();

      // Create a client
      const clientData = generateTestClient();
      const createResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const createdClient = await createResponse.json();

      // Update the client
      const updatedData = {
        ...clientData,
        full_name: 'Updated Name',
        email: 'updated@test.com',
      };

      const response = await auth.put(`${API_BASE}/clients/${createdClient.id}/`, updatedData);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.full_name).toBe('Updated Name');
      expect(body.email).toBe('updated@test.com');
    });

    test('should partially update client with PATCH', async ({ auth }) => {
      await auth.register();

      // Create a client
      const clientData = generateTestClient();
      const createResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const createdClient = await createResponse.json();

      // Partially update the client
      const response = await auth.patch(`${API_BASE}/clients/${createdClient.id}/`, {
        full_name: 'Patched Name',
      });
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.full_name).toBe('Patched Name');
      expect(body.email).toBe(clientData.email); // Unchanged
    });
  });

  test.describe('Delete Client', () => {
    test('should delete client successfully', async ({ auth }) => {
      await auth.register();

      // Create a client
      const clientData = generateTestClient();
      const createResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const createdClient = await createResponse.json();

      // Delete the client
      const deleteResponse = await auth.delete(`${API_BASE}/clients/${createdClient.id}/`);
      expect(deleteResponse.status()).toBe(204);

      // Verify deletion
      const getResponse = await auth.get(`${API_BASE}/clients/${createdClient.id}/`);
      expect(getResponse.status()).toBe(404);
    });
  });

  test.describe('Client Cases Endpoint', () => {
    test('should get cases for a specific client', async ({ auth }) => {
      await auth.register();

      // Create a client
      const clientData = generateTestClient();
      const createResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const createdClient = await createResponse.json();

      // Create a case for this client
      const today = new Date().toISOString().split('T')[0];
      const caseData = {
        client: createdClient.id,
        title: `Test Case ${Date.now()}`,
        description: 'Test case description',
        case_type: 'civil',
        status: 'en_proceso',
        priority: 'media',
        start_date: today,
      };
      await auth.post(`${API_BASE}/cases/`, caseData);

      // Get client's cases
      const response = await auth.get(`${API_BASE}/clients/${createdClient.id}/cases/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(Array.isArray(body)).toBeTruthy();
      expect(body.length).toBeGreaterThan(0);
      expect(body[0].client).toBe(createdClient.id);
    });
  });

  test.describe('Authentication', () => {
    test('should reject unauthenticated requests', async ({ request }) => {
      const response = await request.get(`${API_BASE}/clients/`);
      expect(response.status()).toBe(401);
    });
  });
});

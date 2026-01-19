/**
 * Cases API E2E Tests
 *
 * Tests for:
 * - CRUD operations on cases
 * - Auto-generation of case_number
 * - Filtering by status, case_type, priority
 * - Close case action
 * - Statistics endpoint
 */

import { test, expect, API_BASE, generateTestClient, generateTestCase } from '../fixtures/auth';

test.describe('Cases API', () => {
  // Helper to create a client and return its ID
  async function createTestClient(auth: any): Promise<number> {
    const clientData = generateTestClient();
    const response = await auth.post(`${API_BASE}/clients/`, clientData);
    const client = await response.json();
    return client.id;
  }

  test.describe('List Cases', () => {
    test('should list cases with filters', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/cases/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(Array.isArray(body) || body.results !== undefined).toBeTruthy();
    });

    test('should filter cases by status', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case with specific status
      const caseData = generateTestCase(clientId);
      caseData.status = 'en_revision';
      await auth.post(`${API_BASE}/cases/`, caseData);

      // Filter by status
      const response = await auth.get(`${API_BASE}/cases/?status=en_revision`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      results.forEach((caseItem: any) => {
        expect(caseItem.status).toBe('en_revision');
      });
    });

    test('should filter cases by case_type', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case with specific type
      const caseData = generateTestCase(clientId);
      caseData.case_type = 'penal';
      await auth.post(`${API_BASE}/cases/`, caseData);

      // Filter by case_type
      const response = await auth.get(`${API_BASE}/cases/?case_type=penal`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      results.forEach((caseItem: any) => {
        expect(caseItem.case_type).toBe('penal');
      });
    });

    test('should filter cases by priority', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case with specific priority
      const caseData = generateTestCase(clientId);
      caseData.priority = 'urgente';
      await auth.post(`${API_BASE}/cases/`, caseData);

      // Filter by priority
      const response = await auth.get(`${API_BASE}/cases/?priority=urgente`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      results.forEach((caseItem: any) => {
        expect(caseItem.priority).toBe('urgente');
      });
    });

    test('should search cases by case_number', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case
      const caseData = generateTestCase(clientId);
      const createResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await createResponse.json();

      // Search by case_number
      const response = await auth.get(`${API_BASE}/cases/?search=${encodeURIComponent(createdCase.case_number)}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      expect(results.length).toBeGreaterThan(0);
      expect(results[0].case_number).toBe(createdCase.case_number);
    });

    test('should search cases by title', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case with unique title
      const uniqueTitle = `Unique Case Title ${Date.now()}`;
      const caseData = generateTestCase(clientId);
      caseData.title = uniqueTitle;
      await auth.post(`${API_BASE}/cases/`, caseData);

      // Search by title
      const response = await auth.get(`${API_BASE}/cases/?search=${encodeURIComponent(uniqueTitle)}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      expect(results.length).toBeGreaterThan(0);
      expect(results[0].title).toBe(uniqueTitle);
    });
  });

  test.describe('Create Case', () => {
    test('should create case and auto-generate case_number', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      const caseData = generateTestCase(clientId);
      const response = await auth.post(`${API_BASE}/cases/`, caseData);
      expect(response.status()).toBe(201);

      const body = await response.json();
      expect(body.id).toBeDefined();
      expect(body.case_number).toBeDefined();
      expect(body.case_number).toMatch(/^CASE-\d{4}-\d{4}$/);
      expect(body.title).toBe(caseData.title);
      expect(body.description).toBe(caseData.description);
      expect(body.case_type).toBe(caseData.case_type);
      expect(body.status).toBe(caseData.status);
      expect(body.priority).toBe(caseData.priority);
    });

    test('should reject case with missing required fields', async ({ auth }) => {
      await auth.register();

      const response = await auth.post(`${API_BASE}/cases/`, {
        title: 'Test Case',
        // Missing required fields
      });

      expect(response.status()).toBe(400);
    });

    test('should reject case with invalid client ID', async ({ auth }) => {
      await auth.register();

      const caseData = generateTestCase(99999);
      const response = await auth.post(`${API_BASE}/cases/`, caseData);
      expect(response.status()).toBe(400);
    });
  });

  test.describe('Retrieve Case', () => {
    test('should get case by ID with detailed serializer', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case
      const caseData = generateTestCase(clientId);
      const createResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await createResponse.json();

      // Retrieve the case
      const response = await auth.get(`${API_BASE}/cases/${createdCase.id}/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.id).toBe(createdCase.id);
      expect(body.case_number).toBe(createdCase.case_number);
      expect(body.title).toBe(caseData.title);
    });

    test('should return 404 for non-existent case', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/cases/99999/`);
      expect(response.status()).toBe(404);
    });
  });

  test.describe('Update Case', () => {
    test('should update case successfully', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case
      const caseData = generateTestCase(clientId);
      const createResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await createResponse.json();

      // Update the case
      const updatedData = {
        ...caseData,
        title: 'Updated Case Title',
        priority: 'alta',
      };

      const response = await auth.put(`${API_BASE}/cases/${createdCase.id}/`, updatedData);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.title).toBe('Updated Case Title');
      expect(body.priority).toBe('alta');
    });

    test('should partially update case with PATCH', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case
      const caseData = generateTestCase(clientId);
      const createResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await createResponse.json();

      // Partially update the case
      const response = await auth.patch(`${API_BASE}/cases/${createdCase.id}/`, {
        status: 'pendiente_documentos',
      });
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.status).toBe('pendiente_documentos');
      expect(body.title).toBe(caseData.title); // Unchanged
    });
  });

  test.describe('Close Case Action', () => {
    test('should close case successfully', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case
      const caseData = generateTestCase(clientId);
      const createResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await createResponse.json();

      // Close the case
      const response = await auth.post(`${API_BASE}/cases/${createdCase.id}/close/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.status).toBe('cerrado');
      expect(body.closed_date).toBeDefined();
    });

    test('should reject closing already closed case', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case
      const caseData = generateTestCase(clientId);
      const createResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await createResponse.json();

      // Close the case
      await auth.post(`${API_BASE}/cases/${createdCase.id}/close/`);

      // Try to close again
      const response = await auth.post(`${API_BASE}/cases/${createdCase.id}/close/`);
      expect(response.status()).toBe(400);

      const body = await response.json();
      expect(body.error).toBeDefined();
    });
  });

  test.describe('Statistics Endpoint', () => {
    test('should return case statistics', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/cases/statistics/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.by_status).toBeDefined();
      expect(body.by_type).toBeDefined();
      expect(body.by_priority).toBeDefined();
      expect(typeof body.total).toBe('number');
    });
  });

  test.describe('Delete Case', () => {
    test('should delete case successfully', async ({ auth }) => {
      await auth.register();
      const clientId = await createTestClient(auth);

      // Create a case
      const caseData = generateTestCase(clientId);
      const createResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await createResponse.json();

      // Delete the case
      const deleteResponse = await auth.delete(`${API_BASE}/cases/${createdCase.id}/`);
      expect(deleteResponse.status()).toBe(204);

      // Verify deletion
      const getResponse = await auth.get(`${API_BASE}/cases/${createdCase.id}/`);
      expect(getResponse.status()).toBe(404);
    });
  });

  test.describe('Authentication', () => {
    test('should reject unauthenticated requests', async ({ request }) => {
      const response = await request.get(`${API_BASE}/cases/`);
      expect(response.status()).toBe(401);
    });
  });
});

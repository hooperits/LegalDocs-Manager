/**
 * Search API E2E Tests
 *
 * Tests for:
 * - Global search across clients, cases, and documents
 * - Search result structure
 * - Empty search handling
 */

import { test, expect, API_BASE, generateTestClient, generateTestCase, createTestPDF, AuthHelper } from '../fixtures/auth';

test.describe('Search API', () => {
  // Helper to create test data
  async function createTestData(auth: AuthHelper) {
    // Create a client with unique name
    const uniqueId = `search_${Date.now()}_${Math.random().toString(36).substring(7)}`;
    const clientData = {
      ...generateTestClient(),
      full_name: `Searchable Client ${uniqueId}`,
      email: `searchable_${uniqueId}@test.com`,
    };
    const clientResponse = await auth.post(`${API_BASE}/clients/`, clientData);
    const client = await clientResponse.json();

    // Create a case with unique title
    const caseData = {
      ...generateTestCase(client.id),
      title: `Searchable Case ${uniqueId}`,
    };
    const caseResponse = await auth.post(`${API_BASE}/cases/`, caseData);
    const caseObj = await caseResponse.json();

    // Create a document with unique title
    const pdfBuffer = createTestPDF();
    const docResponse = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'searchable.pdf', {
      case: caseObj.id.toString(),
      title: `Searchable Document ${uniqueId}`,
      document_type: 'contrato',
      description: 'Test search',
      is_confidential: 'false',
    });
    const doc = await docResponse.json();

    return { client, case: caseObj, document: doc, uniqueId };
  }

  test.describe('Global Search', () => {
    test('should find clients by name', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      // Search for the client
      const response = await auth.get(`${API_BASE}/search/?q=Searchable Client ${testData.uniqueId}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.query).toContain('Searchable Client');
      expect(body.results).toBeDefined();
      expect(body.results.clients).toBeDefined();
      expect(body.results.clients.length).toBeGreaterThan(0);

      // Verify client is found
      const foundClient = body.results.clients.find((c: any) => c.id === testData.client.id);
      expect(foundClient).toBeDefined();
      expect(foundClient.type).toBe('client');
    });

    test('should find cases by title', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      // Search for the case
      const response = await auth.get(`${API_BASE}/search/?q=Searchable Case ${testData.uniqueId}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.results.cases).toBeDefined();
      expect(body.results.cases.length).toBeGreaterThan(0);

      // Verify case is found
      const foundCase = body.results.cases.find((c: any) => c.id === testData.case.id);
      expect(foundCase).toBeDefined();
      expect(foundCase.type).toBe('case');
    });

    test('should find cases by case_number', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      // Search for the case by case_number
      const response = await auth.get(`${API_BASE}/search/?q=${testData.case.case_number}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.results.cases).toBeDefined();

      // Verify case is found
      const foundCase = body.results.cases.find((c: any) => c.case_number === testData.case.case_number);
      expect(foundCase).toBeDefined();
    });

    test('should find documents by title', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      // Search for the document
      const response = await auth.get(`${API_BASE}/search/?q=Searchable Document ${testData.uniqueId}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.results.documents).toBeDefined();
      expect(body.results.documents.length).toBeGreaterThan(0);

      // Verify document is found
      const foundDoc = body.results.documents.find((d: any) => d.id === testData.document.id);
      expect(foundDoc).toBeDefined();
      expect(foundDoc.type).toBe('document');
    });

    test('should return counts for each entity type', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      // Search for the unique ID (matches all entities)
      const response = await auth.get(`${API_BASE}/search/?q=${testData.uniqueId}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.counts).toBeDefined();
      expect(typeof body.counts.clients).toBe('number');
      expect(typeof body.counts.cases).toBe('number');
      expect(typeof body.counts.documents).toBe('number');
      expect(typeof body.counts.total).toBe('number');

      // Total should equal sum of individual counts
      expect(body.counts.total).toBe(
        body.counts.clients + body.counts.cases + body.counts.documents
      );
    });

    test('should return empty results for non-matching query', async ({ auth }) => {
      await auth.register();

      // Search for something that doesn't exist
      const uniqueQuery = `nonexistent_${Date.now()}_${Math.random().toString(36).substring(7)}`;
      const response = await auth.get(`${API_BASE}/search/?q=${uniqueQuery}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.results.clients).toEqual([]);
      expect(body.results.cases).toEqual([]);
      expect(body.results.documents).toEqual([]);
      expect(body.counts.total).toBe(0);
    });

    test('should return error 400 for empty query', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/search/`);
      expect(response.status()).toBe(400);

      const body = await response.json();
      expect(body.error).toBeDefined();
    });

    test('should return error 400 for whitespace-only query', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/search/?q=   `);
      expect(response.status()).toBe(400);

      const body = await response.json();
      expect(body.error).toBeDefined();
    });
  });

  test.describe('Search Result Structure', () => {
    test('should return correct structure for client results', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      const response = await auth.get(`${API_BASE}/search/?q=${testData.client.full_name}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      if (body.results.clients.length > 0) {
        const client = body.results.clients[0];
        expect(client).toHaveProperty('id');
        expect(client).toHaveProperty('type', 'client');
        expect(client).toHaveProperty('full_name');
        expect(client).toHaveProperty('email');
      }
    });

    test('should return correct structure for case results', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      const response = await auth.get(`${API_BASE}/search/?q=${testData.case.title}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      if (body.results.cases.length > 0) {
        const caseResult = body.results.cases[0];
        expect(caseResult).toHaveProperty('id');
        expect(caseResult).toHaveProperty('type', 'case');
        expect(caseResult).toHaveProperty('case_number');
        expect(caseResult).toHaveProperty('title');
      }
    });

    test('should return correct structure for document results', async ({ auth }) => {
      await auth.register();
      const testData = await createTestData(auth);

      const response = await auth.get(`${API_BASE}/search/?q=${testData.document.title}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      if (body.results.documents.length > 0) {
        const doc = body.results.documents[0];
        expect(doc).toHaveProperty('id');
        expect(doc).toHaveProperty('type', 'document');
        expect(doc).toHaveProperty('title');
        expect(doc).toHaveProperty('document_type');
      }
    });
  });

  test.describe('Authentication', () => {
    test('should reject unauthenticated requests', async ({ request }) => {
      const response = await request.get(`${API_BASE}/search/?q=test`);
      expect(response.status()).toBe(401);
    });
  });
});

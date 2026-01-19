/**
 * Documents API E2E Tests
 *
 * Tests for:
 * - CRUD operations on documents
 * - File upload with validation
 * - File type restrictions
 * - Auto-calculation of file_size
 * - Auto-assignment of uploaded_by
 * - Owner-based delete permissions
 */

import { test, expect, API_BASE, generateTestClient, generateTestCase, generateTestDocument, createTestPDF, createTestTxt, AuthHelper } from '../fixtures/auth';

test.describe('Documents API', () => {
  // Helper to create a client and case
  async function createClientAndCase(auth: AuthHelper): Promise<{ clientId: number; caseId: number }> {
    const clientData = generateTestClient();
    const clientResponse = await auth.post(`${API_BASE}/clients/`, clientData);
    const client = await clientResponse.json();

    const caseData = generateTestCase(client.id);
    const caseResponse = await auth.post(`${API_BASE}/cases/`, caseData);
    const caseObj = await caseResponse.json();

    return { clientId: client.id, caseId: caseObj.id };
  }

  test.describe('List Documents', () => {
    test('should list documents', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/documents/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(Array.isArray(body) || body.results !== undefined).toBeTruthy();
    });

    test('should filter documents by case', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      // Upload a document
      const docData = generateTestDocument(caseId);
      const pdfBuffer = createTestPDF();
      await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'test.pdf', {
        ...docData,
        case: caseId.toString(),
      });

      // Filter by case
      const response = await auth.get(`${API_BASE}/documents/?case=${caseId}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      results.forEach((doc: any) => {
        expect(doc.case).toBe(caseId);
      });
    });

    test('should filter documents by document_type', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      // Upload a document with specific type
      const pdfBuffer = createTestPDF();
      await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'test.pdf', {
        case: caseId.toString(),
        title: 'Test Contrato',
        document_type: 'contrato',
        description: 'Test',
        is_confidential: 'false',
      });

      // Filter by document_type
      const response = await auth.get(`${API_BASE}/documents/?document_type=contrato`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      results.forEach((doc: any) => {
        expect(doc.document_type).toBe('contrato');
      });
    });
  });

  test.describe('Upload Document', () => {
    test('should upload PDF document successfully', async ({ auth }) => {
      const registerResponse = await auth.register();
      const { caseId } = await createClientAndCase(auth);

      const pdfBuffer = createTestPDF();
      const response = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'legal_doc.pdf', {
        case: caseId.toString(),
        title: 'Legal Document PDF',
        document_type: 'contrato',
        description: 'Test PDF document',
        is_confidential: 'false',
      });

      expect(response.status()).toBe(201);

      const body = await response.json();
      expect(body.id).toBeDefined();
      expect(body.title).toBe('Legal Document PDF');
      expect(body.document_type).toBe('contrato');
      expect(body.file).toBeDefined();
      expect(body.file_size).toBeGreaterThan(0);
      expect(body.uploaded_by).toBe(registerResponse.user.id);
      expect(body.uploaded_by_username).toBe(registerResponse.user.username);
    });

    test('should upload TXT document successfully', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      const txtBuffer = createTestTxt();
      const response = await auth.uploadFile(`${API_BASE}/documents/`, txtBuffer, 'notes.txt', {
        case: caseId.toString(),
        title: 'Text Notes',
        document_type: 'otro',
        description: 'Test text document',
        is_confidential: 'false',
      });

      expect(response.status()).toBe(201);

      const body = await response.json();
      expect(body.id).toBeDefined();
      expect(body.file_size).toBeGreaterThan(0);
    });

    test('should reject non-allowed file types', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      // Create a fake "executable" content
      const exeBuffer = Buffer.from('MZ\x90\x00executable content', 'binary');
      const response = await auth.uploadFile(`${API_BASE}/documents/`, exeBuffer, 'malicious.exe', {
        case: caseId.toString(),
        title: 'Malicious File',
        document_type: 'otro',
        description: 'Should be rejected',
        is_confidential: 'false',
      });

      expect(response.status()).toBe(400);

      const body = await response.json();
      // Error should mention file type (Spanish: 'archivo', English: 'file')
      const bodyStr = JSON.stringify(body);
      expect(bodyStr).toMatch(/file|archivo/);
    });

    test('should auto-calculate file_size', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      const pdfBuffer = createTestPDF();
      const response = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'sized_doc.pdf', {
        case: caseId.toString(),
        title: 'Sized Document',
        document_type: 'contrato',
        description: 'Test file size calculation',
        is_confidential: 'false',
      });

      expect(response.status()).toBe(201);

      const body = await response.json();
      expect(body.file_size).toBe(pdfBuffer.length);
    });

    test('should auto-assign uploaded_by to current user', async ({ auth }) => {
      const registerResponse = await auth.register();
      const { caseId } = await createClientAndCase(auth);

      const pdfBuffer = createTestPDF();
      const response = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'owner_doc.pdf', {
        case: caseId.toString(),
        title: 'Owner Document',
        document_type: 'contrato',
        description: 'Test uploaded_by assignment',
        is_confidential: 'false',
      });

      expect(response.status()).toBe(201);

      const body = await response.json();
      expect(body.uploaded_by).toBe(registerResponse.user.id);
      expect(body.uploaded_by_username).toBe(registerResponse.user.username);
    });
  });

  test.describe('Retrieve Document', () => {
    test('should get document by ID', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      // Upload a document
      const pdfBuffer = createTestPDF();
      const uploadResponse = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'retrieve_test.pdf', {
        case: caseId.toString(),
        title: 'Retrieve Test Document',
        document_type: 'demanda',
        description: 'Test retrieval',
        is_confidential: 'false',
      });
      const uploadedDoc = await uploadResponse.json();

      // Retrieve the document
      const response = await auth.get(`${API_BASE}/documents/${uploadedDoc.id}/`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      expect(body.id).toBe(uploadedDoc.id);
      expect(body.title).toBe('Retrieve Test Document');
      expect(body.case_number).toBeDefined();
    });

    test('should return 404 for non-existent document', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/documents/99999/`);
      expect(response.status()).toBe(404);
    });
  });

  test.describe('Delete Document', () => {
    test('should allow owner to delete document', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      // Upload a document
      const pdfBuffer = createTestPDF();
      const uploadResponse = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'delete_test.pdf', {
        case: caseId.toString(),
        title: 'Delete Test Document',
        document_type: 'contrato',
        description: 'Test deletion',
        is_confidential: 'false',
      });
      const uploadedDoc = await uploadResponse.json();

      // Delete the document
      const deleteResponse = await auth.delete(`${API_BASE}/documents/${uploadedDoc.id}/`);
      expect(deleteResponse.status()).toBe(204);

      // Verify deletion
      const getResponse = await auth.get(`${API_BASE}/documents/${uploadedDoc.id}/`);
      expect(getResponse.status()).toBe(404);
    });

    test('should reject deletion by non-owner (403)', async ({ auth, request }) => {
      // First user uploads a document
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      const pdfBuffer = createTestPDF();
      const uploadResponse = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'protected.pdf', {
        case: caseId.toString(),
        title: 'Protected Document',
        document_type: 'contrato',
        description: 'Test protection',
        is_confidential: 'false',
      });
      const uploadedDoc = await uploadResponse.json();

      // Second user tries to delete it
      const secondAuth = new AuthHelper(request);
      await secondAuth.register();

      const deleteResponse = await secondAuth.delete(`${API_BASE}/documents/${uploadedDoc.id}/`);
      expect(deleteResponse.status()).toBe(403);
    });
  });

  test.describe('Update Document', () => {
    test('should update document metadata', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      // Upload a document
      const pdfBuffer = createTestPDF();
      const uploadResponse = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'update_test.pdf', {
        case: caseId.toString(),
        title: 'Update Test Document',
        document_type: 'contrato',
        description: 'Test update',
        is_confidential: 'false',
      });
      const uploadedDoc = await uploadResponse.json();

      // Update metadata (documents API requires multipart for PATCH)
      const updateResponse = await auth.patchMultipart(`${API_BASE}/documents/${uploadedDoc.id}/`, {
        title: 'Updated Title',
        is_confidential: 'true',
      });
      expect(updateResponse.status()).toBe(200);

      const body = await updateResponse.json();
      expect(body.title).toBe('Updated Title');
      expect(body.is_confidential).toBe(true);
    });
  });

  test.describe('Search Documents', () => {
    test('should search documents by title', async ({ auth }) => {
      await auth.register();
      const { caseId } = await createClientAndCase(auth);

      // Upload a document with unique title
      const uniqueTitle = `Unique Doc Title ${Date.now()}`;
      const pdfBuffer = createTestPDF();
      await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'search_test.pdf', {
        case: caseId.toString(),
        title: uniqueTitle,
        document_type: 'contrato',
        description: 'Test search',
        is_confidential: 'false',
      });

      // Search by title
      const response = await auth.get(`${API_BASE}/documents/?search=${encodeURIComponent(uniqueTitle)}`);
      expect(response.status()).toBe(200);

      const body = await response.json();
      const results = Array.isArray(body) ? body : body.results;
      expect(results.length).toBeGreaterThan(0);
      expect(results[0].title).toBe(uniqueTitle);
    });
  });

  test.describe('Authentication', () => {
    test('should reject unauthenticated requests', async ({ request }) => {
      const response = await request.get(`${API_BASE}/documents/`);
      expect(response.status()).toBe(401);
    });
  });
});

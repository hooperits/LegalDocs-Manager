/**
 * Complete Workflow E2E Tests
 *
 * Tests for full end-to-end user journeys:
 * - Registration → Login → Create client → Create case → Upload document → Search → Dashboard
 */

import { test, expect, AuthHelper, API_BASE, createTestPDF } from '../fixtures/auth';

test.describe('Complete Workflow', () => {
  test('should complete full user journey: Register → Login → Create Client → Create Case → Upload Document → Search → Dashboard', async ({ request }) => {
    const auth = new AuthHelper(request);
    const uniqueId = `workflow_${Date.now()}_${Math.random().toString(36).substring(7)}`;

    // Step 1: Register a new user
    console.log('Step 1: Registering new user...');
    const registerResponse = await auth.register({
      username: `workflowuser_${uniqueId}`,
      email: `workflow_${uniqueId}@test.com`,
      password: 'WorkflowTest123!',
    });

    expect(registerResponse.token).toBeDefined();
    expect(registerResponse.user.id).toBeDefined();
    console.log(`  ✓ User registered: ${registerResponse.user.username}`);

    // Step 2: Verify login worked by checking /auth/me/
    console.log('Step 2: Verifying authentication...');
    const meResponse = await auth.getMe();
    expect(meResponse.username).toBe(`workflowuser_${uniqueId}`);
    console.log(`  ✓ Authentication verified for user ID: ${meResponse.id}`);

    // Step 3: Create a client
    console.log('Step 3: Creating client...');
    const clientData = {
      full_name: `Workflow Client ${uniqueId}`,
      identification_number: `WF-ID-${uniqueId}`,
      email: `workflow_client_${uniqueId}@test.com`,
      phone: '+1234567890',
      address: '123 Workflow Street',
      is_active: true,
      notes: 'Created during E2E workflow test',
    };

    const clientResponse = await auth.post(`${API_BASE}/clients/`, clientData);
    expect(clientResponse.status()).toBe(201);
    const client = await clientResponse.json();
    expect(client.id).toBeDefined();
    console.log(`  ✓ Client created: ${client.full_name} (ID: ${client.id})`);

    // Step 4: Create a case for the client
    console.log('Step 4: Creating case...');
    const today = new Date().toISOString().split('T')[0];
    const deadline = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

    const caseData = {
      client: client.id,
      title: `Workflow Case ${uniqueId}`,
      description: 'Test case created during E2E workflow',
      case_type: 'civil',
      status: 'en_proceso',
      priority: 'alta',
      start_date: today,
      deadline: deadline,
    };

    const caseResponse = await auth.post(`${API_BASE}/cases/`, caseData);
    expect(caseResponse.status()).toBe(201);
    const caseObj = await caseResponse.json();
    expect(caseObj.case_number).toBeDefined();
    expect(caseObj.case_number).toMatch(/^CASE-\d{4}-\d{4}$/);
    console.log(`  ✓ Case created: ${caseObj.case_number} - ${caseObj.title}`);

    // Step 5: Upload a document to the case
    console.log('Step 5: Uploading document...');
    const pdfBuffer = createTestPDF();
    const docResponse = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, `workflow_doc_${uniqueId}.pdf`, {
      case: caseObj.id.toString(),
      title: `Workflow Document ${uniqueId}`,
      document_type: 'contrato',
      description: 'Document uploaded during E2E workflow test',
      is_confidential: 'false',
    });
    expect(docResponse.status()).toBe(201);
    const doc = await docResponse.json();
    expect(doc.id).toBeDefined();
    expect(doc.uploaded_by).toBe(registerResponse.user.id);
    console.log(`  ✓ Document uploaded: ${doc.title} (Size: ${doc.file_size} bytes)`);

    // Step 6: Search for the created entities
    console.log('Step 6: Testing search...');

    // Search for client
    const clientSearchResponse = await auth.get(`${API_BASE}/search/?q=${encodeURIComponent(client.full_name)}`);
    expect(clientSearchResponse.status()).toBe(200);
    const clientSearchResult = await clientSearchResponse.json();
    expect(clientSearchResult.results.clients.length).toBeGreaterThan(0);
    const foundClient = clientSearchResult.results.clients.find((c: any) => c.id === client.id);
    expect(foundClient).toBeDefined();
    console.log(`  ✓ Client found in search results`);

    // Search for case
    const caseSearchResponse = await auth.get(`${API_BASE}/search/?q=${encodeURIComponent(caseObj.title)}`);
    expect(caseSearchResponse.status()).toBe(200);
    const caseSearchResult = await caseSearchResponse.json();
    expect(caseSearchResult.results.cases.length).toBeGreaterThan(0);
    const foundCase = caseSearchResult.results.cases.find((c: any) => c.id === caseObj.id);
    expect(foundCase).toBeDefined();
    console.log(`  ✓ Case found in search results`);

    // Search for document
    const docSearchResponse = await auth.get(`${API_BASE}/search/?q=${encodeURIComponent(doc.title)}`);
    expect(docSearchResponse.status()).toBe(200);
    const docSearchResult = await docSearchResponse.json();
    expect(docSearchResult.results.documents.length).toBeGreaterThan(0);
    const foundDoc = docSearchResult.results.documents.find((d: any) => d.id === doc.id);
    expect(foundDoc).toBeDefined();
    console.log(`  ✓ Document found in search results`);

    // Step 7: Check dashboard
    console.log('Step 7: Checking dashboard...');
    const dashboardResponse = await auth.get(`${API_BASE}/dashboard/`);
    expect(dashboardResponse.status()).toBe(200);
    const dashboard = await dashboardResponse.json();
    expect(dashboard.total_clients).toBeGreaterThan(0);
    expect(dashboard.cases_by_status).toBeDefined();
    expect(dashboard.recent_cases).toBeDefined();
    console.log(`  ✓ Dashboard retrieved - Total clients: ${dashboard.total_clients}, Active: ${dashboard.active_clients}`);

    // Verify our case appears in recent cases if it's recent enough
    const recentCaseIds = dashboard.recent_cases.map((c: any) => c.id);
    console.log(`  ✓ Recent cases include ${recentCaseIds.length} cases`);

    // Step 8: Verify client's cases endpoint
    console.log('Step 8: Verifying client-case relationship...');
    const clientCasesResponse = await auth.get(`${API_BASE}/clients/${client.id}/cases/`);
    expect(clientCasesResponse.status()).toBe(200);
    const clientCases = await clientCasesResponse.json();
    expect(clientCases.length).toBeGreaterThan(0);
    expect(clientCases[0].client).toBe(client.id);
    console.log(`  ✓ Client has ${clientCases.length} associated case(s)`);

    // Step 9: Get case statistics
    console.log('Step 9: Getting case statistics...');
    const statsResponse = await auth.get(`${API_BASE}/cases/statistics/`);
    expect(statsResponse.status()).toBe(200);
    const stats = await statsResponse.json();
    expect(stats.total).toBeGreaterThan(0);
    expect(stats.by_status).toBeDefined();
    console.log(`  ✓ Statistics - Total cases: ${stats.total}`);

    // Step 10: Close the case
    console.log('Step 10: Closing case...');
    const closeResponse = await auth.post(`${API_BASE}/cases/${caseObj.id}/close/`);
    expect(closeResponse.status()).toBe(200);
    const closedCase = await closeResponse.json();
    expect(closedCase.status).toBe('cerrado');
    expect(closedCase.closed_date).toBeDefined();
    console.log(`  ✓ Case closed on ${closedCase.closed_date}`);

    // Step 11: Update user profile
    console.log('Step 11: Updating profile...');
    const profileUpdateResponse = await auth.patch(`${API_BASE}/profile/`, {
      first_name: 'Workflow',
      last_name: 'Test User',
    });
    expect(profileUpdateResponse.status()).toBe(200);
    const updatedProfile = await profileUpdateResponse.json();
    expect(updatedProfile.first_name).toBe('Workflow');
    expect(updatedProfile.last_name).toBe('Test User');
    console.log(`  ✓ Profile updated: ${updatedProfile.first_name} ${updatedProfile.last_name}`);

    // Step 12: Logout
    console.log('Step 12: Logging out...');
    await auth.logout();
    console.log(`  ✓ Logged out successfully`);

    // Step 13: Verify token is invalidated
    console.log('Step 13: Verifying token invalidation...');
    const invalidResponse = await request.get(`${API_BASE}/auth/me/`, {
      headers: {
        'Authorization': `Token ${registerResponse.token}`,
      },
    });
    expect(invalidResponse.status()).toBe(401);
    console.log(`  ✓ Token correctly invalidated`);

    console.log('\n✅ Complete workflow test passed!');
  });

  test('should handle case lifecycle: Create → Update → Assign → Close', async ({ request }) => {
    const auth = new AuthHelper(request);
    const uniqueId = `lifecycle_${Date.now()}_${Math.random().toString(36).substring(7)}`;

    // Register and setup
    const registerResponse = await auth.register({
      username: `lifecycleuser_${uniqueId}`,
    });

    // Create client
    const clientResponse = await auth.post(`${API_BASE}/clients/`, {
      full_name: `Lifecycle Client ${uniqueId}`,
      identification_number: `LC-${uniqueId}`,
      email: `lifecycle_${uniqueId}@test.com`,
      phone: '+1234567890',
    });
    const client = await clientResponse.json();

    // Create case
    const today = new Date().toISOString().split('T')[0];
    const caseResponse = await auth.post(`${API_BASE}/cases/`, {
      client: client.id,
      title: `Lifecycle Case ${uniqueId}`,
      description: 'Testing case lifecycle',
      case_type: 'laboral',
      status: 'en_proceso',
      priority: 'baja',
      start_date: today,
    });
    expect(caseResponse.status()).toBe(201);
    const caseObj = await caseResponse.json();
    expect(caseObj.status).toBe('en_proceso');
    console.log(`Case created with status: ${caseObj.status}`);

    // Update case status
    const updateResponse = await auth.patch(`${API_BASE}/cases/${caseObj.id}/`, {
      status: 'pendiente_documentos',
      priority: 'alta',
    });
    expect(updateResponse.status()).toBe(200);
    const updatedCase = await updateResponse.json();
    expect(updatedCase.status).toBe('pendiente_documentos');
    expect(updatedCase.priority).toBe('alta');
    console.log(`Case updated - Status: ${updatedCase.status}, Priority: ${updatedCase.priority}`);

    // Assign case to user
    const assignResponse = await auth.patch(`${API_BASE}/cases/${caseObj.id}/`, {
      assigned_to: registerResponse.user.id,
    });
    expect(assignResponse.status()).toBe(200);
    const assignedCase = await assignResponse.json();
    expect(assignedCase.assigned_to).toBe(registerResponse.user.id);
    console.log(`Case assigned to user ID: ${assignedCase.assigned_to}`);

    // Move to review
    const reviewResponse = await auth.patch(`${API_BASE}/cases/${caseObj.id}/`, {
      status: 'en_revision',
    });
    expect(reviewResponse.status()).toBe(200);
    const reviewCase = await reviewResponse.json();
    expect(reviewCase.status).toBe('en_revision');
    console.log(`Case moved to review: ${reviewCase.status}`);

    // Close case
    const closeResponse = await auth.post(`${API_BASE}/cases/${caseObj.id}/close/`);
    expect(closeResponse.status()).toBe(200);
    const closedCase = await closeResponse.json();
    expect(closedCase.status).toBe('cerrado');
    expect(closedCase.closed_date).toBeDefined();
    console.log(`Case closed on: ${closedCase.closed_date}`);

    // Verify cannot close again
    const reCloseResponse = await auth.post(`${API_BASE}/cases/${caseObj.id}/close/`);
    expect(reCloseResponse.status()).toBe(400);
    console.log('Correctly prevented re-closing of case');

    console.log('\n✅ Case lifecycle test passed!');
  });

  test('should handle document management flow', async ({ request }) => {
    const auth = new AuthHelper(request);
    const uniqueId = `docflow_${Date.now()}_${Math.random().toString(36).substring(7)}`;

    // Setup
    await auth.register({ username: `docflowuser_${uniqueId}` });

    const clientResponse = await auth.post(`${API_BASE}/clients/`, {
      full_name: `DocFlow Client ${uniqueId}`,
      identification_number: `DF-${uniqueId}`,
      email: `docflow_${uniqueId}@test.com`,
      phone: '+1234567890',
    });
    const client = await clientResponse.json();

    const today = new Date().toISOString().split('T')[0];
    const caseResponse = await auth.post(`${API_BASE}/cases/`, {
      client: client.id,
      title: `DocFlow Case ${uniqueId}`,
      description: 'Testing document flow',
      case_type: 'mercantil',
      start_date: today,
    });
    const caseObj = await caseResponse.json();

    // Upload multiple documents
    const pdfBuffer = createTestPDF();

    // Document 1: Contrato
    const doc1Response = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'contrato.pdf', {
      case: caseObj.id.toString(),
      title: 'Contrato Principal',
      document_type: 'contrato',
      description: 'Main contract',
      is_confidential: 'false',
    });
    expect(doc1Response.status()).toBe(201);
    const doc1 = await doc1Response.json();
    console.log(`Document 1 uploaded: ${doc1.title}`);

    // Document 2: Demanda (confidential)
    const doc2Response = await auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'demanda.pdf', {
      case: caseObj.id.toString(),
      title: 'Demanda Legal',
      document_type: 'demanda',
      description: 'Legal complaint',
      is_confidential: 'true',
    });
    expect(doc2Response.status()).toBe(201);
    const doc2 = await doc2Response.json();
    expect(doc2.is_confidential).toBe(true);
    console.log(`Document 2 uploaded (confidential): ${doc2.title}`);

    // List documents for case
    const listResponse = await auth.get(`${API_BASE}/documents/?case=${caseObj.id}`);
    expect(listResponse.status()).toBe(200);
    const docList = await listResponse.json();
    const docs = Array.isArray(docList) ? docList : docList.results;
    expect(docs.length).toBe(2);
    console.log(`Total documents for case: ${docs.length}`);

    // Filter confidential documents
    const confidentialResponse = await auth.get(`${API_BASE}/documents/?case=${caseObj.id}&is_confidential=true`);
    expect(confidentialResponse.status()).toBe(200);
    const confidentialDocs = await confidentialResponse.json();
    const confidentialList = Array.isArray(confidentialDocs) ? confidentialDocs : confidentialDocs.results;
    expect(confidentialList.length).toBe(1);
    expect(confidentialList[0].title).toBe('Demanda Legal');
    console.log(`Confidential documents: ${confidentialList.length}`);

    // Update document metadata
    const updateResponse = await auth.patch(`${API_BASE}/documents/${doc1.id}/`, {
      title: 'Contrato Principal Actualizado',
      description: 'Updated contract description',
    });
    expect(updateResponse.status()).toBe(200);
    const updatedDoc = await updateResponse.json();
    expect(updatedDoc.title).toBe('Contrato Principal Actualizado');
    console.log(`Document updated: ${updatedDoc.title}`);

    // Delete document
    const deleteResponse = await auth.delete(`${API_BASE}/documents/${doc2.id}/`);
    expect(deleteResponse.status()).toBe(204);
    console.log('Document deleted successfully');

    // Verify deletion
    const verifyResponse = await auth.get(`${API_BASE}/documents/${doc2.id}/`);
    expect(verifyResponse.status()).toBe(404);
    console.log('Deletion verified');

    console.log('\n✅ Document flow test passed!');
  });

  test('should handle multi-user collaboration scenario', async ({ request }) => {
    const uniqueId = `collab_${Date.now()}_${Math.random().toString(36).substring(7)}`;

    // User 1: Creates client and case
    const user1Auth = new AuthHelper(request);
    const user1 = await user1Auth.register({ username: `collab_user1_${uniqueId}` });
    console.log(`User 1 registered: ${user1.user.username}`);

    const clientResponse = await user1Auth.post(`${API_BASE}/clients/`, {
      full_name: `Collab Client ${uniqueId}`,
      identification_number: `CC-${uniqueId}`,
      email: `collab_${uniqueId}@test.com`,
      phone: '+1234567890',
    });
    const client = await clientResponse.json();
    console.log(`Client created by User 1: ${client.full_name}`);

    const today = new Date().toISOString().split('T')[0];
    const caseResponse = await user1Auth.post(`${API_BASE}/cases/`, {
      client: client.id,
      title: `Collaboration Case ${uniqueId}`,
      description: 'Testing multi-user access',
      case_type: 'civil',
      start_date: today,
    });
    const caseObj = await caseResponse.json();
    console.log(`Case created by User 1: ${caseObj.case_number}`);

    // User 1 uploads a document
    const pdfBuffer = createTestPDF();
    const doc1Response = await user1Auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'user1_doc.pdf', {
      case: caseObj.id.toString(),
      title: `User1 Document ${uniqueId}`,
      document_type: 'contrato',
      description: 'Uploaded by user 1',
      is_confidential: 'false',
    });
    const doc1 = await doc1Response.json();
    console.log(`Document uploaded by User 1: ${doc1.title}`);

    // User 2: Registers and can view the same data
    const user2Auth = new AuthHelper(request);
    const user2 = await user2Auth.register({ username: `collab_user2_${uniqueId}` });
    console.log(`User 2 registered: ${user2.user.username}`);

    // User 2 can view the client
    const viewClientResponse = await user2Auth.get(`${API_BASE}/clients/${client.id}/`);
    expect(viewClientResponse.status()).toBe(200);
    console.log('User 2 can view client created by User 1');

    // User 2 can view the case
    const viewCaseResponse = await user2Auth.get(`${API_BASE}/cases/${caseObj.id}/`);
    expect(viewCaseResponse.status()).toBe(200);
    console.log('User 2 can view case created by User 1');

    // User 2 can view documents
    const viewDocsResponse = await user2Auth.get(`${API_BASE}/documents/?case=${caseObj.id}`);
    expect(viewDocsResponse.status()).toBe(200);
    console.log('User 2 can view documents');

    // User 2 uploads their own document
    const doc2Response = await user2Auth.uploadFile(`${API_BASE}/documents/`, pdfBuffer, 'user2_doc.pdf', {
      case: caseObj.id.toString(),
      title: `User2 Document ${uniqueId}`,
      document_type: 'demanda',
      description: 'Uploaded by user 2',
      is_confidential: 'false',
    });
    const doc2 = await doc2Response.json();
    expect(doc2.uploaded_by).toBe(user2.user.id);
    console.log(`Document uploaded by User 2: ${doc2.title}`);

    // User 2 CANNOT delete User 1's document (ownership check)
    const deleteAttemptResponse = await user2Auth.delete(`${API_BASE}/documents/${doc1.id}/`);
    expect(deleteAttemptResponse.status()).toBe(403);
    console.log("User 2 correctly blocked from deleting User 1's document");

    // User 2 CAN delete their own document
    const deleteOwnResponse = await user2Auth.delete(`${API_BASE}/documents/${doc2.id}/`);
    expect(deleteOwnResponse.status()).toBe(204);
    console.log('User 2 successfully deleted their own document');

    // Both users see same dashboard stats
    const user1Dashboard = await user1Auth.get(`${API_BASE}/dashboard/`);
    const user2Dashboard = await user2Auth.get(`${API_BASE}/dashboard/`);

    const user1Stats = await user1Dashboard.json();
    const user2Stats = await user2Dashboard.json();

    expect(user1Stats.total_clients).toBe(user2Stats.total_clients);
    console.log('Both users see consistent dashboard data');

    console.log('\n✅ Multi-user collaboration test passed!');
  });
});

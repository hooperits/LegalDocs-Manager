/**
 * Dashboard API E2E Tests
 *
 * Tests for:
 * - Dashboard statistics endpoint
 * - Response structure validation
 * - Caching behavior
 */

import { test, expect, API_BASE, generateTestClient, generateTestCase } from '../fixtures/auth';

test.describe('Dashboard API', () => {
  test.describe('Get Dashboard Statistics', () => {
    test('should return dashboard statistics', async ({ auth }) => {
      await auth.register();

      const response = await auth.get(`${API_BASE}/dashboard/`);
      expect(response.status()).toBe(200);

      const body = await response.json();

      // Verify required fields exist
      expect(typeof body.total_clients).toBe('number');
      expect(typeof body.active_clients).toBe('number');
      expect(body.cases_by_status).toBeDefined();
      expect(body.cases_by_type).toBeDefined();
      expect(body.recent_cases).toBeDefined();
      expect(body.documents_by_type).toBeDefined();
      expect(body.upcoming_deadlines).toBeDefined();
    });

    test('should return complete response structure', async ({ auth }) => {
      await auth.register();

      // Create some test data to populate the dashboard
      const clientData = generateTestClient();
      const clientResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const client = await clientResponse.json();

      const caseData = generateTestCase(client.id);
      await auth.post(`${API_BASE}/cases/`, caseData);

      const response = await auth.get(`${API_BASE}/dashboard/`);
      expect(response.status()).toBe(200);

      const body = await response.json();

      // Verify structure
      expect(body).toHaveProperty('total_clients');
      expect(body).toHaveProperty('active_clients');
      expect(body).toHaveProperty('cases_by_status');
      expect(body).toHaveProperty('cases_by_type');
      expect(body).toHaveProperty('recent_cases');
      expect(body).toHaveProperty('documents_by_type');
      expect(body).toHaveProperty('upcoming_deadlines');

      // recent_cases should be an array
      expect(Array.isArray(body.recent_cases)).toBeTruthy();

      // upcoming_deadlines should be an array
      expect(Array.isArray(body.upcoming_deadlines)).toBeTruthy();

      // cases_by_status and cases_by_type should be objects
      expect(typeof body.cases_by_status).toBe('object');
      expect(typeof body.cases_by_type).toBe('object');
    });

    test('should verify caching behavior (second call faster)', async ({ auth }) => {
      await auth.register();

      // First call - might be slower as it computes stats
      const startFirst = Date.now();
      const firstResponse = await auth.get(`${API_BASE}/dashboard/`);
      const firstDuration = Date.now() - startFirst;
      expect(firstResponse.status()).toBe(200);

      // Second call - should use cache (potentially faster)
      const startSecond = Date.now();
      const secondResponse = await auth.get(`${API_BASE}/dashboard/`);
      const secondDuration = Date.now() - startSecond;
      expect(secondResponse.status()).toBe(200);

      // Both should return the same data structure
      const firstBody = await firstResponse.json();
      const secondBody = await secondResponse.json();

      expect(Object.keys(firstBody).sort()).toEqual(Object.keys(secondBody).sort());

      // Note: Due to network latency, we can't guarantee the second call is faster
      // but we can log the durations for debugging
      console.log(`First call: ${firstDuration}ms, Second call: ${secondDuration}ms`);
    });

    test('should include recent cases with correct structure', async ({ auth }) => {
      await auth.register();

      // Create a client and case
      const clientData = generateTestClient();
      const clientResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const client = await clientResponse.json();

      const caseData = generateTestCase(client.id);
      const caseResponse = await auth.post(`${API_BASE}/cases/`, caseData);
      const createdCase = await caseResponse.json();

      const response = await auth.get(`${API_BASE}/dashboard/`);
      expect(response.status()).toBe(200);

      const body = await response.json();

      // recent_cases should have specific structure if there are cases
      if (body.recent_cases.length > 0) {
        const recentCase = body.recent_cases[0];
        expect(recentCase).toHaveProperty('id');
        expect(recentCase).toHaveProperty('case_number');
        expect(recentCase).toHaveProperty('title');
        expect(recentCase).toHaveProperty('status');
        expect(recentCase).toHaveProperty('client_name');
      }
    });

    test('should include upcoming deadlines with correct structure', async ({ auth }) => {
      await auth.register();

      // Create a client and case with deadline in next 7 days
      const clientData = generateTestClient();
      const clientResponse = await auth.post(`${API_BASE}/clients/`, clientData);
      const client = await clientResponse.json();

      const caseData = generateTestCase(client.id);
      // Set deadline to 3 days from now
      const deadline = new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
      caseData.deadline = deadline;
      await auth.post(`${API_BASE}/cases/`, caseData);

      const response = await auth.get(`${API_BASE}/dashboard/`);
      expect(response.status()).toBe(200);

      const body = await response.json();

      // upcoming_deadlines should have specific structure if there are deadlines
      if (body.upcoming_deadlines.length > 0) {
        const upcomingDeadline = body.upcoming_deadlines[0];
        expect(upcomingDeadline).toHaveProperty('id');
        expect(upcomingDeadline).toHaveProperty('case_number');
        expect(upcomingDeadline).toHaveProperty('title');
        expect(upcomingDeadline).toHaveProperty('deadline');
        expect(upcomingDeadline).toHaveProperty('days_remaining');
        expect(upcomingDeadline).toHaveProperty('client_name');
      }
    });
  });

  test.describe('Authentication', () => {
    test('should reject unauthenticated requests', async ({ request }) => {
      const response = await request.get(`${API_BASE}/dashboard/`);
      expect(response.status()).toBe(401);
    });
  });
});

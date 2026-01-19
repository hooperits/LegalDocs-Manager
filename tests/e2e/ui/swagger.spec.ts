/**
 * Swagger UI E2E Tests
 *
 * Tests for:
 * - Swagger UI page loads
 * - All endpoints are documented
 * - Authentication works from Swagger
 * - API execution from Swagger UI
 */

import { test, expect } from '@playwright/test';

test.describe('Swagger UI', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to Swagger UI
    await page.goto('/api/v1/docs/');
  });

  test.describe('Page Load', () => {
    test('should load Swagger UI page', async ({ page }) => {
      // Wait for Swagger UI to load
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });
    });

    test('should display API title', async ({ page }) => {
      // Wait for the title to appear
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Check for the API title (from drf-spectacular)
      const title = page.locator('.swagger-ui .title');
      await expect(title).toBeVisible({ timeout: 5000 });
    });

    test('should display API version', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Check for version info
      const versionInfo = page.locator('.swagger-ui .info');
      await expect(versionInfo).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Endpoint Documentation', () => {
    test('should document auth endpoints', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Look for auth endpoints
      const authSection = page.locator('text=/auth/');
      await expect(authSection.first()).toBeVisible({ timeout: 5000 });
    });

    test('should document clients endpoints', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Look for clients endpoint
      const clientsSection = page.locator('text=/clients/');
      await expect(clientsSection.first()).toBeVisible({ timeout: 5000 });
    });

    test('should document cases endpoints', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Look for cases endpoint
      const casesSection = page.locator('text=/cases/');
      await expect(casesSection.first()).toBeVisible({ timeout: 5000 });
    });

    test('should document documents endpoints', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Look for documents endpoint
      const documentsSection = page.locator('text=/documents/');
      await expect(documentsSection.first()).toBeVisible({ timeout: 5000 });
    });

    test('should document dashboard endpoint', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Look for dashboard endpoint
      const dashboardSection = page.locator('text=/dashboard/');
      await expect(dashboardSection.first()).toBeVisible({ timeout: 5000 });
    });

    test('should document search endpoint', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Look for search endpoint
      const searchSection = page.locator('text=/search/');
      await expect(searchSection.first()).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Swagger Interaction', () => {
    test('should expand endpoint details on click', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Find and click on a POST endpoint (like login)
      const loginEndpoint = page.locator('.opblock-summary').filter({ hasText: '/auth/login/' }).first();

      if (await loginEndpoint.isVisible()) {
        await loginEndpoint.click();

        // Should show request body section
        const requestBody = page.locator('.opblock-body');
        await expect(requestBody.first()).toBeVisible({ timeout: 5000 });
      }
    });

    test('should show "Try it out" button', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Find an endpoint and expand it
      const endpoint = page.locator('.opblock-summary').first();

      if (await endpoint.isVisible()) {
        await endpoint.click();

        // Look for "Try it out" button
        const tryItButton = page.locator('button').filter({ hasText: 'Try it out' }).first();
        await expect(tryItButton).toBeVisible({ timeout: 5000 });
      }
    });

    test('should have authorize button for authentication', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Look for the authorize button
      const authorizeButton = page.locator('.authorize');
      await expect(authorizeButton).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Authentication from Swagger', () => {
    test('should open auth modal when clicking Authorize', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Click authorize button
      const authorizeButton = page.locator('.authorize');
      await authorizeButton.click();

      // Modal should appear
      const modal = page.locator('.modal-ux');
      await expect(modal).toBeVisible({ timeout: 5000 });
    });

    test('should show Token authentication option', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Click authorize button
      const authorizeButton = page.locator('.authorize');
      await authorizeButton.click();

      // Look for token auth section
      const tokenSection = page.locator('.modal-ux');
      await expect(tokenSection).toBeVisible({ timeout: 5000 });

      // Should have an input for the token
      const tokenInput = page.locator('.modal-ux input[type="text"]');
      await expect(tokenInput.first()).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('API Execution from Swagger', () => {
    test('should execute login request from Swagger', async ({ page }) => {
      await expect(page.locator('.swagger-ui')).toBeVisible({ timeout: 10000 });

      // Find login endpoint
      const loginEndpoint = page.locator('.opblock-summary').filter({ hasText: 'login' }).first();

      if (await loginEndpoint.isVisible()) {
        await loginEndpoint.click();

        // Click "Try it out"
        const tryItButton = page.locator('button').filter({ hasText: 'Try it out' }).first();
        await tryItButton.click();

        // Find and fill the request body textarea
        const textarea = page.locator('.body-param__text');

        if (await textarea.isVisible()) {
          // Fill with test credentials
          await textarea.fill(JSON.stringify({
            username: 'testuser',
            password: 'testpassword'
          }));

          // Click Execute
          const executeButton = page.locator('button').filter({ hasText: 'Execute' }).first();
          await executeButton.click();

          // Wait for response
          const responseSection = page.locator('.responses-table');
          await expect(responseSection).toBeVisible({ timeout: 10000 });
        }
      }
    });
  });

  test.describe('Schema Download', () => {
    test('should provide access to OpenAPI schema', async ({ page }) => {
      // Navigate to schema endpoint
      const response = await page.request.get('/api/v1/schema/');
      expect(response.status()).toBe(200);

      // Should return JSON or YAML schema
      const contentType = response.headers()['content-type'];
      expect(
        contentType?.includes('application/json') ||
        contentType?.includes('application/yaml') ||
        contentType?.includes('application/vnd.oai.openapi')
      ).toBeTruthy();
    });
  });
});

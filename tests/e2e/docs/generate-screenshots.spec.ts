/**
 * Screenshot Documentation Generator for LegalDocs Manager
 *
 * Generates comprehensive visual documentation by capturing screenshots
 * of all application interfaces: Swagger UI, Django Admin, and API endpoints.
 *
 * Usage:
 *   cd tests/e2e
 *   DISABLE_THROTTLING=1 npx playwright test docs/generate-screenshots.spec.ts
 *
 * Individual modules:
 *   npx playwright test docs/generate-screenshots.spec.ts -g "01-auth"
 *   npx playwright test docs/generate-screenshots.spec.ts -g "06-admin"
 */

import { test, expect, Page } from '@playwright/test';
import {
  captureScreenshot,
  VIEWPORT,
  logProgress,
  logModuleStart,
  logSummary,
  clearCapturedScreenshots,
  getScreenshotCount,
} from './screenshot-utils';
import { createTestData, cleanupTestData, TestDataSet } from './test-data';
import { URLS, SELECTORS, ADMIN_CREDENTIALS, MODULES } from './module-config';
import { writeReadme, validateScreenshots, getSummary } from './readme-generator';

// Shared test data across all tests
let testData: TestDataSet | null = null;

// Configure test to run sequentially (screenshots depend on order)
test.describe.configure({ mode: 'serial' });

test.describe('Screenshot Documentation Generator', () => {
  // Set viewport for consistent screenshots and increase timeout
  test.use({ viewport: VIEWPORT });
  test.setTimeout(60000); // 60 seconds per test

  test.beforeAll(async ({ request }) => {
    logProgress('Starting screenshot documentation generation...');
    clearCapturedScreenshots();

    // Verify server is available
    try {
      // Check API health endpoint instead of docs (which may have content negotiation issues)
      const response = await request.get('/api/v1/auth/me/', {
        headers: { 'Accept': 'application/json' },
      });
      // 401 means server is up but we're not authenticated - that's fine
      if (response.status() !== 401 && response.status() !== 200) {
        throw new Error(`Server returned unexpected status ${response.status()}`);
      }
      logProgress('Server is available');
    } catch (error) {
      console.error('\n❌ Server not available at http://localhost:8000');
      console.error('   Please start the Django server before running screenshot generation.');
      throw error;
    }

    // Create test data for screenshots
    testData = await createTestData(request);
  });

  test.afterAll(async ({ request }) => {
    // Optionally cleanup test data (uncomment to enable)
    // if (testData && process.env.CLEANUP_TEST_DATA === '1') {
    //   await cleanupTestData(request, testData);
    // }

    logSummary();
  });

  // ============================================================================
  // Module 01: Authentication
  // ============================================================================

  test('01-auth: Swagger authentication endpoints', async ({ page }) => {
    logModuleStart('01-auth: Authentication');

    // Navigate to Swagger UI auth section
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000); // Wait for animations and JS to settle

    // Close any auth dialogs that might be open
    const closeButton = page.locator('.close-modal, button[aria-label="Close"]').first();
    if (await closeButton.isVisible().catch(() => false)) {
      await closeButton.click().catch(() => {});
      await page.waitForTimeout(500);
    }

    // Screenshot 1: Auth section overview (full page)
    await captureScreenshot(page, {
      name: 'auth-endpoints-overview',
      module: '01-auth',
      description: 'Overview of authentication endpoints in Swagger UI, showing login, register, logout, and user info operations.',
    });

    // Screenshot 2: Login endpoint expanded - use JS click to avoid overlay issues
    const loginEndpoint = page.locator('.opblock-post').filter({ hasText: '/auth/login/' }).first();
    if (await loginEndpoint.isVisible()) {
      await loginEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      // Use force: true to bypass overlay detection
      await loginEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'login-endpoint',
        module: '01-auth',
        description: 'Login endpoint details showing required parameters (username, password) and response format.',
      });
    }

    // Screenshot 3: Register endpoint expanded
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const registerEndpoint = page.locator('.opblock-post').filter({ hasText: '/auth/register/' }).first();
    if (await registerEndpoint.isVisible()) {
      await registerEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await registerEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'register-endpoint',
        module: '01-auth',
        description: 'Registration endpoint showing required fields for creating a new user account.',
      });
    }
  });

  // ============================================================================
  // Module 02: Clients
  // ============================================================================

  test('02-clients: Swagger client management endpoints', async ({ page }) => {
    logModuleStart('02-clients: Client Management');

    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    // Screenshot 1: Clients overview
    await captureScreenshot(page, {
      name: 'clients-endpoints-overview',
      module: '02-clients',
      description: 'Overview of client management endpoints showing CRUD operations available.',
    });

    // Screenshot 2: Client list endpoint
    const listEndpoint = page.locator('.opblock-get').filter({ hasText: '/clients/' }).first();
    if (await listEndpoint.isVisible()) {
      await listEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await listEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'client-list-endpoint',
        module: '02-clients',
        description: 'Client list endpoint with filtering and pagination parameters.',
      });
    }

    // Screenshot 3: Client create endpoint
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const createEndpoint = page.locator('.opblock-post').filter({ hasText: '/clients/' }).first();
    if (await createEndpoint.isVisible()) {
      await createEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await createEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'client-create-endpoint',
        module: '02-clients',
        description: 'Client creation endpoint showing required and optional fields.',
      });
    }

    // Screenshot 4: Client detail endpoint
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const detailEndpoint = page.locator('.opblock-get').filter({ hasText: '/clients/{id}/' }).first();
    if (await detailEndpoint.isVisible()) {
      await detailEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await detailEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'client-detail-endpoint',
        module: '02-clients',
        description: 'Client detail endpoint for retrieving individual client information.',
      });
    }
  });

  // ============================================================================
  // Module 03: Cases
  // ============================================================================

  test('03-cases: Swagger case management endpoints', async ({ page }) => {
    logModuleStart('03-cases: Case Management');

    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    // Screenshot 1: Cases overview
    await captureScreenshot(page, {
      name: 'cases-endpoints-overview',
      module: '03-cases',
      description: 'Overview of case management endpoints showing all available operations.',
    });

    // Screenshot 2: Case list with filters
    const listEndpoint = page.locator('.opblock-get').filter({ hasText: '/cases/' }).first();
    if (await listEndpoint.isVisible()) {
      await listEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await listEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'case-list-filters',
        module: '03-cases',
        description: 'Case list endpoint with filtering options for status, type, priority, and client.',
      });
    }

    // Screenshot 3: Case create
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const createEndpoint = page.locator('.opblock-post').filter({ hasText: '/cases/' }).first();
    if (await createEndpoint.isVisible()) {
      await createEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await createEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'case-create-endpoint',
        module: '03-cases',
        description: 'Case creation endpoint showing required fields including client association.',
      });
    }

    // Screenshot 4: Case statistics
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const statsEndpoint = page.locator('.opblock-get').filter({ hasText: '/cases/statistics/' }).first();
    if (await statsEndpoint.isVisible()) {
      await statsEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await statsEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'case-statistics-endpoint',
        module: '03-cases',
        description: 'Case statistics endpoint providing summary counts by status, type, and priority.',
      });
    }

    // Screenshot 5: Case close action
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const closeEndpoint = page.locator('.opblock-post').filter({ hasText: '/close/' }).first();
    if (await closeEndpoint.isVisible()) {
      await closeEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await closeEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'case-close-action',
        module: '03-cases',
        description: 'Case close action endpoint for marking a case as completed.',
      });
    }
  });

  // ============================================================================
  // Module 04: Documents
  // ============================================================================

  test('04-documents: Swagger document management endpoints', async ({ page }) => {
    logModuleStart('04-documents: Document Management');

    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    // Screenshot 1: Documents overview
    await captureScreenshot(page, {
      name: 'documents-endpoints-overview',
      module: '04-documents',
      description: 'Overview of document management endpoints for file upload and management.',
    });

    // Screenshot 2: Document list
    const listEndpoint = page.locator('.opblock-get').filter({ hasText: '/documents/' }).first();
    if (await listEndpoint.isVisible()) {
      await listEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await listEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'document-list-endpoint',
        module: '04-documents',
        description: 'Document list endpoint with filtering by case and document type.',
      });
    }

    // Screenshot 3: Document upload
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const uploadEndpoint = page.locator('.opblock-post').filter({ hasText: '/documents/' }).first();
    if (await uploadEndpoint.isVisible()) {
      await uploadEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await uploadEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'document-upload-endpoint',
        module: '04-documents',
        description: 'Document upload endpoint showing multipart file upload parameters.',
      });
    }
  });

  // ============================================================================
  // Module 05: Dashboard
  // ============================================================================

  test('05-dashboard: Swagger dashboard and search endpoints', async ({ page }) => {
    logModuleStart('05-dashboard: Dashboard & Search');

    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    // Screenshot 1: Dashboard endpoint
    const dashEndpoint = page.locator('.opblock-get').filter({ hasText: '/dashboard/' }).first();
    if (await dashEndpoint.isVisible()) {
      await dashEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await dashEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'dashboard-endpoint',
        module: '05-dashboard',
        description: 'Dashboard endpoint providing aggregated statistics and recent activity.',
      });
    }

    // Screenshot 2: Search endpoint
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    const searchEndpoint = page.locator('.opblock-get').filter({ hasText: '/search/' }).first();
    if (await searchEndpoint.isVisible()) {
      await searchEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await searchEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      await captureScreenshot(page, {
        name: 'search-endpoint',
        module: '05-dashboard',
        description: 'Global search endpoint for finding clients, cases, and documents.',
      });
    } else {
      // If no search endpoint, capture API overview instead
      await captureScreenshot(page, {
        name: 'api-overview',
        module: '05-dashboard',
        description: 'API overview showing all available endpoint categories.',
      });
    }
  });

  // ============================================================================
  // Module 06: Django Admin
  // ============================================================================

  test('06-admin: Django admin interface', async ({ page }) => {
    logModuleStart('06-admin: Django Admin');

    // Screenshot 1: Admin login page
    await page.goto(URLS.adminLogin);
    await page.waitForSelector(SELECTORS.adminLoginForm, { timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(500);

    await captureScreenshot(page, {
      name: 'admin-login',
      module: '06-admin',
      description: 'Django admin login page for administrative access.',
    });

    // Try to login
    const usernameInput = page.locator('#id_username');
    const passwordInput = page.locator('#id_password');

    if (await usernameInput.isVisible() && await passwordInput.isVisible()) {
      await usernameInput.fill(ADMIN_CREDENTIALS.username);
      await passwordInput.fill(ADMIN_CREDENTIALS.password);
      await page.locator('input[type="submit"]').click();
      await page.waitForTimeout(1000);

      // Check if login was successful
      const isLoggedIn = await page.locator('#user-tools').isVisible().catch(() => false);

      if (isLoggedIn) {
        // Screenshot 2: Admin dashboard
        await captureScreenshot(page, {
          name: 'admin-dashboard',
          module: '06-admin',
          description: 'Django admin dashboard showing all registered models and management options.',
        });

        // Screenshot 3: Clients list in admin
        await page.goto(URLS.adminClients);
        await page.waitForTimeout(1000);

        await captureScreenshot(page, {
          name: 'admin-clients-list',
          module: '06-admin',
          description: 'Client management in Django admin with list display and filters.',
        });

        // Screenshot 4: Cases list in admin
        await page.goto(URLS.adminCases);
        await page.waitForTimeout(1000);

        await captureScreenshot(page, {
          name: 'admin-cases-list',
          module: '06-admin',
          description: 'Case management in Django admin with status badges and filtering.',
        });
      } else {
        console.log('  ⚠ Admin login failed - capturing login page only');
      }
    }
  });

  // ============================================================================
  // Module 07: Swagger API Overview
  // ============================================================================

  test('07-api: Swagger UI overview', async ({ page }) => {
    logModuleStart('07-api: Swagger API');

    // Screenshot 1: Full API overview
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    await captureScreenshot(page, {
      name: 'swagger-overview',
      module: '07-api',
      description: 'Complete Swagger UI overview showing all available API endpoints organized by category.',
      fullPage: true,
    });

    // Screenshot 2: API info header
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    await captureScreenshot(page, {
      name: 'swagger-header',
      module: '07-api',
      description: 'API information header showing version, description, and base URL.',
    });

    // Screenshot 3: Example endpoint with try-it-out
    await page.goto(URLS.swagger);
    await page.waitForSelector(SELECTORS.swaggerLoaded);
    await page.waitForTimeout(2000);

    // Expand a simple GET endpoint
    const getEndpoint = page.locator('.opblock-get').first();
    if (await getEndpoint.isVisible()) {
      await getEndpoint.evaluate(el => el.scrollIntoView({ block: 'center' }));
      await page.waitForTimeout(300);
      await getEndpoint.click({ force: true });
      await page.waitForTimeout(800);

      // Try to click "Try it out" if visible
      const tryItOut = page.locator('.try-out__btn').first();
      if (await tryItOut.isVisible().catch(() => false)) {
        await tryItOut.click({ force: true }).catch(() => {});
        await page.waitForTimeout(500);
      }

      await captureScreenshot(page, {
        name: 'swagger-try-it-out',
        module: '07-api',
        description: 'Swagger interactive "Try it out" feature for testing API endpoints directly.',
      });
    }
  });

  // ============================================================================
  // Final: Generate README
  // ============================================================================

  test('Generate README index', async () => {
    logProgress('Generating README.md index...');

    // Validate screenshots
    const validation = validateScreenshots();
    if (validation.missing.length > 0) {
      console.log('\n⚠ Missing screenshots:');
      for (const msg of validation.missing) {
        console.log(`   - ${msg}`);
      }
    }
    if (validation.extra.length > 0) {
      console.log('\n📌 Extra screenshots:');
      for (const msg of validation.extra) {
        console.log(`   - ${msg}`);
      }
    }

    // Generate README
    await writeReadme();

    // Print summary
    const summary = getSummary();
    console.log(`\n✅ Documentation generation complete!`);
    console.log(`   Total modules: ${summary.totalModules}`);
    console.log(`   Total screenshots: ${summary.totalScreenshots}`);
    console.log(`   Output: docs/screenshots/README.md`);

    // Assert minimum screenshots captured
    expect(summary.totalScreenshots).toBeGreaterThanOrEqual(15);
  });
});

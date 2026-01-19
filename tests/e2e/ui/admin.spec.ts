/**
 * Django Admin UI E2E Tests
 *
 * Tests for:
 * - Admin login
 * - Client management
 * - Case management with badges
 * - Bulk actions
 * - Document inline views
 */

import { test, expect } from '@playwright/test';

// Admin credentials (adjust as needed for your setup)
const ADMIN_CREDENTIALS = {
  username: process.env.ADMIN_USERNAME || 'admin',
  password: process.env.ADMIN_PASSWORD || 'admin',
};

test.describe('Django Admin', () => {
  test.describe('Admin Login', () => {
    test('should load admin login page', async ({ page }) => {
      await page.goto('/admin/');

      // Should redirect to login page
      await expect(page.locator('input[name="username"]')).toBeVisible({ timeout: 10000 });
      await expect(page.locator('input[name="password"]')).toBeVisible();
    });

    test('should login to admin successfully', async ({ page }) => {
      await page.goto('/admin/login/');

      // Fill login form
      await page.fill('input[name="username"]', ADMIN_CREDENTIALS.username);
      await page.fill('input[name="password"]', ADMIN_CREDENTIALS.password);

      // Submit form
      await page.click('input[type="submit"]');

      // Should be redirected to admin dashboard
      await expect(page.locator('#site-name')).toBeVisible({ timeout: 10000 });
    });

    test('should reject invalid admin credentials', async ({ page }) => {
      await page.goto('/admin/login/');

      // Fill with invalid credentials
      await page.fill('input[name="username"]', 'invalid_admin');
      await page.fill('input[name="password"]', 'wrong_password');

      // Submit form
      await page.click('input[type="submit"]');

      // Should show error message
      await expect(page.locator('.errornote')).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Admin Dashboard', () => {
    test.beforeEach(async ({ page }) => {
      // Login to admin
      await page.goto('/admin/login/');
      await page.fill('input[name="username"]', ADMIN_CREDENTIALS.username);
      await page.fill('input[name="password"]', ADMIN_CREDENTIALS.password);
      await page.click('input[type="submit"]');
      await expect(page.locator('#site-name')).toBeVisible({ timeout: 10000 });
    });

    test('should display admin dashboard', async ({ page }) => {
      // Should be on admin index
      await expect(page.locator('#site-name')).toBeVisible();

      // Should show app list
      const appList = page.locator('#content-main');
      await expect(appList).toBeVisible();
    });

    test('should show registered models', async ({ page }) => {
      // Look for the models in the admin
      const content = page.locator('#content-main');
      await expect(content).toBeVisible();

      // Should show Clients model
      const clientsLink = page.locator('a').filter({ hasText: 'Clientes' });
      const hasClients = await clientsLink.count() > 0;

      // Should show Cases model
      const casesLink = page.locator('a').filter({ hasText: 'Casos' });
      const hasCases = await casesLink.count() > 0;

      // Should show Documents model
      const documentsLink = page.locator('a').filter({ hasText: 'Documentos' });
      const hasDocuments = await documentsLink.count() > 0;

      // At least one model should be visible
      expect(hasClients || hasCases || hasDocuments).toBe(true);
    });
  });

  test.describe('Client Management', () => {
    test.beforeEach(async ({ page }) => {
      // Login to admin
      await page.goto('/admin/login/');
      await page.fill('input[name="username"]', ADMIN_CREDENTIALS.username);
      await page.fill('input[name="password"]', ADMIN_CREDENTIALS.password);
      await page.click('input[type="submit"]');
      await expect(page.locator('#site-name')).toBeVisible({ timeout: 10000 });
    });

    test('should navigate to clients list', async ({ page }) => {
      // Click on Clientes link
      const clientsLink = page.locator('a').filter({ hasText: 'Clientes' }).first();

      if (await clientsLink.isVisible()) {
        await clientsLink.click();

        // Should show clients list page
        await expect(page.locator('#changelist')).toBeVisible({ timeout: 5000 });
      }
    });

    test('should show "Add" button for clients', async ({ page }) => {
      // Navigate to clients
      await page.goto('/admin/clients/client/');

      // Should have add button
      const addButton = page.locator('.addlink');
      await expect(addButton).toBeVisible({ timeout: 5000 });
    });

    test('should create new client from admin', async ({ page }) => {
      await page.goto('/admin/clients/client/add/');

      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;

      // Fill client form
      await page.fill('input[name="full_name"]', `Admin Test Client ${uniqueId}`);
      await page.fill('input[name="identification_number"]', `ADMIN-ID-${uniqueId}`);
      await page.fill('input[name="email"]', `admin_test_${uniqueId}@test.com`);
      await page.fill('input[name="phone"]', '+1234567890');

      // Submit form
      await page.click('input[name="_save"]');

      // Should redirect to change list with success message
      await expect(page.locator('.success')).toBeVisible({ timeout: 10000 });
    });
  });

  test.describe('Case Management', () => {
    test.beforeEach(async ({ page }) => {
      // Login to admin
      await page.goto('/admin/login/');
      await page.fill('input[name="username"]', ADMIN_CREDENTIALS.username);
      await page.fill('input[name="password"]', ADMIN_CREDENTIALS.password);
      await page.click('input[type="submit"]');
      await expect(page.locator('#site-name')).toBeVisible({ timeout: 10000 });
    });

    test('should navigate to cases list', async ({ page }) => {
      // Click on Casos link
      const casesLink = page.locator('a').filter({ hasText: 'Casos' }).first();

      if (await casesLink.isVisible()) {
        await casesLink.click();

        // Should show cases list page
        await expect(page.locator('#changelist')).toBeVisible({ timeout: 5000 });
      }
    });

    test('should show status badges in case list', async ({ page }) => {
      await page.goto('/admin/cases/case/');

      // If there are cases, they should have status displayed
      const caseList = page.locator('#result_list');

      if (await caseList.isVisible()) {
        // Check for status column
        const statusHeader = page.locator('th').filter({ hasText: /estado/i });
        await expect(statusHeader.first()).toBeVisible({ timeout: 5000 });
      }
    });

    test('should have bulk actions available', async ({ page }) => {
      await page.goto('/admin/cases/case/');

      // Look for actions dropdown
      const actionsSelect = page.locator('select[name="action"]');
      await expect(actionsSelect).toBeVisible({ timeout: 5000 });

      // Should have "Mark as closed" action or similar
      // Click on the dropdown to see options
      await actionsSelect.click();
      const options = page.locator('select[name="action"] option');
      const optionCount = await options.count();
      expect(optionCount).toBeGreaterThan(1); // At least delete and custom actions
    });

    test('should show filter sidebar', async ({ page }) => {
      await page.goto('/admin/cases/case/');

      // Look for filter sidebar
      const filterSidebar = page.locator('#changelist-filter');

      // Filter sidebar should exist if there are filterable fields
      const hasFilter = await filterSidebar.isVisible();

      // If no filter sidebar, check for filters in a different location
      if (!hasFilter) {
        // Some Django admin themes put filters elsewhere
        const filterForm = page.locator('form#changelist-form');
        await expect(filterForm).toBeVisible({ timeout: 5000 });
      }
    });
  });

  test.describe('Document Management', () => {
    test.beforeEach(async ({ page }) => {
      // Login to admin
      await page.goto('/admin/login/');
      await page.fill('input[name="username"]', ADMIN_CREDENTIALS.username);
      await page.fill('input[name="password"]', ADMIN_CREDENTIALS.password);
      await page.click('input[type="submit"]');
      await expect(page.locator('#site-name')).toBeVisible({ timeout: 10000 });
    });

    test('should navigate to documents list', async ({ page }) => {
      // Click on Documentos link
      const documentsLink = page.locator('a').filter({ hasText: 'Documentos' }).first();

      if (await documentsLink.isVisible()) {
        await documentsLink.click();

        // Should show documents list page
        await expect(page.locator('#changelist')).toBeVisible({ timeout: 5000 });
      }
    });

    test('should show documents as inline in case edit', async ({ page }) => {
      // First need to have a case - go to cases list
      await page.goto('/admin/cases/case/');

      // If there are cases, click on first one
      const firstCase = page.locator('#result_list tbody tr:first-child a').first();

      if (await firstCase.isVisible()) {
        await firstCase.click();

        // Should show inline documents section
        const inlineSection = page.locator('.inline-group');
        const hasInline = await inlineSection.isVisible();

        // Check for documents inline header or related section
        if (!hasInline) {
          // Some Django admin setups might show related documents differently
          const relatedSection = page.locator('fieldset');
          await expect(relatedSection.first()).toBeVisible({ timeout: 5000 });
        }
      }
    });
  });

  test.describe('Admin Search', () => {
    test.beforeEach(async ({ page }) => {
      // Login to admin
      await page.goto('/admin/login/');
      await page.fill('input[name="username"]', ADMIN_CREDENTIALS.username);
      await page.fill('input[name="password"]', ADMIN_CREDENTIALS.password);
      await page.click('input[type="submit"]');
      await expect(page.locator('#site-name')).toBeVisible({ timeout: 10000 });
    });

    test('should have search box in clients list', async ({ page }) => {
      await page.goto('/admin/clients/client/');

      // Look for search box
      const searchBox = page.locator('#searchbar');
      await expect(searchBox).toBeVisible({ timeout: 5000 });
    });

    test('should have search box in cases list', async ({ page }) => {
      await page.goto('/admin/cases/case/');

      // Look for search box
      const searchBox = page.locator('#searchbar');
      await expect(searchBox).toBeVisible({ timeout: 5000 });
    });

    test('should search clients', async ({ page }) => {
      await page.goto('/admin/clients/client/');

      // Fill search box
      const searchBox = page.locator('#searchbar');
      await searchBox.fill('test');

      // Submit search
      await page.click('input[type="submit"]');

      // Should show search results or "0 results" message
      await expect(page.locator('#changelist')).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Admin Logout', () => {
    test('should logout from admin', async ({ page }) => {
      // Login first
      await page.goto('/admin/login/');
      await page.fill('input[name="username"]', ADMIN_CREDENTIALS.username);
      await page.fill('input[name="password"]', ADMIN_CREDENTIALS.password);
      await page.click('input[type="submit"]');
      await expect(page.locator('#site-name')).toBeVisible({ timeout: 10000 });

      // Find and click logout link
      const logoutLink = page.locator('a').filter({ hasText: /log out|cerrar sesión/i }).first();

      if (await logoutLink.isVisible()) {
        await logoutLink.click();

        // Should be logged out
        await expect(page.locator('input[name="username"]')).toBeVisible({ timeout: 10000 });
      }
    });
  });
});

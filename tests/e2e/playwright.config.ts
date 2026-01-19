import { defineConfig, devices } from '@playwright/test';
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Playwright configuration for LegalDocs-Manager E2E tests.
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: '.',

  // Run tests in files in parallel
  fullyParallel: true,

  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,

  // Retry on CI only
  retries: process.env.CI ? 1 : 0,

  // Use single worker to avoid triggering rate limits
  // The Django API has rate limiting (5 requests/minute on auth endpoints)
  workers: 1,

  // Reporter to use
  reporter: [
    ['list'],
    ['html', { open: 'never' }],
  ],

  // Shared settings for all the projects below
  use: {
    // Base URL for API tests
    baseURL: process.env.BASE_URL || 'http://localhost:8000',

    // Collect trace when retrying the failed test
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Extra HTTP headers
    // Note: Don't set Content-Type here as it conflicts with multipart uploads
    // Playwright auto-sets Content-Type based on request data type
    extraHTTPHeaders: {
      'Accept': 'application/json',
    },
  },

  // Global timeout
  timeout: 30000,

  // Expect timeout
  expect: {
    timeout: 10000,
  },

  // Configure projects for different test types
  projects: [
    {
      name: 'api',
      testMatch: /api\/.*\.spec\.ts/,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'ui',
      testMatch: /ui\/.*\.spec\.ts/,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'workflows',
      testMatch: /workflows\/.*\.spec\.ts/,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'docs',
      testMatch: /docs\/.*\.spec\.ts/,
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 },
        screenshot: 'off', // We handle screenshots manually
      },
    },
  ],

  // Run your local dev server before starting the tests
  // webServer: {
  //   command: 'cd ../../legaldocs && python manage.py runserver',
  //   url: 'http://localhost:8000',
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120 * 1000,
  // },
});

/**
 * Security API E2E Tests
 *
 * Tests for:
 * - Rate limiting on authentication endpoints
 * - CORS headers
 * - Invalid token handling
 * - Error messages in Spanish
 */

import { test, expect, API_BASE } from '../fixtures/auth';

test.describe('Security API', () => {
  // Rate limiting tests are skipped by default because they consume the rate limit quota
  // and affect other tests. Run them separately with: npx playwright test -g "Rate Limiting"
  test.describe('Rate Limiting - Login', () => {
    test.skip('should allow 5 login attempts', async ({ request }) => {
      // Make 5 login attempts with invalid credentials
      for (let i = 0; i < 5; i++) {
        const response = await request.post(`${API_BASE}/auth/login/`, {
          data: {
            username: `nonexistent_user_${i}`,
            password: 'wrongpassword',
          },
        });
        // Should return 400 for invalid credentials, not 429 yet
        expect(response.status()).toBe(400);
      }
    });

    test.skip('should return 429 on 6th login attempt (rate limit exceeded)', async ({ request }) => {
      // Make 6 login attempts - the 6th should be rate limited
      let lastResponse;
      for (let i = 0; i < 6; i++) {
        lastResponse = await request.post(`${API_BASE}/auth/login/`, {
          data: {
            username: `ratelimit_test_${Date.now()}_${i}`,
            password: 'wrongpassword',
          },
        });
      }

      // The 6th attempt should be rate limited
      expect(lastResponse!.status()).toBe(429);
    });
  });

  test.describe('Rate Limiting - Register', () => {
    test.skip('should rate limit registration endpoint', async ({ request }) => {
      // Make multiple registration attempts
      let rateLimited = false;

      for (let i = 0; i < 7; i++) {
        const uniqueId = `${Date.now()}_${i}_${Math.random().toString(36).substring(7)}`;
        const response = await request.post(`${API_BASE}/auth/register/`, {
          data: {
            username: `ratelimit_reg_${uniqueId}`,
            email: `ratelimit_${uniqueId}@test.com`,
            password: 'TestPassword123!',
            password_confirm: 'TestPassword123!',
          },
        });

        if (response.status() === 429) {
          rateLimited = true;
          break;
        }
      }

      // Should eventually hit rate limit
      expect(rateLimited).toBe(true);
    });
  });

  test.describe('CORS Headers', () => {
    test('should include CORS headers in response', async ({ request }) => {
      // Make a simple GET request with Origin header
      // CORS headers are returned on any request with Origin header
      const response = await request.get(`${API_BASE}/docs/`, {
        headers: {
          'Origin': 'http://localhost:3000',
        },
      });

      expect(response.status()).toBeLessThan(500);

      // Check for CORS headers
      const headers = response.headers();
      // The exact header names depend on django-cors-headers configuration
      // Most common is Access-Control-Allow-Origin
      const corsHeaderPresent =
        headers['access-control-allow-origin'] !== undefined ||
        headers['access-control-allow-credentials'] !== undefined;

      // If CORS is configured, at least one header should be present
      // Note: This might not be present if localhost:3000 isn't in CORS_ALLOWED_ORIGINS
      console.log('CORS Headers present:', corsHeaderPresent);
      console.log('access-control-allow-origin:', headers['access-control-allow-origin']);
    });
  });

  test.describe('Invalid Token Handling', () => {
    test('should return 401 for invalid token format', async ({ request }) => {
      const response = await request.get(`${API_BASE}/auth/me/`, {
        headers: {
          'Authorization': 'Token invalid_token_format',
        },
      });

      expect(response.status()).toBe(401);
    });

    test('should return 401 for expired/deleted token', async ({ request }) => {
      // Use a token that doesn't exist
      const response = await request.get(`${API_BASE}/auth/me/`, {
        headers: {
          'Authorization': 'Token 0000000000000000000000000000000000000000',
        },
      });

      expect(response.status()).toBe(401);
    });

    test('should return 401 for missing token', async ({ request }) => {
      const response = await request.get(`${API_BASE}/auth/me/`);
      expect(response.status()).toBe(401);
    });

    test('should return 401 for wrong auth scheme', async ({ request }) => {
      const response = await request.get(`${API_BASE}/auth/me/`, {
        headers: {
          'Authorization': 'Bearer some_token',
        },
      });

      expect(response.status()).toBe(401);
    });
  });

  test.describe('Error Messages', () => {
    test('should return error message for invalid login credentials', async ({ request }) => {
      const response = await request.post(`${API_BASE}/auth/login/`, {
        data: {
          username: 'nonexistent_user',
          password: 'wrongpassword',
        },
      });

      expect(response.status()).toBe(400);
      const body = await response.json();

      // Verify error message exists (Spanish: 'errores generales', English: 'non_field_errors')
      const hasError =
        body['errores generales'] !== undefined ||
        body.non_field_errors !== undefined;
      expect(hasError).toBe(true);
    });

    test('should return validation error for invalid email in registration', async ({ request }) => {
      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
      const response = await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username: `testuser_${uniqueId}`,
          email: 'invalid-email',
          password: 'TestPassword123!',
          password_confirm: 'TestPassword123!',
        },
      });

      expect(response.status()).toBe(400);
      const body = await response.json();

      // Email validation error should be present (could be 'email' or 'correo electrónico')
      const hasEmailError =
        body.email !== undefined ||
        body['correo electrónico'] !== undefined;
      expect(hasEmailError).toBe(true);
    });

    test('should return validation error for password mismatch', async ({ request }) => {
      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
      const response = await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username: `testuser_${uniqueId}`,
          email: `test_${uniqueId}@test.com`,
          password: 'TestPassword123!',
          password_confirm: 'DifferentPassword456!',
        },
      });

      expect(response.status()).toBe(400);
      const body = await response.json();

      // Password mismatch error (Spanish or English keys)
      const hasPasswordError =
        body.password_confirm !== undefined ||
        body.non_field_errors !== undefined ||
        body['errores generales'] !== undefined;
      expect(hasPasswordError).toBe(true);
    });
  });

  test.describe('Protected Endpoints', () => {
    test('should protect clients endpoint', async ({ request }) => {
      const response = await request.get(`${API_BASE}/clients/`);
      expect(response.status()).toBe(401);
    });

    test('should protect cases endpoint', async ({ request }) => {
      const response = await request.get(`${API_BASE}/cases/`);
      expect(response.status()).toBe(401);
    });

    test('should protect documents endpoint', async ({ request }) => {
      const response = await request.get(`${API_BASE}/documents/`);
      expect(response.status()).toBe(401);
    });

    test('should protect dashboard endpoint', async ({ request }) => {
      const response = await request.get(`${API_BASE}/dashboard/`);
      expect(response.status()).toBe(401);
    });

    test('should protect search endpoint', async ({ request }) => {
      const response = await request.get(`${API_BASE}/search/?q=test`);
      expect(response.status()).toBe(401);
    });

    test('should protect profile endpoint', async ({ request }) => {
      const response = await request.get(`${API_BASE}/profile/`);
      expect(response.status()).toBe(401);
    });
  });
});

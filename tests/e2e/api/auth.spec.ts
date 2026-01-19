/**
 * Authentication API E2E Tests
 *
 * Tests for:
 * - User registration
 * - Login and token generation
 * - Logout and token invalidation
 * - Current user info (/auth/me/)
 * - Error handling
 */

import { test, expect, AuthHelper, API_BASE } from '../fixtures/auth';

test.describe('Authentication API', () => {
  test.describe('Registration', () => {
    test('should register a new user successfully', async ({ request }) => {
      const auth = new AuthHelper(request);
      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;

      const response = await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username: `newuser_${uniqueId}`,
          email: `newuser_${uniqueId}@test.com`,
          password: 'SecurePassword123!',
          password_confirm: 'SecurePassword123!',
        },
      });

      expect(response.status()).toBe(201);
      const body = await response.json();
      expect(body.token).toBeDefined();
      expect(body.user).toBeDefined();
      expect(body.user.username).toBe(`newuser_${uniqueId}`);
      expect(body.user.email).toBe(`newuser_${uniqueId}@test.com`);
    });

    test('should reject registration with mismatched passwords', async ({ request }) => {
      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;

      const response = await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username: `newuser_${uniqueId}`,
          email: `newuser_${uniqueId}@test.com`,
          password: 'SecurePassword123!',
          password_confirm: 'DifferentPassword456!',
        },
      });

      expect(response.status()).toBe(400);
    });

    test('should reject registration with existing username', async ({ request }) => {
      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
      const username = `existing_${uniqueId}`;

      // First registration
      await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username,
          email: `user1_${uniqueId}@test.com`,
          password: 'SecurePassword123!',
          password_confirm: 'SecurePassword123!',
        },
      });

      // Second registration with same username
      const response = await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username,
          email: `user2_${uniqueId}@test.com`,
          password: 'SecurePassword123!',
          password_confirm: 'SecurePassword123!',
        },
      });

      expect(response.status()).toBe(400);
    });

    test('should reject registration with invalid email format', async ({ request }) => {
      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;

      const response = await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username: `newuser_${uniqueId}`,
          email: 'invalid-email',
          password: 'SecurePassword123!',
          password_confirm: 'SecurePassword123!',
        },
      });

      expect(response.status()).toBe(400);
    });
  });

  test.describe('Login', () => {
    test('should login successfully and return token', async ({ request }) => {
      const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
      const username = `logintest_${uniqueId}`;
      const password = 'TestPassword123!';

      // Register the test user first
      await request.post(`${API_BASE}/auth/register/`, {
        data: {
          username,
          email: `${username}@test.com`,
          password,
          password_confirm: password,
        },
      });

      // Now login
      const loginResponse = await request.post(`${API_BASE}/auth/login/`, {
        data: { username, password },
      });

      expect(loginResponse.status()).toBe(200);
      const body = await loginResponse.json();
      expect(body.token).toBeDefined();
      expect(body.username).toBe(username);
      expect(body.user_id).toBeDefined();
    });

    test('should reject login with invalid credentials', async ({ request }) => {
      const response = await request.post(`${API_BASE}/auth/login/`, {
        data: {
          username: 'nonexistent_user',
          password: 'wrongpassword',
        },
      });

      expect(response.status()).toBe(400);
      const body = await response.json();
      // Error messages are in Spanish - check for 'errores generales' or 'non_field_errors'
      const hasError = body['errores generales'] !== undefined || body.non_field_errors !== undefined;
      expect(hasError).toBe(true);
    });

    test('should reject login with missing credentials', async ({ request }) => {
      const response = await request.post(`${API_BASE}/auth/login/`, {
        data: {},
      });

      expect(response.status()).toBe(400);
    });
  });

  test.describe('Logout', () => {
    test('should logout successfully and invalidate token', async ({ auth, request }) => {
      // Register and get a token
      await auth.register();
      const token = auth.getToken();

      // Logout
      await auth.logout();

      // Try to use the old token - should fail
      const response = await request.get(`${API_BASE}/auth/me/`, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });

      expect(response.status()).toBe(401);
    });

    test('should reject logout without authentication', async ({ request }) => {
      const response = await request.post(`${API_BASE}/auth/logout/`);

      expect(response.status()).toBe(401);
    });
  });

  test.describe('Me Endpoint', () => {
    test('should return current user info with valid token', async ({ auth }) => {
      const registerResponse = await auth.register();
      const userInfo = await auth.getMe();

      expect(userInfo.id).toBe(registerResponse.user.id);
      expect(userInfo.username).toBe(registerResponse.user.username);
      expect(userInfo.email).toBe(registerResponse.user.email);
    });

    test('should reject access without authentication (401)', async ({ request }) => {
      const response = await request.get(`${API_BASE}/auth/me/`);

      expect(response.status()).toBe(401);
    });

    test('should reject access with invalid token (401)', async ({ request }) => {
      const response = await request.get(`${API_BASE}/auth/me/`, {
        headers: {
          'Authorization': 'Token invalid_token_12345',
        },
      });

      expect(response.status()).toBe(401);
    });
  });
});

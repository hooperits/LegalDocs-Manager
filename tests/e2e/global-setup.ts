/**
 * Global setup for Playwright tests.
 *
 * Creates a shared test user that can be reused across tests
 * to avoid hitting rate limits on the registration endpoint.
 */

import { request } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.BASE_URL || 'http://localhost:8000';

interface SharedAuth {
  token: string;
  userId: number;
  username: string;
}

export const AUTH_FILE = path.join(__dirname, '.auth.json');

async function globalSetup() {
  console.log('Setting up shared test user...');

  const context = await request.newContext({
    baseURL: API_BASE,
  });

  const uniqueId = `shared_${Date.now()}`;
  const username = `testuser_${uniqueId}`;
  const email = `testuser_${uniqueId}@test.com`;
  const password = 'TestPassword123!';

  try {
    // Register a shared test user
    const response = await context.post('/api/v1/auth/register/', {
      data: {
        username,
        email,
        password,
        password_confirm: password,
      },
    });

    if (response.status() === 201) {
      const body = await response.json();
      const auth: SharedAuth = {
        token: body.token,
        userId: body.user.id,
        username: body.user.username,
      };

      // Save auth to file for tests to use
      fs.writeFileSync(AUTH_FILE, JSON.stringify(auth, null, 2));
      console.log(`Shared user created: ${auth.username}`);
    } else if (response.status() === 429) {
      console.log('Rate limited during setup, using existing auth if available');
      // Check if we have existing auth
      if (fs.existsSync(AUTH_FILE)) {
        console.log('Using existing auth file');
      } else {
        console.warn('No existing auth file, tests may fail');
      }
    } else {
      const error = await response.text();
      console.error(`Failed to create user: ${response.status()} - ${error}`);
    }
  } catch (error) {
    console.error('Error in global setup:', error);
  }

  await context.dispose();
}

export default globalSetup;

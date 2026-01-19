/**
 * Authentication fixtures for E2E tests.
 *
 * Provides helper functions and test fixtures for:
 * - User registration and login
 * - Token management
 * - Authenticated API requests
 */

import { test as base, expect, APIRequestContext, APIResponse } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Path to shared auth file created by global setup
const AUTH_FILE = path.join(__dirname, '..', '.auth.json');

interface SharedAuth {
  token: string;
  userId: number;
  username: string;
}

/**
 * Get shared auth from global setup if available
 */
export function getSharedAuth(): SharedAuth | null {
  try {
    if (fs.existsSync(AUTH_FILE)) {
      const data = fs.readFileSync(AUTH_FILE, 'utf-8');
      return JSON.parse(data) as SharedAuth;
    }
  } catch {
    // Ignore errors
  }
  return null;
}

// Test user credentials
export const TEST_USER = {
  username: `testuser_${Date.now()}`,
  email: `testuser_${Date.now()}@test.com`,
  password: 'TestPassword123!',
  password_confirm: 'TestPassword123!',
};

export const ADMIN_USER = {
  username: 'admin',
  password: 'admin',
};

// API base URL
export const API_BASE = '/api/v1';

/**
 * Response types for API endpoints
 */
export interface LoginResponse {
  token: string;
  user_id: number;
  username: string;
}

export interface RegisterResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
  };
}

export interface UserInfo {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

export interface Client {
  id: number;
  full_name: string;
  identification_number: string;
  email: string;
  phone: string;
  address?: string;
  is_active: boolean;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Case {
  id: number;
  client: number;
  case_number: string;
  title: string;
  description: string;
  case_type: string;
  status: string;
  priority: string;
  start_date: string;
  deadline?: string;
  closed_date?: string;
  assigned_to?: number;
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: number;
  case: number;
  case_number: string;
  title: string;
  document_type: string;
  description?: string;
  file: string;
  file_size: number;
  is_confidential: boolean;
  uploaded_by: number;
  uploaded_by_username: string;
  uploaded_at: string;
}

/**
 * Authentication helper class
 */
export class AuthHelper {
  public readonly request: APIRequestContext;
  private token: string | null = null;
  private userId: number | null = null;
  private username: string | null = null;

  constructor(request: APIRequestContext) {
    this.request = request;
  }

  /**
   * Use shared auth from global setup (avoids rate limits)
   * Returns true if shared auth was available and set
   */
  useSharedAuth(): boolean {
    const shared = getSharedAuth();
    if (shared) {
      this.token = shared.token;
      this.userId = shared.userId;
      this.username = shared.username;
      return true;
    }
    return false;
  }

  /**
   * Register a new user (may be rate limited)
   * Consider using useSharedAuth() first if you don't need a fresh user
   */
  async register(userData?: Partial<typeof TEST_USER>): Promise<RegisterResponse> {
    const data = {
      ...TEST_USER,
      username: `testuser_${Date.now()}_${Math.random().toString(36).substring(7)}`,
      email: `testuser_${Date.now()}_${Math.random().toString(36).substring(7)}@test.com`,
      ...userData,
    };
    // Ensure password_confirm matches password
    data.password_confirm = data.password;

    const response = await this.request.post(`${API_BASE}/auth/register/`, {
      data,
    });

    if (response.status() === 429) {
      // Rate limited - try to use shared auth
      const shared = getSharedAuth();
      if (shared) {
        this.token = shared.token;
        this.userId = shared.userId;
        this.username = shared.username;
        return {
          token: shared.token,
          user: {
            id: shared.userId,
            username: shared.username,
            email: `${shared.username}@test.com`,
          },
        };
      }
      throw new Error('Rate limited and no shared auth available');
    }

    expect(response.status()).toBe(201);
    const json = await response.json() as RegisterResponse;
    this.token = json.token;
    this.userId = json.user.id;
    this.username = json.user.username;
    return json;
  }

  /**
   * Login with credentials
   */
  async login(credentials: { username: string; password: string }): Promise<LoginResponse> {
    const response = await this.request.post(`${API_BASE}/auth/login/`, {
      data: credentials,
    });

    expect(response.status()).toBe(200);
    const json = await response.json() as LoginResponse;
    this.token = json.token;
    return json;
  }

  /**
   * Logout the current user
   */
  async logout(): Promise<void> {
    if (!this.token) {
      throw new Error('No token available for logout');
    }

    const response = await this.request.post(`${API_BASE}/auth/logout/`, {
      headers: this.getAuthHeaders(),
    });

    expect(response.status()).toBe(200);
    this.token = null;
  }

  /**
   * Get current user info
   */
  async getMe(): Promise<UserInfo> {
    if (!this.token) {
      throw new Error('No token available');
    }

    const response = await this.request.get(`${API_BASE}/auth/me/`, {
      headers: this.getAuthHeaders(),
    });

    expect(response.status()).toBe(200);
    return await response.json() as UserInfo;
  }

  /**
   * Get authorization headers
   */
  getAuthHeaders(): Record<string, string> {
    if (!this.token) {
      throw new Error('No token available');
    }
    return {
      'Authorization': `Token ${this.token}`,
    };
  }

  /**
   * Get the current token
   */
  getToken(): string | null {
    return this.token;
  }

  /**
   * Set the token manually
   */
  setToken(token: string): void {
    this.token = token;
  }

  /**
   * Make an authenticated GET request
   */
  async get(url: string): Promise<APIResponse> {
    return await this.request.get(url, {
      headers: this.getAuthHeaders(),
    });
  }

  /**
   * Make an authenticated POST request
   */
  async post(url: string, data?: object): Promise<APIResponse> {
    return await this.request.post(url, {
      headers: this.getAuthHeaders(),
      data,
    });
  }

  /**
   * Make an authenticated PUT request
   */
  async put(url: string, data: object): Promise<APIResponse> {
    return await this.request.put(url, {
      headers: this.getAuthHeaders(),
      data,
    });
  }

  /**
   * Make an authenticated PATCH request
   */
  async patch(url: string, data: object): Promise<APIResponse> {
    return await this.request.patch(url, {
      headers: this.getAuthHeaders(),
      data,
    });
  }

  /**
   * Make an authenticated DELETE request
   */
  async delete(url: string): Promise<APIResponse> {
    return await this.request.delete(url, {
      headers: this.getAuthHeaders(),
    });
  }

  /**
   * Upload a file with multipart form data
   */
  async uploadFile(
    url: string,
    file: Buffer,
    filename: string,
    additionalData?: Record<string, string | number | boolean>
  ): Promise<APIResponse> {
    const formData: Record<string, string | number | boolean | { name: string; mimeType: string; buffer: Buffer }> = {
      file: {
        name: filename,
        mimeType: this.getMimeType(filename),
        buffer: file,
      },
      ...additionalData,
    };

    return await this.request.post(url, {
      headers: {
        'Authorization': `Token ${this.token}`,
      },
      multipart: formData,
    });
  }

  /**
   * Get MIME type from filename
   */
  private getMimeType(filename: string): string {
    const ext = filename.toLowerCase().split('.').pop();
    const mimeTypes: Record<string, string> = {
      'pdf': 'application/pdf',
      'doc': 'application/msword',
      'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'txt': 'text/plain',
      'jpg': 'image/jpeg',
      'jpeg': 'image/jpeg',
      'png': 'image/png',
      'exe': 'application/octet-stream',
      'js': 'application/javascript',
    };
    return mimeTypes[ext || ''] || 'application/octet-stream';
  }
}

/**
 * Extended test fixture with authentication helper
 */
export const test = base.extend<{ auth: AuthHelper }>({
  auth: async ({ request }, use) => {
    const auth = new AuthHelper(request);
    await use(auth);
  },
});

export { expect };

/**
 * Generate unique test data
 */
export function generateTestClient(): Omit<Client, 'id' | 'created_at' | 'updated_at'> {
  const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
  return {
    full_name: `Test Client ${uniqueId}`,
    identification_number: `ID-${uniqueId}`,
    email: `client_${uniqueId}@test.com`,
    phone: '+1234567890',
    address: '123 Test Street',
    is_active: true,
    notes: 'Test client created by E2E tests',
  };
}

export function generateTestCase(clientId: number): Omit<Case, 'id' | 'case_number' | 'created_at' | 'updated_at'> {
  const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
  const today = new Date().toISOString().split('T')[0];
  const deadline = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  return {
    client: clientId,
    title: `Test Case ${uniqueId}`,
    description: 'Test case created by E2E tests',
    case_type: 'civil',
    status: 'en_proceso',
    priority: 'media',
    start_date: today,
    deadline: deadline,
  };
}

export function generateTestDocument(caseId: number): {
  case: number;
  title: string;
  document_type: string;
  description: string;
  is_confidential: boolean;
} {
  const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(7)}`;
  return {
    case: caseId,
    title: `Test Document ${uniqueId}`,
    document_type: 'contrato',
    description: 'Test document created by E2E tests',
    is_confidential: false,
  };
}

/**
 * Create a simple PDF file buffer for testing
 */
export function createTestPDF(): Buffer {
  // Minimal valid PDF content
  const pdfContent = `%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>
endobj
xref
0 4
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
trailer
<< /Size 4 /Root 1 0 R >>
startxref
191
%%EOF`;
  return Buffer.from(pdfContent, 'utf-8');
}

/**
 * Create a simple text file buffer for testing
 */
export function createTestTxt(): Buffer {
  return Buffer.from('This is a test text file for E2E testing.', 'utf-8');
}

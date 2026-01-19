/**
 * Module configuration for screenshot documentation.
 *
 * Defines all modules and their screenshot configurations for
 * consistent documentation generation.
 */

/**
 * Module definition with metadata
 */
export interface ModuleConfig {
  /** Unique module ID (used for directory name) */
  id: string;
  /** Human-readable module name */
  name: string;
  /** Module description for README */
  description: string;
  /** Expected number of screenshots */
  expectedScreenshots: number;
}

/**
 * All documentation modules in order
 */
export const MODULES: ModuleConfig[] = [
  {
    id: '01-auth',
    name: 'Authentication',
    description: 'User authentication flows including login, registration, and session management.',
    expectedScreenshots: 3,
  },
  {
    id: '02-clients',
    name: 'Client Management',
    description: 'CRUD operations for managing legal clients including listing, creation, and editing.',
    expectedScreenshots: 4,
  },
  {
    id: '03-cases',
    name: 'Case Management',
    description: 'Legal case lifecycle management including creation, status tracking, and closure.',
    expectedScreenshots: 5,
  },
  {
    id: '04-documents',
    name: 'Document Management',
    description: 'Document upload, storage, and management associated with legal cases.',
    expectedScreenshots: 3,
  },
  {
    id: '05-dashboard',
    name: 'Dashboard & Search',
    description: 'Overview dashboard with statistics and global search functionality.',
    expectedScreenshots: 2,
  },
  {
    id: '06-admin',
    name: 'Django Admin',
    description: 'Administrative interface for advanced data management and configuration.',
    expectedScreenshots: 4,
  },
  {
    id: '07-api',
    name: 'Swagger API',
    description: 'Interactive API documentation for developers using Swagger/OpenAPI.',
    expectedScreenshots: 3,
  },
];

/**
 * Get module by ID
 */
export function getModule(id: string): ModuleConfig | undefined {
  return MODULES.find(m => m.id === id);
}

/**
 * Get total expected screenshot count
 */
export function getTotalExpectedScreenshots(): number {
  return MODULES.reduce((sum, m) => sum + m.expectedScreenshots, 0);
}

/**
 * Application URLs for screenshot capture
 */
export const URLS = {
  // Swagger UI
  swagger: '/api/v1/docs/',
  swaggerAuth: '/api/v1/docs/#/auth',
  swaggerClients: '/api/v1/docs/#/clients',
  swaggerCases: '/api/v1/docs/#/cases',
  swaggerDocuments: '/api/v1/docs/#/documents',
  swaggerDashboard: '/api/v1/docs/#/dashboard',
  swaggerSearch: '/api/v1/docs/#/search',

  // Django Admin
  adminLogin: '/admin/login/',
  adminDashboard: '/admin/',
  adminClients: '/admin/clients/client/',
  adminCases: '/admin/cases/case/',
  adminDocuments: '/admin/documents/document/',

  // API Endpoints (for reference)
  apiAuth: '/api/v1/auth/',
  apiClients: '/api/v1/clients/',
  apiCases: '/api/v1/cases/',
  apiDocuments: '/api/v1/documents/',
  apiDashboard: '/api/v1/dashboard/',
  apiSearch: '/api/v1/search/',
};

/**
 * CSS selectors for waiting on page elements
 */
export const SELECTORS = {
  // Swagger UI elements
  swaggerLoaded: '.swagger-ui',
  swaggerOperation: '.opblock',
  swaggerOperationExpanded: '.opblock.is-open',
  swaggerTryItOut: '.try-out__btn',
  swaggerExecute: '.execute',
  swaggerResponse: '.responses-table',

  // Django Admin elements
  adminLoginForm: '#login-form',
  adminDashboard: '#content',
  adminModelList: '#changelist',
  adminChangeForm: '#content-main',

  // Common elements
  pageLoaded: 'body',
};

/**
 * Admin credentials from environment
 */
export const ADMIN_CREDENTIALS = {
  username: process.env.ADMIN_USERNAME || 'admin',
  password: process.env.ADMIN_PASSWORD || 'admin123',
};

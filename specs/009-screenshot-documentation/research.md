# Research: Screenshot Documentation for LegalDocs Manager

**Feature**: 009-screenshot-documentation
**Date**: 2026-01-19

## Existing Infrastructure Analysis

### Current E2E Test Structure

The project already has a comprehensive Playwright E2E test suite in `tests/e2e/`:

```
tests/e2e/
├── playwright.config.ts     # Configured for Chromium, 1280x720 implied
├── package.json             # @playwright/test ^1.40.0
├── fixtures/
│   └── auth.ts              # AuthHelper class with full API support
├── api/                     # 7 API test files (111 tests passing)
├── ui/                      # Swagger and Admin tests
└── workflows/               # Complete flow tests
```

### Key Findings from Existing Code

1. **Authentication Helper** (`fixtures/auth.ts`):
   - `AuthHelper` class handles registration, login, logout
   - Token-based authentication working
   - Methods: `register()`, `login()`, `get()`, `post()`, `uploadFile()`
   - Generates unique test data with `generateTestClient()`, `generateTestCase()`, `generateTestDocument()`

2. **Playwright Config** (`playwright.config.ts`):
   - Base URL: `http://localhost:8000`
   - Browser: Desktop Chrome (Chromium)
   - Screenshot on failure already enabled
   - Single worker to avoid rate limits
   - Projects: `api`, `ui`, `workflows`

3. **Admin Interface** (`ui/admin.spec.ts`):
   - Django admin at `/admin/`
   - Models: clients, cases, documents
   - Authentication separate from API

4. **Swagger UI** (`ui/swagger.spec.ts`):
   - Available at `/api/v1/docs/`
   - Interactive API documentation

### Application URLs to Document

Based on existing tests and Django routes:

| Module | URL | Auth Required |
|--------|-----|---------------|
| Login | `/api/v1/docs/` (Swagger has auth) | No |
| Register | `/api/v1/docs/` | No |
| Clients List | `/api/v1/clients/` | Yes (API) |
| Clients Create | `/api/v1/clients/` | Yes (API) |
| Cases List | `/api/v1/cases/` | Yes (API) |
| Cases Detail | `/api/v1/cases/{id}/` | Yes (API) |
| Documents | `/api/v1/documents/` | Yes (API) |
| Dashboard | `/api/v1/dashboard/` | Yes (API) |
| Search | `/api/v1/search/` | Yes (API) |
| Admin | `/admin/` | Yes (Django) |
| Swagger | `/api/v1/docs/` | No |

### Technical Approach

Since LegalDocs Manager is an **API-only** backend (no frontend UI), screenshots will focus on:

1. **Swagger UI** - Primary interface for API documentation
2. **Django Admin** - Backend management interface
3. **API Responses** - JSON rendered in browser or formatted output

### Screenshot Strategy

**Option A**: Swagger UI + Admin Only (Recommended)
- Capture Swagger UI showing all endpoints
- Capture Django Admin for all models
- Pros: Real visual documentation, what users actually see
- Cons: Limited to these two interfaces

**Option B**: API Response Screenshots
- Capture JSON responses formatted in browser
- Use browser dev tools or JSON viewer
- Pros: Shows actual API data
- Cons: Not visually appealing, JSON is text-based

**Decision**: Option A - Focus on Swagger UI and Django Admin as the visual interfaces. API responses can be included as code blocks in the README.

## Dependencies

### Already Available
- `@playwright/test` - Installed in `tests/e2e/`
- Chromium browser - Bundled with Playwright
- `AuthHelper` class - For API authentication
- Test data generators - For creating sample content

### No Additional Dependencies Needed
The existing E2E infrastructure provides everything required.

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Server not running | Script checks server health before starting |
| Rate limiting triggers | Use DISABLE_THROTTLING=1 env var |
| No test data | Create test data via API before screenshots |
| Admin credentials | Use env vars ADMIN_USERNAME/ADMIN_PASSWORD |
| Element not loaded | Use Playwright's auto-waiting and explicit waits |

## Implementation Approach

1. Create new Playwright test file in `tests/e2e/docs/`
2. Reuse existing `AuthHelper` for authentication
3. Create test data via API (client, case, document)
4. Navigate and screenshot Swagger UI sections
5. Navigate and screenshot Django Admin sections
6. Generate markdown README with image links
7. Clean up test data (optional)

## References

- Existing tests: `tests/e2e/ui/swagger.spec.ts`, `tests/e2e/ui/admin.spec.ts`
- Playwright screenshots: https://playwright.dev/docs/screenshots
- Playwright page.screenshot(): https://playwright.dev/docs/api/class-page#page-screenshot

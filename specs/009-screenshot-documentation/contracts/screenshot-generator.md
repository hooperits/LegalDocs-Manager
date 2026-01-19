# Contract: Screenshot Generator

**Feature**: 009-screenshot-documentation
**Date**: 2026-01-19

## Interface Definition

### Main Entry Point

```typescript
// tests/e2e/docs/generate-screenshots.spec.ts

import { test } from '@playwright/test';
import { AuthHelper } from '../fixtures/auth';

test.describe('Screenshot Documentation Generator', () => {
  // Configuration
  const SCREENSHOT_DIR = 'docs/screenshots';
  const VIEWPORT = { width: 1280, height: 720 };

  // Module tests generate screenshots
  test('01-auth: Authentication screens', async ({ page, request }) => {});
  test('02-clients: Client management screens', async ({ page, request }) => {});
  test('03-cases: Case management screens', async ({ page, request }) => {});
  test('04-documents: Document management screens', async ({ page, request }) => {});
  test('05-dashboard: Dashboard and search screens', async ({ page, request }) => {});
  test('06-admin: Django admin screens', async ({ page }) => {});
  test('07-api: Swagger API documentation screens', async ({ page }) => {});
  test('Generate README index', async () => {});
});
```

### Screenshot Helper Functions

```typescript
interface ScreenshotOptions {
  name: string;           // Screenshot filename (without extension)
  module: string;         // Module directory name
  description: string;    // Description for README
  fullPage?: boolean;     // Capture full page (default: false)
  waitFor?: string;       // CSS selector to wait for before capture
}

async function captureScreenshot(
  page: Page,
  options: ScreenshotOptions
): Promise<void>;

async function ensureDirectory(path: string): Promise<void>;

function generateReadme(modules: ModuleInfo[]): string;
```

### Module Configuration

```typescript
interface ModuleConfig {
  id: string;
  name: string;
  description: string;
  screens: ScreenConfig[];
}

interface ScreenConfig {
  order: number;
  name: string;
  url: string;
  description: string;
  requiresAuth: boolean;
  waitFor?: string;
  actions?: PageAction[];
}

interface PageAction {
  type: 'click' | 'fill' | 'wait' | 'scroll';
  selector?: string;
  value?: string;
  timeout?: number;
}
```

## Expected Outputs

### Screenshot Files

- Location: `docs/screenshots/{module}/{order}-{name}.png`
- Format: PNG, 1280x720 pixels
- Naming: Zero-padded order, kebab-case name

### README.md

```markdown
# LegalDocs Manager - Visual Documentation

Generated: {ISO timestamp}

## Table of Contents

1. [Authentication](#authentication)
2. [Client Management](#client-management)
...

## Authentication

Screenshots demonstrating the authentication flow.

### Login Page
![Login Page](./01-auth/01-login-page.png)

Description of the login interface.

### Register Form
![Register Form](./01-auth/02-register-form.png)
...
```

## Execution Contract

### Prerequisites
- Django server running at `http://localhost:8000`
- Admin user exists with known credentials
- `DISABLE_THROTTLING=1` environment variable set
- Playwright and Chromium installed

### Invocation

```bash
cd tests/e2e
npx playwright test docs/generate-screenshots.spec.ts
```

### Success Criteria
- Exit code 0
- All screenshots exist in `docs/screenshots/`
- README.md generated with valid image links
- No broken image references

### Failure Modes
- Server unavailable: Exit with error, no partial output
- Auth failure: Exit with error, log credentials issue
- Element not found: Skip screenshot, log warning, continue
- Permission denied: Exit with error, log path issue

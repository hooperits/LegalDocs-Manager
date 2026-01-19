# LegalDocs-Manager E2E Tests

End-to-end tests for the LegalDocs-Manager API using Playwright with Chromium.

## Setup

```bash
cd tests/e2e
npm install
npx playwright install chromium
```

## Running Tests

### Start the Django server first

```bash
cd legaldocs
source ../venv/bin/activate
python manage.py runserver
```

### Run all tests

```bash
npx playwright test
```

### Run specific test categories

```bash
# API tests only
npx playwright test api/

# UI tests only
npx playwright test ui/

# Workflow tests only
npx playwright test workflows/
```

### Debug mode

```bash
npx playwright test --ui
```

### View HTML report

```bash
npx playwright show-report
```

## Rate Limiting Considerations

The Django API has rate limiting enabled:
- **5 requests/minute** on `/auth/login/` and `/auth/register/`

This affects E2E tests because many tests need to register users. To work around this:

1. **Run tests with single worker** (default in config):
   ```bash
   npx playwright test --workers=1
   ```

2. **Run small subsets of tests**:
   ```bash
   npx playwright test -g "should register"
   ```

3. **Wait between test runs** if you hit rate limits (wait ~60 seconds)

4. **For CI/CD**, consider:
   - Increasing rate limits in test settings
   - Using a pre-created test user
   - Running tests in batches with delays

## Test Structure

```
tests/e2e/
├── playwright.config.ts     # Playwright configuration
├── global-setup.ts          # Creates shared test user
├── fixtures/
│   └── auth.ts              # Auth helpers and test fixtures
├── api/
│   ├── auth.spec.ts         # Authentication tests
│   ├── clients.spec.ts      # Clients CRUD tests
│   ├── cases.spec.ts        # Cases CRUD tests
│   ├── documents.spec.ts    # Documents upload tests
│   ├── dashboard.spec.ts    # Dashboard statistics tests
│   ├── search.spec.ts       # Global search tests
│   └── security.spec.ts     # Security tests (rate limiting skipped)
├── ui/
│   ├── swagger.spec.ts      # Swagger UI tests
│   └── admin.spec.ts        # Django Admin tests
└── workflows/
    └── complete-flow.spec.ts # End-to-end workflow tests
```

## Test Count

- **132 total tests** (3 skipped - rate limiting tests)
- **API tests**: 91 tests
- **UI tests**: 37 tests
- **Workflow tests**: 4 tests

## Environment Variables

- `BASE_URL`: API base URL (default: `http://localhost:8000`)
- `ADMIN_USERNAME`: Django admin username (default: `admin`)
- `ADMIN_PASSWORD`: Django admin password (default: `admin`)

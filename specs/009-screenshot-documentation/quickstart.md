# Quickstart: Screenshot Documentation Generator

**Feature**: 009-screenshot-documentation
**Date**: 2026-01-19

## Prerequisites

1. **Django Server Running**
   ```bash
   cd legaldocs
   python manage.py runserver
   ```

2. **Admin User Created**
   ```bash
   python manage.py createsuperuser
   # Or reset password for existing:
   python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='admin'); u.set_password('admin123'); u.save()"
   ```

3. **Playwright Installed**
   ```bash
   cd tests/e2e
   npm install
   npx playwright install chromium
   ```

## Environment Variables

Create or update `tests/e2e/.env`:

```env
BASE_URL=http://localhost:8000
DISABLE_THROTTLING=1
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

## Running the Documentation Generator

### Full Documentation

```bash
cd tests/e2e
npx playwright test docs/generate-screenshots.spec.ts
```

### Specific Module Only

```bash
# Only authentication screenshots
npx playwright test docs/generate-screenshots.spec.ts -g "01-auth"

# Only admin screenshots
npx playwright test docs/generate-screenshots.spec.ts -g "06-admin"
```

### With Visual Browser (Debug)

```bash
npx playwright test docs/generate-screenshots.spec.ts --headed
```

## Output Location

Screenshots are saved to:
```
docs/screenshots/
├── README.md           # Index with all screenshots
├── 01-auth/           # Authentication screens
├── 02-clients/        # Client management
├── 03-cases/          # Case management
├── 04-documents/      # Document management
├── 05-dashboard/      # Dashboard and search
├── 06-admin/          # Django admin
└── 07-api/            # Swagger documentation
```

## Viewing the Documentation

After generation:

1. **Local Preview**
   - Open `docs/screenshots/README.md` in VS Code with Markdown preview
   - Or use: `npx serve docs/screenshots`

2. **GitHub**
   - Push to repository
   - Navigate to `docs/screenshots/README.md` on GitHub
   - Images render inline automatically

## Troubleshooting

### Server Not Available
```
Error: net::ERR_CONNECTION_REFUSED
```
**Fix**: Start Django server with `python manage.py runserver`

### Rate Limiting (429 Error)
```
Error: 429 Too Many Requests
```
**Fix**: Set `DISABLE_THROTTLING=1` in environment

### Admin Login Fails
```
Error: Could not login to admin
```
**Fix**: Verify ADMIN_USERNAME and ADMIN_PASSWORD in .env

### Element Not Found
```
Error: Timeout waiting for selector
```
**Fix**: Ensure page is fully loaded, check if UI changed

## Regenerating Documentation

To update screenshots after UI changes:

```bash
# Delete existing screenshots
rm -rf docs/screenshots/*

# Regenerate all
cd tests/e2e
npx playwright test docs/generate-screenshots.spec.ts
```

## Integration with CI

Add to `.github/workflows/docs.yml`:

```yaml
name: Generate Documentation
on:
  workflow_dispatch:
  push:
    branches: [master]
    paths:
      - 'legaldocs/**/*.html'
      - 'legaldocs/**/*.css'

jobs:
  screenshots:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          cd tests/e2e && npm ci && npx playwright install chromium

      - name: Start Django server
        run: |
          cd legaldocs
          python manage.py migrate
          python manage.py runserver &
          sleep 5
        env:
          DISABLE_THROTTLING: 1

      - name: Generate screenshots
        run: |
          cd tests/e2e
          npx playwright test docs/generate-screenshots.spec.ts
        env:
          DISABLE_THROTTLING: 1
          ADMIN_USERNAME: admin
          ADMIN_PASSWORD: admin123

      - name: Commit screenshots
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add docs/screenshots/
          git commit -m "docs: actualizar screenshots" || exit 0
          git push
```

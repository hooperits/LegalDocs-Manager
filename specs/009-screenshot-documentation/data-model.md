# Data Model: Screenshot Documentation

**Feature**: 009-screenshot-documentation
**Date**: 2026-01-19

## Overview

This feature does not introduce new database models. It generates static files (PNG images and Markdown) as documentation artifacts.

## Output Artifacts

### Screenshot Files

```typescript
interface Screenshot {
  filename: string;        // e.g., "01-login-page.png"
  module: string;          // e.g., "01-auth"
  description: string;     // Human-readable description
  order: number;           // Display order within module
  path: string;            // Relative path from docs/screenshots/
}
```

### Module Structure

```typescript
interface Module {
  id: string;              // e.g., "01-auth"
  name: string;            // e.g., "Authentication"
  description: string;     // Module description for README
  screenshots: Screenshot[];
}
```

### Generated Index

```typescript
interface DocumentationIndex {
  title: string;           // "LegalDocs Manager - Visual Documentation"
  generatedAt: string;     // ISO timestamp
  modules: Module[];
  totalScreenshots: number;
}
```

## Screenshot Specifications

| Property | Value |
|----------|-------|
| Format | PNG |
| Resolution | 1280 x 720 pixels |
| Color Depth | 24-bit (RGB) |
| Naming | `{order}-{slug}.png` |

## Module Definitions

| ID | Name | Description | Expected Screenshots |
|----|------|-------------|---------------------|
| 01-auth | Authentication | Login, registration, and user session | 3 |
| 02-clients | Client Management | CRUD operations for clients | 3-4 |
| 03-cases | Case Management | Legal case lifecycle | 4-5 |
| 04-documents | Document Management | File upload and management | 3 |
| 05-dashboard | Dashboard & Search | Statistics and global search | 2 |
| 06-admin | Django Admin | Backend administration | 3-4 |
| 07-api | Swagger API | API documentation interface | 2-3 |

## Test Data Requirements

To generate meaningful screenshots, temporary test data must be created:

```typescript
interface TestDataSet {
  user: {
    username: string;
    password: string;
    token: string;
  };
  client: {
    id: number;
    full_name: string;
    // ... other fields
  };
  case: {
    id: number;
    case_number: string;
    title: string;
    // ... other fields
  };
  document: {
    id: number;
    title: string;
    file: string;
    // ... other fields
  };
}
```

## File System Layout

```
docs/screenshots/
├── README.md                    # Auto-generated index
├── 01-auth/
│   ├── 01-login-page.png
│   ├── 02-register-form.png
│   └── 03-user-menu.png
├── 02-clients/
│   ├── 01-client-list.png
│   ├── 02-client-create.png
│   ├── 03-client-detail.png
│   └── 04-client-edit.png
├── 03-cases/
│   ├── 01-case-list.png
│   ├── 02-case-create.png
│   ├── 03-case-detail.png
│   ├── 04-case-status.png
│   └── 05-case-close.png
├── 04-documents/
│   ├── 01-document-list.png
│   ├── 02-document-upload.png
│   └── 03-document-detail.png
├── 05-dashboard/
│   ├── 01-dashboard-overview.png
│   └── 02-search-results.png
├── 06-admin/
│   ├── 01-admin-login.png
│   ├── 02-admin-dashboard.png
│   ├── 03-admin-clients.png
│   └── 04-admin-cases.png
└── 07-api/
    ├── 01-swagger-overview.png
    ├── 02-swagger-auth.png
    └── 03-swagger-endpoint.png
```

## No Database Migrations Required

This feature operates entirely at the file system level and does not require any Django model changes or database migrations.

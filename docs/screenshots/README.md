# LegalDocs Manager - Visual Documentation

> Auto-generated documentation with screenshots of all application interfaces.

**Generated**: 2026-01-19T21:27:42.331Z

## Table of Contents

- [Authentication](#authentication)
- [Client Management](#client-management)
- [Case Management](#case-management)
- [Document Management](#document-management)
- [Dashboard & Search](#dashboard-search)
- [Django Admin](#django-admin)
- [Swagger API](#swagger-api)

---

## Authentication

User authentication flows including login, registration, and session management.

### Auth Endpoints Overview

Overview of authentication endpoints in Swagger UI, showing login, register, logout, and user info operations.

![Auth Endpoints Overview](./01-auth/01-auth-endpoints-overview.png)

### Login Endpoint

Login endpoint details showing required parameters (username, password) and response format.

![Login Endpoint](./01-auth/02-login-endpoint.png)

### Register Endpoint

Registration endpoint showing required fields for creating a new user account.

![Register Endpoint](./01-auth/03-register-endpoint.png)

---

## Client Management

CRUD operations for managing legal clients including listing, creation, and editing.

### Clients Endpoints Overview

Overview of client management endpoints showing CRUD operations available.

![Clients Endpoints Overview](./02-clients/01-clients-endpoints-overview.png)

### Client List Endpoint

Client list endpoint with filtering and pagination parameters.

![Client List Endpoint](./02-clients/02-client-list-endpoint.png)

### Client Create Endpoint

Client creation endpoint showing required and optional fields.

![Client Create Endpoint](./02-clients/03-client-create-endpoint.png)

### Client Detail Endpoint

Client detail endpoint for retrieving individual client information.

![Client Detail Endpoint](./02-clients/04-client-detail-endpoint.png)

---

## Case Management

Legal case lifecycle management including creation, status tracking, and closure.

### Cases Endpoints Overview

Overview of case management endpoints showing all available operations.

![Cases Endpoints Overview](./03-cases/01-cases-endpoints-overview.png)

### Case List Filters

Case list endpoint with filtering options for status, type, priority, and client.

![Case List Filters](./03-cases/02-case-list-filters.png)

### Case Create Endpoint

Case creation endpoint showing required fields including client association.

![Case Create Endpoint](./03-cases/03-case-create-endpoint.png)

### Case Statistics Endpoint

Case statistics endpoint providing summary counts by status, type, and priority.

![Case Statistics Endpoint](./03-cases/04-case-statistics-endpoint.png)

### Case Close Action

Case close action endpoint for marking a case as completed.

![Case Close Action](./03-cases/05-case-close-action.png)

---

## Document Management

Document upload, storage, and management associated with legal cases.

### Documents Endpoints Overview

Overview of document management endpoints for file upload and management.

![Documents Endpoints Overview](./04-documents/01-documents-endpoints-overview.png)

### Document List Endpoint

Document list endpoint with filtering by case and document type.

![Document List Endpoint](./04-documents/02-document-list-endpoint.png)

### Document Upload Endpoint

Document upload endpoint showing multipart file upload parameters.

![Document Upload Endpoint](./04-documents/03-document-upload-endpoint.png)

---

## Dashboard & Search

Overview dashboard with statistics and global search functionality.

### Dashboard Endpoint

Dashboard endpoint providing aggregated statistics and recent activity.

![Dashboard Endpoint](./05-dashboard/01-dashboard-endpoint.png)

### Search Endpoint

Global search endpoint for finding clients, cases, and documents.

![Search Endpoint](./05-dashboard/02-search-endpoint.png)

---

## Django Admin

Administrative interface for advanced data management and configuration.

### Admin Login

Django admin login page for administrative access.

![Admin Login](./06-admin/01-admin-login.png)

### Admin Dashboard

Django admin dashboard showing all registered models and management options.

![Admin Dashboard](./06-admin/02-admin-dashboard.png)

### Admin Clients List

Client management in Django admin with list display and filters.

![Admin Clients List](./06-admin/03-admin-clients-list.png)

### Admin Cases List

Case management in Django admin with status badges and filtering.

![Admin Cases List](./06-admin/04-admin-cases-list.png)

---

## Swagger API

Interactive API documentation for developers using Swagger/OpenAPI.

### Swagger Overview

Complete Swagger UI overview showing all available API endpoints organized by category.

![Swagger Overview](./07-api/01-swagger-overview.png)

### Swagger Header

API information header showing version, description, and base URL.

![Swagger Header](./07-api/02-swagger-header.png)

### Swagger Try It Out

Swagger interactive "Try it out" feature for testing API endpoints directly.

![Swagger Try It Out](./07-api/03-swagger-try-it-out.png)

---

---

## About This Documentation

This visual documentation was automatically generated using [Playwright](https://playwright.dev/)
to capture screenshots of the LegalDocs Manager application.

### Regenerating Screenshots

```bash
cd tests/e2e
DISABLE_THROTTLING=1 npx playwright test docs/generate-screenshots.spec.ts
```

### Requirements

- Django server running at `http://localhost:8000`
- Admin user with known credentials
- `DISABLE_THROTTLING=1` environment variable set

---

*Generated by LegalDocs Manager Screenshot Documentation System*

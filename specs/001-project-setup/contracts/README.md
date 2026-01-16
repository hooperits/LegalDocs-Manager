# API Contracts: Project Setup

**Feature**: 001-project-setup
**Status**: N/A

## Overview

This feature focuses on project initialization and does not define custom API endpoints.

## Built-in Endpoints Available After Setup

Once the project is set up, the following Django/DRF built-in endpoints will be available:

### Django Admin

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/` | GET | Django Admin interface |
| `/admin/login/` | GET, POST | Admin login |
| `/admin/logout/` | GET, POST | Admin logout |

### DRF Authentication (to be wired in urls.py)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api-auth/login/` | GET, POST | DRF browsable API login |
| `/api-auth/logout/` | GET, POST | DRF browsable API logout |

### Token Authentication (to be created in future feature)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/token/` | POST | Obtain auth token |

## Custom API Contracts

Custom API endpoints will be defined in subsequent features:

- `002-core-models`: Base model and shared utilities
- `003-user-management`: User registration, authentication
- `004-client-management`: Client CRUD operations
- `005-case-management`: Case CRUD operations
- `006-document-management`: Document upload and management

Each feature will have its own OpenAPI specification in its contracts directory.

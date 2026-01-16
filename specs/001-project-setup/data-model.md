# Data Model: Project Setup

**Feature**: 001-project-setup
**Date**: 2026-01-16
**Status**: Complete

## Overview

This feature establishes the project structure and configuration. No custom models are created in this phase - only the Django apps and the foundation for future models.

## App Structure (Entities Placeholder)

The following apps are created with empty models, ready for future development:

### core

**Purpose**: Shared utilities, base classes, and cross-cutting concerns.

**Future Models**:
- `BaseModel`: Abstract model with `created_at`, `updated_at` timestamps (to be created in next feature)

```python
# core/models.py - Structure only, implementation in future feature
class BaseModel(models.Model):
    """
    Abstract base model providing timestamp fields for all models.
    All other models should inherit from this.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### users

**Purpose**: Custom user model and authentication.

**Future Models**:
- `User`: Custom user model extending Django's AbstractUser
- User roles and permissions

### clients

**Purpose**: Client/customer management for the legal practice.

**Future Models**:
- `Client`: Legal client entity with contact information
- `ClientContact`: Additional contacts for a client

### cases

**Purpose**: Legal case/matter management.

**Future Models**:
- `Case`: Legal case/matter
- `CaseNote`: Notes and updates on a case
- `CaseStatus`: Status tracking

### documents

**Purpose**: Document upload and management.

**Future Models**:
- `Document`: Uploaded legal document
- `DocumentCategory`: Document classification
- `DocumentVersion`: Version tracking for documents

## Entity Relationships (Planned)

```
┌─────────────┐     ┌─────────────┐
│   Client    │────<│    Case     │
└─────────────┘     └─────────────┘
                           │
                           │
                    ┌──────┴──────┐
                    │  Document   │
                    └─────────────┘
```

- A Client has many Cases (one-to-many)
- A Case has many Documents (one-to-many)
- Users can be assigned to Cases (many-to-many, future)

## Database Configuration

### PostgreSQL Setup

```sql
-- Database creation (run as postgres superuser)
CREATE DATABASE legaldocs_db;
CREATE USER legaldocs_user WITH PASSWORD 'your-secure-password';
ALTER ROLE legaldocs_user SET client_encoding TO 'utf8';
ALTER ROLE legaldocs_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE legaldocs_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE legaldocs_db TO legaldocs_user;

-- For Django 5.x / PostgreSQL 15+, also grant schema permissions
\c legaldocs_db
GRANT ALL ON SCHEMA public TO legaldocs_user;
```

### Django Database Configuration

```python
# legaldocs/legaldocs/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'legaldocs_db'),
        'USER': os.getenv('DB_USER', 'legaldocs_user'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## Initial Migrations

This feature only runs Django's built-in migrations:

1. `django.contrib.admin` - Admin site
2. `django.contrib.auth` - Authentication framework (User, Group, Permission)
3. `django.contrib.contenttypes` - Content type framework
4. `django.contrib.sessions` - Session framework
5. `rest_framework.authtoken` - DRF token authentication

No custom app migrations are created until models are defined in subsequent features.

## Validation Rules

N/A for project setup. Validation rules will be defined when models are created.

## State Transitions

N/A for project setup. State machines will be defined for Case and Document entities in future features.

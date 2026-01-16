# Implementation Plan: Authentication and Dashboard Views

**Branch**: `005-auth-dashboard` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-auth-dashboard/spec.md`

## Summary

Implement complete authentication flows (login, logout, registration, user info), a dashboard statistics endpoint with optimized queries, a global search endpoint across all models, and user profile management. All endpoints use DRF with existing TokenAuthentication and require comprehensive test coverage.

## Technical Context

**Language/Version**: Python 3.11+ + Django 5.x
**Primary Dependencies**: Django REST Framework 3.15+, rest_framework.authtoken (already installed)
**Storage**: PostgreSQL 15+ (existing database with Client, Case, Document models)
**Testing**: Django TestCase, DRF APITestCase
**Target Platform**: Web API (Linux server)
**Project Type**: Django web application (existing structure)
**Performance Goals**: Dashboard queries < 100ms with proper indexing
**Constraints**: Use optimized queries (annotate, select_related, prefetch_related)
**Scale/Scope**: POC - up to 1000 clients, 5000 cases, 10000 documents

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Django Best Practices First | PASS | Using DRF built-in ObtainAuthToken, Django ORM aggregations |
| Clean Architecture | PASS | All views in api/ app, no circular imports |
| API-First Design | PASS | RESTful endpoints with proper HTTP methods and status codes |
| Documentation is Mandatory | PASS | Docstrings, type hints, API schema via drf-spectacular |
| Security by Default | PASS | Token auth, permission checks, input validation |

**Gate Status**: PASS - No violations. Proceeding with Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/005-auth-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── openapi.yaml
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```text
legaldocs/
├── api/
│   ├── views.py          # Auth views, DashboardView, SearchView, ProfileView
│   ├── serializers.py    # Auth, profile, search serializers
│   ├── urls.py           # Route configuration
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_dashboard.py
│       ├── test_search.py
│       └── test_profile.py
├── clients/              # Existing - queried by dashboard/search
├── cases/                # Existing - queried by dashboard/search
└── documents/            # Existing - queried by dashboard/search
```

**Structure Decision**: Extend existing `api/` app with new views and serializers. Create `tests/` subdirectory within `api/` for organized test files.

## Complexity Tracking

No violations to justify - design follows constitution principles.

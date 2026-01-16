# Implementation Plan: Django REST Framework API

**Branch**: `004-rest-api` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-rest-api/spec.md`

## Summary

Build a complete RESTful API for the LegalDocs Manager using Django REST Framework. The API will provide CRUD operations for clients, cases, and documents with proper authentication (Token + Session), pagination (20 items), filtering, search, ordering, and custom actions. Includes OpenAPI schema generation and Swagger UI documentation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Django 5.x, Django REST Framework 3.15+, django-filter, drf-spectacular, django-cors-headers
**Storage**: PostgreSQL 15+ (existing database with Client, Case, Document models)
**Testing**: Django TestCase, DRF APITestCase
**Target Platform**: Linux server (development on any platform)
**Project Type**: Web application (Django backend, API-only for this feature)
**Performance Goals**: API responses within 500ms for list operations
**Constraints**: File uploads limited to 10MB, pagination at 20 items per page
**Scale/Scope**: POC scope - focusing on core CRUD and custom actions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Django Best Practices First | ✅ PASS | Using DRF's built-in features (viewsets, serializers, routers) |
| II. Clean Architecture | ✅ PASS | Serializers/views in their respective apps, permissions in api/ app |
| III. API-First Design | ✅ PASS | This feature implements the API layer per constitution |
| IV. Documentation Mandatory | ✅ PASS | OpenAPI schema + Swagger UI + docstrings required |
| V. Security by Default | ✅ PASS | Token auth, permissions, file validation specified |

**Constitution Alignment**:
- Uses DRF TokenAuthentication as specified in constitution
- Follows app-per-domain structure (serializers/views in clients/, cases/, documents/)
- API app (`api/`) contains only shared concerns (permissions, URLs)
- All endpoints require authentication per security standards

## Project Structure

### Documentation (this feature)

```text
specs/004-rest-api/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (API structure, not DB models)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
legaldocs/
├── legaldocs/
│   ├── settings.py      # Add REST_FRAMEWORK, CORS settings
│   └── urls.py          # Add api/v1/ include
├── api/                 # NEW - API configuration app
│   ├── __init__.py
│   ├── urls.py          # Router registration, auth endpoint
│   └── permissions.py   # Custom permissions
├── clients/
│   ├── serializers.py   # NEW - ClientSerializer, ClientDetailSerializer
│   └── views.py         # NEW - ClientViewSet
├── cases/
│   ├── serializers.py   # NEW - CaseSerializer, CaseDetailSerializer
│   └── views.py         # NEW - CaseViewSet
└── documents/
    ├── serializers.py   # NEW - DocumentSerializer
    └── views.py         # NEW - DocumentViewSet
```

**Structure Decision**: Following Django convention with serializers and views in each domain app. New `api/` app created for shared API concerns (permissions, URL routing) to avoid circular imports and keep clean separation.

## Complexity Tracking

> No violations detected. Feature follows constitution guidelines.

| Aspect | Assessment |
|--------|------------|
| New dependencies | Standard DRF ecosystem (django-filter, drf-spectacular, django-cors-headers) |
| Architecture | Extends existing app structure, no new patterns |
| Cross-app imports | DocumentSerializer imported in CaseDetailSerializer (allowed at serializer level per constitution) |

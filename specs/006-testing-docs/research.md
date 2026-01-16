# Research: Testing and Documentation

**Feature**: 006-testing-docs
**Date**: 2026-01-16

## Executive Summary

This feature focuses on testing and documentation for an existing Django REST Framework application. The codebase has well-structured models (Client, Case, Document), serializers, and ViewSets. Existing tests in `api/tests/` cover authentication, dashboard, search, and profile endpoints (40 tests). This feature will add model-level tests, serializer tests, ViewSet tests, integration tests, and comprehensive documentation.

---

## Research Findings

### 1. Testing Framework Selection

**Decision**: Use Django's TestCase + DRF's APITestCase + coverage.py

**Rationale**:
- Already established in the project (api/tests/ uses APITestCase)
- Constitution mandates Django TestCase for models and APITestCase for endpoints
- coverage.py is the standard for Python code coverage measurement
- No additional dependencies needed (coverage.py just needs to be installed)

**Alternatives Considered**:
- pytest-django: More features but adds complexity; standard Django test runner is sufficient
- Factory Boy: Useful for complex test data but not needed given fixture approach already in use
- model_bakery: Similar reasoning; manual test data creation is sufficient for this scope

### 2. Test Organization Strategy

**Decision**: Per-app tests/ directory structure

**Rationale**:
- Aligns with Django conventions
- Constitution specifies "Test each component before moving to the next"
- Keeps tests close to the code they test
- Allows running tests per-app: `python manage.py test clients`

**Structure**:
```
legaldocs/
├── clients/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       └── test_views.py
├── cases/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       └── test_views.py
├── documents/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       └── test_views.py
└── api/
    └── tests/
        ├── __init__.py
        ├── test_auth.py (existing)
        ├── test_dashboard.py (existing)
        ├── test_search.py (existing)
        ├── test_profile.py (existing)
        └── test_integration.py (new)
```

### 3. Code Coverage Strategy

**Decision**: Target 70% overall, 80% for models/serializers

**Rationale**:
- 70% is a practical target for a POC/MVP
- Models and serializers are critical and easier to test exhaustively
- Views have more edge cases; 70% is reasonable
- Constitution emphasizes testing but doesn't specify coverage percentages

**Implementation**:
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # For detailed HTML report
```

### 4. Existing Test Analysis

**Current State**:
- 40 tests in `api/tests/` covering auth, dashboard, search, profile
- Tests use `APITestCase` and token authentication
- SQLite used for test database (configured in settings.py)

**What's Missing**:
- Model tests (Client, Case, Document) - creation, validation, methods
- Serializer tests - valid/invalid data, computed fields
- ViewSet tests - CRUD operations, custom actions, permissions
- Integration tests - end-to-end workflows
- File upload tests for documents

### 5. Demo Data Strategy

**Decision**: JSON fixtures + management command

**Rationale**:
- Django's built-in fixture system is simple and reliable
- Management command provides easy one-step loading
- JSON format is human-readable and editable
- Constitution specifies "fixtures for demo data in fixtures/ directory"

**Data Requirements**:
- 20+ clients with Spanish names and varied data
- 30+ cases across all types and statuses
- 50+ documents with different types
- Realistic dates spanning past 2 years

### 6. Documentation Format

**Decision**: Markdown files in repository root

**Rationale**:
- README.md is standard and expected by all developers
- API_DOCS.md separates API details from general documentation
- DEPLOYMENT.md focuses on production concerns
- Markdown renders well on GitHub and is version-controlled

**Structure**:
- README.md: Installation, setup, quick start
- API_DOCS.md: Complete endpoint reference
- DEPLOYMENT.md: Production deployment guide

### 7. API Documentation Approach

**Decision**: Manual markdown + reference to OpenAPI/Swagger

**Rationale**:
- drf-spectacular already generates OpenAPI schema at `/api/v1/schema/`
- Swagger UI available at `/api/v1/docs/`
- Manual markdown provides copy-paste examples
- Covers both automated and human-readable documentation

---

## Technical Decisions Summary

| Area | Decision | Rationale |
|------|----------|-----------|
| Test Framework | Django TestCase + DRF APITestCase | Established pattern, constitution compliance |
| Coverage Tool | coverage.py | Standard, no dependencies |
| Coverage Target | 70% overall, 80% models | Practical for POC scope |
| Test Structure | Per-app tests/ directories | Django convention, isolation |
| Demo Data | JSON fixtures + mgmt command | Built-in, constitution compliance |
| Docs Format | Markdown (README, API_DOCS, DEPLOYMENT) | Standard, version-controlled |
| API Docs | Manual + OpenAPI reference | Best of both worlds |

---

## Dependencies

**New Dependencies**:
- coverage (for code coverage measurement)

**Existing Dependencies Used**:
- Django TestCase
- DRF APITestCase
- drf-spectacular (already configured for OpenAPI)

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| File upload tests require temp files | Use Django's SimpleUploadedFile for in-memory files |
| Coverage may reveal untested code paths | Focus on critical paths first, then edge cases |
| Demo data may have foreign key issues | Use loaddata order: clients → cases → documents |
| Tests may be slow | Use SQLite in-memory (already configured), parallel test runner |

---

## Open Questions (Resolved)

1. **Q**: Should we use pytest or Django's test runner?
   **A**: Django's test runner - already established, simpler setup

2. **Q**: Should fixtures use natural keys?
   **A**: No - use explicit IDs for clarity and relationship management

3. **Q**: Should demo data include real-looking ID numbers?
   **A**: Use fictional but format-correct IDs (e.g., "12345678-A")

# Tasks: Testing and Documentation

**Input**: Design documents from `/specs/006-testing-docs/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

## Task Overview

| Phase | Tasks | Focus |
|-------|-------|-------|
| 1. Setup | 4 | Add coverage, create test directories |
| 2. Foundational | 2 | Verify existing tests work |
| 3. US1 - Unit Tests | 12 | Model, serializer, ViewSet tests |
| 4. US3 - README | 2 | Project documentation |
| 5. US4 - API Docs | 2 | API reference documentation |
| 6. US2 - Integration | 2 | End-to-end workflow tests |
| 7. US5 - Demo Data | 5 | Fixtures and management command |
| 8. US6 - Deployment | 2 | Deployment documentation |
| 9. Validation | 3 | Coverage check, final verification |

**Total Tasks**: 34

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Add coverage dependency and create test directory structure

- [x] T001 Add coverage to requirements.txt in legaldocs/requirements.txt
- [x] T002 [P] Create clients/tests/ directory with __init__.py in legaldocs/clients/tests/__init__.py
- [x] T003 [P] Create cases/tests/ directory with __init__.py in legaldocs/cases/tests/__init__.py
- [x] T004 [P] Create documents/tests/ directory with __init__.py in legaldocs/documents/tests/__init__.py

**Checkpoint**: Test directory structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify existing tests and infrastructure work

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Run existing api/tests/ to verify test infrastructure works
- [x] T006 Verify SQLite test database configuration in legaldocs/legaldocs/settings.py

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Unit Tests (Priority: P1) 🎯 MVP

**Goal**: Comprehensive unit tests for models, serializers, and ViewSets with 70%+ coverage

**Independent Test**: `python manage.py test clients cases documents` passes; `coverage report` shows ≥70%

### Model Tests (US1)

- [x] T007 [P] [US1] Create Client model tests in legaldocs/clients/tests/test_models.py
- [x] T008 [P] [US1] Create Case model tests (incl. manager, case_number generation) in legaldocs/cases/tests/test_models.py
- [x] T009 [P] [US1] Create Document model tests (incl. file_size calculation) in legaldocs/documents/tests/test_models.py

### Serializer Tests (US1)

- [x] T010 [P] [US1] Create Client serializer tests in legaldocs/clients/tests/test_serializers.py
- [x] T011 [P] [US1] Create Case serializer tests in legaldocs/cases/tests/test_serializers.py
- [x] T012 [P] [US1] Create Document serializer tests in legaldocs/documents/tests/test_serializers.py

### ViewSet Tests (US1)

- [x] T013 [P] [US1] Create ClientViewSet tests (CRUD, filters, search, custom action) in legaldocs/clients/tests/test_views.py
- [x] T014 [P] [US1] Create CaseViewSet tests (CRUD, filters, close action, statistics) in legaldocs/cases/tests/test_views.py
- [x] T015 [P] [US1] Create DocumentViewSet tests (CRUD, file upload, permissions) in legaldocs/documents/tests/test_views.py

### Permission Tests (US1)

- [x] T016 [US1] Add unauthenticated access tests to all ViewSet test files
- [x] T017 [US1] Add IsOwnerOrReadOnly permission tests in legaldocs/documents/tests/test_views.py
- [x] T018 [US1] Run all unit tests and verify pass rate (146 tests pass)

**Checkpoint**: Unit tests complete, all pass

---

## Phase 4: User Story 3 - Project Documentation (Priority: P1)

**Goal**: Comprehensive README.md with installation, usage, and API overview

**Independent Test**: README.md exists with all required sections; instructions are accurate

### Implementation for User Story 3

- [x] T019 [US3] Create README.md with project description, features, tech stack in README.md
- [x] T020 [US3] Add installation, environment variables, database setup, running tests sections to README.md

**Checkpoint**: README.md complete with all required sections

---

## Phase 5: User Story 4 - API Documentation (Priority: P1)

**Goal**: Detailed API reference with endpoints, examples, and authentication

**Independent Test**: API_DOCS.md lists all endpoints with request/response examples

### Implementation for User Story 4

- [x] T021 [US4] Create API_DOCS.md with authentication section and endpoint list in API_DOCS.md
- [x] T022 [US4] Add request/response examples, error formats, pagination info to API_DOCS.md

**Checkpoint**: API_DOCS.md complete with all endpoints documented

---

## Phase 6: User Story 2 - Integration Tests (Priority: P2)

**Goal**: End-to-end workflow tests verifying complete user journeys

**Independent Test**: `python manage.py test api.tests.test_integration` passes

### Implementation for User Story 2

- [x] T023 [US2] Create integration tests for client→case→document workflow in legaldocs/api/tests/test_integration.py
- [x] T024 [US2] Add dashboard accuracy and search functionality integration tests in legaldocs/api/tests/test_integration.py

**Checkpoint**: Integration tests pass, workflows verified

---

## Phase 7: User Story 5 - Demo Data (Priority: P2)

**Goal**: Realistic demo data fixtures and easy-to-use management command

**Independent Test**: `python manage.py load_demo_data` runs without errors; database has 20+ clients, 30+ cases, 50+ documents

### Implementation for User Story 5

- [x] T025 [P] [US5] Create demo_clients.json with 20+ clients in legaldocs/fixtures/demo_clients.json
- [x] T026 [P] [US5] Create demo_cases.json with 30+ cases in legaldocs/fixtures/demo_cases.json
- [x] T027 [P] [US5] Create demo_documents.json with 50+ documents in legaldocs/fixtures/demo_documents.json
- [x] T028 [US5] Create management command directory structure in legaldocs/core/management/commands/__init__.py
- [x] T029 [US5] Create load_demo_data management command in legaldocs/core/management/commands/load_demo_data.py

**Checkpoint**: Demo data loads successfully with correct counts

---

## Phase 8: User Story 6 - Deployment Documentation (Priority: P2)

**Goal**: Production deployment guide with checklist and security recommendations

**Independent Test**: DEPLOYMENT.md exists with checklist, environment variables, and security recommendations

### Implementation for User Story 6

- [x] T030 [US6] Create DEPLOYMENT.md with pre-deployment checklist in DEPLOYMENT.md
- [x] T031 [US6] Add production settings, environment variables, security recommendations to DEPLOYMENT.md

**Checkpoint**: DEPLOYMENT.md complete with all production guidance

---

## Phase 9: Validation & Polish

**Purpose**: Verify coverage target met and all documentation accurate

- [x] T032 Run full test suite with coverage and verify ≥70% coverage
- [x] T033 Review all documentation for accuracy against actual behavior
- [x] T034 Run quickstart.md verification checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - create directory structure first
- **Phase 2 (Foundational)**: Depends on Phase 1 - verify existing tests work
- **Phase 3 (US1 - Unit Tests)**: Depends on Phase 2 - can begin after foundation
- **Phase 4 (US3 - README)**: Depends on Phase 2 - can run parallel to US1
- **Phase 5 (US4 - API Docs)**: Depends on Phase 2 - can run parallel to US1
- **Phase 6 (US2 - Integration)**: Depends on Phase 3 - needs unit tests complete
- **Phase 7 (US5 - Demo Data)**: Depends on Phase 2 - can run parallel to other stories
- **Phase 8 (US6 - Deployment)**: Depends on Phase 2 - can run parallel to other stories
- **Phase 9 (Validation)**: Depends on all phases complete

### User Story Independence

After Phase 2, P1 stories can be implemented in parallel:

- **US1 (Unit Tests)**: Independent - creates test files only
- **US3 (README)**: Independent - creates README.md only
- **US4 (API Docs)**: Independent - creates API_DOCS.md only

P2 stories can also run in parallel:

- **US2 (Integration)**: Depends on US1 model tests for patterns
- **US5 (Demo Data)**: Independent - creates fixtures and command
- **US6 (Deployment)**: Independent - creates DEPLOYMENT.md only

### Parallel Opportunities

```text
Phase 1 (T001-T004): Setup - T002, T003, T004 in parallel
  ↓
Phase 2 (T005-T006): Foundational
  ↓
Parallel execution possible:
├── Phase 3 (T007-T018): Unit Tests [US1]
│   ├── T007, T008, T009 in parallel (model tests)
│   ├── T010, T011, T012 in parallel (serializer tests)
│   └── T013, T014, T015 in parallel (ViewSet tests)
├── Phase 4 (T019-T020): README [US3]
├── Phase 5 (T021-T022): API Docs [US4]
├── Phase 7 (T025-T029): Demo Data [US5]
│   └── T025, T026, T027 in parallel (fixture files)
└── Phase 8 (T030-T031): Deployment [US6]
  ↓
Phase 6 (T023-T024): Integration Tests [US2] (after US1)
  ↓
Phase 9 (T032-T034): Validation
```

---

## Implementation Strategy

### MVP First (Recommended Order)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 - Unit Tests (core deliverable)
4. **STOP and VALIDATE**: Run tests, check coverage
5. Complete Phase 4: US3 - README
6. Complete Phase 5: US4 - API Docs
7. Complete Phase 6: US2 - Integration Tests
8. Complete Phase 7: US5 - Demo Data
9. Complete Phase 8: US6 - Deployment Docs
10. Complete Phase 9: Full validation

### Parallel Execution

If working with multiple developers:
- Developer A: Phase 1 → Phase 2 → Phase 3 (Unit Tests)
- Developer B: Wait for Phase 2 → Phase 4 + Phase 5 (Documentation)
- Developer C: Wait for Phase 2 → Phase 7 + Phase 8 (Demo Data + Deployment)
- All: Phase 6 (Integration) → Phase 9 (Validation)

---

## Git Commit

After completing all tasks:

```bash
git add .
git commit -m "test(all): agregar tests comprehensivos y documentación

- Agregar tests unitarios para modelos, serializers y ViewSets
- Crear tests de integración para flujos completos
- Crear README.md con instrucciones de instalación
- Documentar API completa en API_DOCS.md
- Agregar fixtures de demo con datos realistas
- Crear guía de deployment en DEPLOYMENT.md
- Alcanzar 70%+ de cobertura de código"
```

---

## Notes

- All test files use Django TestCase for models, APITestCase for views
- File upload tests use Django's SimpleUploadedFile for in-memory files
- Demo data uses Spanish names and Latin American legal terminology
- Fixtures must be loaded in order: clients → cases → documents
- Coverage is measured with: `coverage run --source='clients,cases,documents,api' manage.py test`

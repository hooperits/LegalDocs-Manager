# Tasks: Django REST Framework API

**Input**: Design documents from `/specs/004-rest-api/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Task Overview

| Phase | Tasks | Focus |
|-------|-------|-------|
| 1. Setup | 3 | Install dependencies, create api app |
| 2. Foundational (US1) | 5 | DRF configuration, authentication, CORS |
| 3. User Story 2 | 4 | Client API (serializers, viewset) |
| 4. User Story 3 | 4 | Case API (serializers, viewset, custom actions) |
| 5. User Story 4 | 4 | Document API (serializer, viewset, permissions) |
| 6. User Story 5 | 2 | API Documentation (schema, swagger) |
| 7. Validation | 2 | Testing and verification |

**Total Tasks**: 24

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Install dependencies and create API app structure

- [x] T001 Install DRF dependencies: djangorestframework, django-filter, drf-spectacular, django-cors-headers in requirements.txt
- [x] T002 Create api Django app with startapp command in legaldocs/api/
- [x] T003 Add new apps to INSTALLED_APPS in legaldocs/legaldocs/settings.py (rest_framework, django_filters, drf_spectacular, corsheaders, api)

**Checkpoint**: Dependencies installed and api app created

---

## Phase 2: User Story 1 - API Setup and Authentication (Priority: P1) 🎯 MVP

**Goal**: Configure DRF with authentication so that only authorized users can access endpoints

**Independent Test**: Access /api/v1/clients/ without token → 401, with token → 200

### Implementation for User Story 1

- [x] T004 [US1] Add REST_FRAMEWORK configuration (authentication, pagination, filters) to legaldocs/legaldocs/settings.py
- [x] T005 [US1] Add CORS configuration (CORS_ALLOWED_ORIGINS, middleware) to legaldocs/legaldocs/settings.py
- [x] T006 [US1] Add file upload limits (DATA_UPLOAD_MAX_MEMORY_SIZE) to legaldocs/legaldocs/settings.py
- [x] T007 [US1] Create IsOwnerOrReadOnly permission class in legaldocs/api/permissions.py
- [x] T008 [US1] Create URL router with token auth endpoint in legaldocs/api/urls.py (placeholder, viewsets added later)

**Checkpoint**: DRF configured with authentication - API infrastructure ready for viewsets

---

## Phase 3: User Story 2 - Client API (Priority: P1)

**Goal**: Complete Client API with CRUD operations, filtering, search, and custom action

**Independent Test**: Test all CRUD on /api/v1/clients/, filter by is_active, search by name, access /clients/{id}/cases/

### Implementation for User Story 2

- [x] T009 [P] [US2] Create ClientSerializer (excludes notes) in legaldocs/clients/serializers.py
- [x] T010 [P] [US2] Create ClientDetailSerializer (includes notes, case_count) in legaldocs/clients/serializers.py
- [x] T011 [US2] Create ClientViewSet with filter, search, ordering in legaldocs/clients/views.py
- [x] T012 [US2] Add cases custom action (@action) to ClientViewSet in legaldocs/clients/views.py

**Checkpoint**: Client API fully functional with all CRUD and /clients/{id}/cases/ action

---

## Phase 4: User Story 3 - Case API (Priority: P1)

**Goal**: Complete Case API with CRUD, filtering, ordering, and custom actions (close, statistics)

**Independent Test**: Test CRUD on /api/v1/cases/, filter by status/type/priority, test /cases/{id}/close/ and /cases/statistics/

### Implementation for User Story 3

- [x] T013 [P] [US3] Create CaseSerializer (includes client_name) in legaldocs/cases/serializers.py
- [x] T014 [P] [US3] Create CaseDetailSerializer (nested client, documents) in legaldocs/cases/serializers.py
- [x] T015 [US3] Create CaseViewSet with filters, ordering in legaldocs/cases/views.py
- [x] T016 [US3] Add close and statistics custom actions to CaseViewSet in legaldocs/cases/views.py

**Checkpoint**: Case API fully functional with all CRUD, close action, and statistics endpoint

---

## Phase 5: User Story 4 - Document API (Priority: P1)

**Goal**: Document API with file upload support and owner-based delete permissions

**Independent Test**: Upload file via multipart/form-data, verify uploaded_by auto-set, test delete permission (owner vs non-owner)

### Implementation for User Story 4

- [x] T017 [P] [US4] Create DocumentSerializer (includes case_number, uploaded_by_username) in legaldocs/documents/serializers.py
- [x] T018 [US4] Create DocumentViewSet with MultiPartParser in legaldocs/documents/views.py
- [x] T019 [US4] Add perform_create to auto-set uploaded_by in DocumentViewSet in legaldocs/documents/views.py
- [x] T020 [US4] Apply IsOwnerOrReadOnly permission to DocumentViewSet in legaldocs/documents/views.py

**Checkpoint**: Document API fully functional with file upload and delete permissions

---

## Phase 6: User Story 5 - API Documentation (Priority: P2)

**Goal**: OpenAPI schema generation and Swagger UI for interactive documentation

**Independent Test**: Access /api/v1/schema/ for OpenAPI spec, /api/v1/docs/ for Swagger UI

### Implementation for User Story 5

- [x] T021 [US5] Add drf-spectacular settings (SPECTACULAR_SETTINGS) to legaldocs/legaldocs/settings.py
- [x] T022 [US5] Add schema and docs URLs to legaldocs/api/urls.py

**Checkpoint**: API documentation available at /api/v1/schema/ and /api/v1/docs/

---

## Phase 7: Integration & Wiring

**Purpose**: Connect all components and finalize URL routing

- [x] T023 Register all viewsets (clients, cases, documents) in router in legaldocs/api/urls.py
- [x] T024 Add api/v1/ URL include to legaldocs/legaldocs/urls.py

**Checkpoint**: All API endpoints accessible at /api/v1/

---

## Phase 8: Validation & Polish

**Purpose**: Verify all API features work correctly per quickstart.md

- [x] T025 Run Django system checks and verify no errors
- [x] T026 Test all endpoints per quickstart.md verification checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - install dependencies first
- **Phase 2 (US1)**: Depends on Phase 1 - DRF must be installed
- **Phase 3-5 (US2-US4)**: Depend on Phase 2 - authentication must be configured
- **Phase 6 (US5)**: Depends on Phase 2 - needs DRF configured
- **Phase 7 (Integration)**: Depends on Phases 3-6 - all viewsets must exist
- **Phase 8 (Validation)**: Depends on all phases complete

### User Story Independence

After Phase 2, user stories can be implemented in parallel:

- **US2 (ClientAPI)**: Independent - creates clients/serializers.py and clients/views.py
- **US3 (CaseAPI)**: Independent - creates cases/serializers.py and cases/views.py (imports DocumentSerializer)
- **US4 (DocumentAPI)**: Independent - creates documents/serializers.py and documents/views.py
- **US5 (Documentation)**: Independent - only adds settings and URLs

### Parallel Opportunities

```text
Phase 1 (T001-T003): Setup
  ↓
Phase 2 (T004-T008): Authentication & Config [US1]
  ↓
Parallel execution possible:
├── Phase 3 (T009-T012): ClientAPI [US2]
├── Phase 4 (T013-T016): CaseAPI [US3]
├── Phase 5 (T017-T020): DocumentAPI [US4]
└── Phase 6 (T021-T022): Documentation [US5]
  ↓
Phase 7 (T023-T024): Integration (wire all viewsets)
  ↓
Phase 8 (T025-T026): Validation
```

---

## Implementation Strategy

### MVP First (Recommended Order)

1. Complete Phase 1: Setup
2. Complete Phase 2: Authentication (US1)
3. Complete Phase 3: ClientAPI (US2) - First working endpoint
4. Complete Phase 7: Integration (wire ClientViewSet)
5. **STOP and VALIDATE**: Test Client API works
6. Continue with Phases 4-6
7. Complete Phase 8: Full validation

### Parallel Execution

If working with multiple developers:
- Developer A: Phase 1 → Phase 2 → Phase 3 (Client)
- Developer B: Wait for Phase 2 → Phase 4 (Case)
- Developer C: Wait for Phase 2 → Phase 5 (Document)
- Developer D: Wait for Phase 2 → Phase 6 (Docs)
- All: Phase 7-8 (Integration & Validation)

---

## Git Commit

After completing all tasks:

```bash
git add .
git commit -m "feat(api): implementar API REST con Django REST Framework

- Configurar DRF con autenticación Token y Session
- Implementar ClientViewSet con filtros y acción /cases/
- Implementar CaseViewSet con acciones close y statistics
- Implementar DocumentViewSet con permisos de propietario
- Agregar documentación OpenAPI con Swagger UI
- Configurar CORS para desarrollo"
```

---

## Notes

- DocumentSerializer must be created before CaseDetailSerializer (imports it)
- All serializers use ModelSerializer with explicit field lists
- ViewSets use select_related for performance
- Custom permissions in api/permissions.py, not in each app
- Token auth uses DRF's built-in obtain_auth_token view
- CORS middleware must be first in MIDDLEWARE list

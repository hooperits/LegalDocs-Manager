# Tasks: Authentication and Dashboard Views

**Input**: Design documents from `/specs/005-auth-dashboard/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Task Overview

| Phase | Tasks | Focus |
|-------|-------|-------|
| 1. Setup | 2 | Create tests directory structure |
| 2. Foundational | 2 | Create serializers file, base URL structure |
| 3. User Story 1 | 8 | Authentication endpoints (login, logout, register, me) |
| 4. User Story 2 | 2 | Dashboard statistics endpoint |
| 5. User Story 3 | 2 | Global search endpoint |
| 6. User Story 4 | 2 | User profile endpoint |
| 7. User Story 5 | 4 | Comprehensive tests |
| 8. Validation | 2 | System checks and verification |

**Total Tasks**: 24

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create test directory structure within api app

- [x] T001 Create tests directory with __init__.py in legaldocs/api/tests/__init__.py
- [x] T002 [P] Verify api app serializers.py exists, create if missing in legaldocs/api/serializers.py

**Checkpoint**: Test directory structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Base serializers and URL structure that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create UserInfoSerializer for basic user data in legaldocs/api/serializers.py
- [x] T004 Add auth URL namespace structure in legaldocs/api/urls.py (placeholder paths for auth/, dashboard/, search/, profile/)

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Authentication Endpoints (Priority: P1) 🎯 MVP

**Goal**: Complete authentication flows: login (obtain token), logout (delete token), register (create user + token), me (current user info)

**Independent Test**: POST /api/v1/auth/login/ with valid credentials returns token; POST /api/v1/auth/logout/ deletes token; POST /api/v1/auth/register/ creates user; GET /api/v1/auth/me/ returns user info

### Implementation for User Story 1

- [x] T005 [P] [US1] Create LoginSerializer extending AuthTokenSerializer in legaldocs/api/serializers.py
- [x] T006 [P] [US1] Create RegisterSerializer with password validation in legaldocs/api/serializers.py
- [x] T007 [US1] Create LoginView extending ObtainAuthToken in legaldocs/api/views.py
- [x] T008 [US1] Create LogoutView with token deletion in legaldocs/api/views.py
- [x] T009 [US1] Create RegisterView with user creation and token return in legaldocs/api/views.py
- [x] T010 [US1] Create MeView for current user info in legaldocs/api/views.py
- [x] T011 [US1] Add auth endpoint URLs (login, logout, register, me) in legaldocs/api/urls.py
- [x] T012 [US1] Test auth endpoints manually via curl/httpie per quickstart.md

**Checkpoint**: Authentication endpoints fully functional - login, logout, register, me all working

---

## Phase 4: User Story 2 - Dashboard Statistics (Priority: P1)

**Goal**: Dashboard endpoint returning aggregated statistics with optimized queries

**Independent Test**: GET /api/v1/dashboard/ returns total_clients, active_clients, cases_by_status, cases_by_type, recent_cases, documents_by_type, upcoming_deadlines

### Implementation for User Story 2

- [x] T013 [US2] Create DashboardView with optimized aggregate queries in legaldocs/api/views.py
- [x] T014 [US2] Add dashboard URL endpoint in legaldocs/api/urls.py

**Checkpoint**: Dashboard endpoint returns all required statistics with optimized queries

---

## Phase 5: User Story 3 - Global Search (Priority: P2)

**Goal**: Search endpoint that queries across clients, cases, and documents

**Independent Test**: GET /api/v1/search/?q=García returns matching clients, cases, and documents limited to 10 per model

### Implementation for User Story 3

- [x] T015 [US3] Create SearchView with Q objects for cross-model search in legaldocs/api/views.py
- [x] T016 [US3] Add search URL endpoint in legaldocs/api/urls.py

**Checkpoint**: Search endpoint returns unified results from all models

---

## Phase 6: User Story 4 - User Profile (Priority: P2)

**Goal**: Profile endpoint for viewing and updating user profile (email, first_name, last_name)

**Independent Test**: GET /api/v1/profile/ returns profile with assigned_cases_count; PATCH updates allowed fields; username is read-only

### Implementation for User Story 4

- [x] T017 [P] [US4] Create ProfileSerializer with assigned_cases_count and read-only username in legaldocs/api/serializers.py
- [x] T018 [US4] Create ProfileView with GET and PATCH methods in legaldocs/api/views.py
- [x] T019 [US4] Add profile URL endpoint in legaldocs/api/urls.py

**Checkpoint**: Profile endpoint allows viewing and updating user profile

---

## Phase 7: User Story 5 - Comprehensive Tests (Priority: P1)

**Goal**: Full test coverage for all authentication and API flows

**Independent Test**: Run pytest and verify all tests pass

### Implementation for User Story 5

- [x] T020 [P] [US5] Create test_auth.py with login, logout, register, me tests in legaldocs/api/tests/test_auth.py
- [x] T021 [P] [US5] Create test_dashboard.py with dashboard statistics tests in legaldocs/api/tests/test_dashboard.py
- [x] T022 [P] [US5] Create test_search.py with global search tests in legaldocs/api/tests/test_search.py
- [x] T023 [P] [US5] Create test_profile.py with profile get/update tests in legaldocs/api/tests/test_profile.py

**Checkpoint**: All tests pass, comprehensive coverage for authentication and API endpoints

---

## Phase 8: Validation & Polish

**Purpose**: Verify all API features work correctly per quickstart.md

- [x] T024 Run Django system checks and verify no errors
- [x] T025 Test all endpoints per quickstart.md verification checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - create directory structure first
- **Phase 2 (Foundational)**: Depends on Phase 1 - base serializers and URL structure
- **Phase 3 (US1 - Auth)**: Depends on Phase 2 - authentication endpoints
- **Phase 4 (US2 - Dashboard)**: Depends on Phase 2 - can run parallel to US1
- **Phase 5 (US3 - Search)**: Depends on Phase 2 - can run parallel to US1/US2
- **Phase 6 (US4 - Profile)**: Depends on Phase 2 - can run parallel to other US
- **Phase 7 (US5 - Tests)**: Depends on Phases 3-6 - all endpoints must exist
- **Phase 8 (Validation)**: Depends on all phases complete

### User Story Independence

After Phase 2, user stories can be implemented in parallel:

- **US1 (Auth)**: Independent - creates auth views and serializers
- **US2 (Dashboard)**: Independent - creates DashboardView only
- **US3 (Search)**: Independent - creates SearchView only
- **US4 (Profile)**: Independent - creates ProfileSerializer and ProfileView
- **US5 (Tests)**: Depends on US1-US4 - tests all endpoints

### Parallel Opportunities

```text
Phase 1 (T001-T002): Setup
  ↓
Phase 2 (T003-T004): Foundational
  ↓
Parallel execution possible:
├── Phase 3 (T005-T012): Auth [US1]
├── Phase 4 (T013-T014): Dashboard [US2]
├── Phase 5 (T015-T016): Search [US3]
└── Phase 6 (T017-T019): Profile [US4]
  ↓
Phase 7 (T020-T023): Tests [US5] (all tests can run in parallel)
  ↓
Phase 8 (T024-T025): Validation
```

---

## Implementation Strategy

### MVP First (Recommended Order)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: Auth (US1) - First working endpoints
4. **STOP and VALIDATE**: Test auth endpoints work
5. Complete Phase 4: Dashboard (US2)
6. Complete Phase 5: Search (US3)
7. Complete Phase 6: Profile (US4)
8. Complete Phase 7: Tests (US5)
9. Complete Phase 8: Full validation

### Parallel Execution

If working with multiple developers:
- Developer A: Phase 1 → Phase 2 → Phase 3 (Auth)
- Developer B: Wait for Phase 2 → Phase 4 (Dashboard)
- Developer C: Wait for Phase 2 → Phase 5 (Search)
- Developer D: Wait for Phase 2 → Phase 6 (Profile)
- All: Phase 7-8 (Tests & Validation)

---

## Git Commit

After completing all tasks:

```bash
git add .
git commit -m "feat(auth): implementar autenticación, dashboard, búsqueda y perfil

- Agregar endpoints de autenticación (login, logout, register, me)
- Crear endpoint de dashboard con estadísticas optimizadas
- Implementar búsqueda global en clientes, casos y documentos
- Agregar gestión de perfil de usuario
- Incluir tests comprehensivos para todos los endpoints"
```

---

## Notes

- All serializers in api/serializers.py, all views in api/views.py
- Use DRF's ObtainAuthToken as base for LoginView
- Dashboard uses Django ORM annotate() and values() for efficiency
- Search uses Q objects with icontains for case-insensitive matching
- Profile allows PATCH for email, first_name, last_name (username read-only)
- Tests use DRF's APITestCase with force_authenticate() for auth

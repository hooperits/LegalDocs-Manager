# Tasks: Project Setup

**Input**: Design documents from `/specs/001-project-setup/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: No tests explicitly requested for this infrastructure setup feature.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- All paths are relative to repository root: `/home/juanca/proys/LegalDocs-Manager/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create repository-level configuration files that all user stories depend on

- [x] T001 [P] Create requirements.txt with pinned dependencies at ./requirements.txt
- [x] T002 [P] Create .gitignore for Python/Django at ./.gitignore
- [x] T003 [P] Create .env.example with documented variables at ./.env.example

**Checkpoint**: Configuration files ready - proceed to Foundational phase

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create Django project structure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Python virtual environment at ./venv/
- [x] T005 Install dependencies from requirements.txt into virtual environment
- [x] T006 Create Django project 'legaldocs' at ./legaldocs/ using django-admin startproject

**Checkpoint**: Django project skeleton exists - user story implementation can now begin

---

## Phase 3: User Story 1 - Developer Environment Setup (Priority: P1) 🎯 MVP

**Goal**: Complete Django development environment with all dependencies installed and configured

**Independent Test**: Run `python manage.py runserver` and access Django welcome page at `http://localhost:8000`

### Implementation for User Story 1

- [x] T007 [US1] Configure settings.py to load environment variables using python-dotenv at ./legaldocs/legaldocs/settings.py
- [x] T008 [US1] Add third-party apps to INSTALLED_APPS (rest_framework, corsheaders, django_filters) in ./legaldocs/legaldocs/settings.py
- [x] T009 [US1] Configure REST_FRAMEWORK settings (authentication, pagination, filtering) in ./legaldocs/legaldocs/settings.py
- [x] T010 [US1] Configure CORS settings in ./legaldocs/legaldocs/settings.py
- [x] T011 [US1] Configure MIDDLEWARE to include corsheaders middleware in ./legaldocs/legaldocs/settings.py
- [x] T012 [US1] Verify Django check passes: run `python manage.py check`

**Checkpoint**: User Story 1 complete - Django starts with `python manage.py runserver`

---

## Phase 4: User Story 2 - Database Connection (Priority: P1)

**Goal**: PostgreSQL database configured and connected, migrations working

**Independent Test**: Run `python manage.py migrate` successfully and create a superuser

### Implementation for User Story 2

- [x] T013 [US2] Configure DATABASES setting for PostgreSQL in ./legaldocs/legaldocs/settings.py
- [x] T014 [US2] Create .env file from .env.example with actual database credentials at ./.env
- [x] T015 [US2] Verify database connection: run `python manage.py dbshell` (should connect)
- [x] T016 [US2] Run initial Django migrations: `python manage.py migrate`
- [x] T017 [US2] Create superuser account: `python manage.py createsuperuser`

**Checkpoint**: User Story 2 complete - Database connected, migrations applied, superuser exists

---

## Phase 5: User Story 3 - Django Admin Access (Priority: P1)

**Goal**: Django Admin accessible and functional for verifying project setup

**Independent Test**: Login to `/admin/` with superuser credentials

### Implementation for User Story 3

- [x] T018 [US3] Verify admin URL is configured in ./legaldocs/legaldocs/urls.py
- [x] T019 [US3] Start development server and access admin at http://localhost:8000/admin/
- [x] T020 [US3] Login to Django Admin with superuser credentials and verify dashboard loads

**Checkpoint**: User Story 3 complete - Admin interface accessible and functional

---

## Phase 6: User Story 4 - App Structure Ready (Priority: P2)

**Goal**: All five Django apps created and registered in INSTALLED_APPS

**Independent Test**: Check project structure shows all app directories and `python manage.py check` passes

### Implementation for User Story 4

- [x] T021 [P] [US4] Create core app: run `python manage.py startapp core` in ./legaldocs/
- [x] T022 [P] [US4] Create users app: run `python manage.py startapp users` in ./legaldocs/
- [x] T023 [P] [US4] Create clients app: run `python manage.py startapp clients` in ./legaldocs/
- [x] T024 [P] [US4] Create cases app: run `python manage.py startapp cases` in ./legaldocs/
- [x] T025 [P] [US4] Create documents app: run `python manage.py startapp documents` in ./legaldocs/
- [x] T026 [US4] Register all five local apps in INSTALLED_APPS in ./legaldocs/legaldocs/settings.py
- [x] T027 [P] [US4] Create static directory at ./legaldocs/static/
- [x] T028 [P] [US4] Create media directory at ./legaldocs/media/
- [x] T029 [US4] Configure STATIC_URL, STATICFILES_DIRS, MEDIA_URL, MEDIA_ROOT in ./legaldocs/legaldocs/settings.py
- [x] T030 [US4] Verify all apps registered: run `python manage.py check`

**Checkpoint**: User Story 4 complete - All apps created and registered

---

## Phase 7: User Story 5 - Environment Configuration (Priority: P2)

**Goal**: Secure environment variable configuration with .env gitignored

**Independent Test**: Verify `.env` not tracked by git and `.env.example` documents all variables

### Implementation for User Story 5

- [x] T031 [US5] Verify .env is in .gitignore at ./.gitignore
- [x] T032 [US5] Verify .env.example documents all required variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_*)
- [x] T033 [US5] Run `git status` to confirm .env is not tracked
- [x] T034 [US5] Verify Django loads env vars correctly by checking settings values

**Checkpoint**: User Story 5 complete - Environment securely configured

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, git commit, and documentation

- [ ] T035 Run full verification: `python manage.py check` (no issues)
- [ ] T036 Run full verification: `python manage.py migrate` (no pending migrations)
- [ ] T037 Run full verification: `python manage.py runserver` (starts on port 8000)
- [ ] T038 Verify Django Admin login works at http://localhost:8000/admin/
- [ ] T039 Create initial git commit in Spanish per constitution standards
- [ ] T040 Validate against quickstart.md checklist

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ─────────────────────────────────────┐
                                                     │
Phase 2 (Foundational) ──────────────────────────────┤
                                                     │
    ┌────────────────────────────────────────────────┘
    │
    ├── Phase 3 (US1: Environment) ──────┐
    │                                    │
    ├── Phase 4 (US2: Database) ─────────┤─── Can run sequentially
    │                                    │    (US2 depends on US1 settings)
    ├── Phase 5 (US3: Admin) ────────────┤
    │                                    │    (US3 depends on US2 superuser)
    ├── Phase 6 (US4: Apps) ─────────────┤
    │                                    │    (Can run parallel to US1-3)
    └── Phase 7 (US5: Env Config) ───────┘
                                         │
Phase 8 (Polish) ────────────────────────┘
```

### User Story Dependencies

| Story | Depends On | Notes |
|-------|------------|-------|
| US1 (Environment) | Phase 2 | First story - enables Django startup |
| US2 (Database) | US1 | Needs settings.py configured |
| US3 (Admin) | US2 | Needs database and superuser |
| US4 (Apps) | Phase 2 | Can run parallel to US1-3 |
| US5 (Env Config) | Phase 1 | Can run parallel after Phase 1 |

### Parallel Opportunities

**Phase 1 - All tasks parallel:**
```
T001, T002, T003 → All create different files
```

**Phase 6 (US4) - App creation parallel:**
```
T021, T022, T023, T024, T025 → Each creates different app directory
T027, T028 → Create different directories
```

---

## Parallel Example: Phase 1 Setup

```bash
# All three tasks can run simultaneously:
Task: "Create requirements.txt at ./requirements.txt"
Task: "Create .gitignore at ./.gitignore"
Task: "Create .env.example at ./.env.example"
```

## Parallel Example: Phase 6 App Creation

```bash
# All five app creation tasks can run simultaneously:
Task: "Create core app in ./legaldocs/"
Task: "Create users app in ./legaldocs/"
Task: "Create clients app in ./legaldocs/"
Task: "Create cases app in ./legaldocs/"
Task: "Create documents app in ./legaldocs/"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T006)
3. Complete Phase 3: US1 Environment (T007-T012)
4. Complete Phase 4: US2 Database (T013-T017)
5. Complete Phase 5: US3 Admin (T018-T020)
6. **STOP and VALIDATE**: Django running + Admin accessible = MVP!

### Full Implementation

1. MVP (above)
2. Add Phase 6: US4 Apps (T021-T030)
3. Add Phase 7: US5 Env Config (T031-T034)
4. Complete Phase 8: Polish (T035-T040)
5. Commit with Spanish message per constitution

### Recommended Execution Order

Since this is infrastructure setup (single developer), execute sequentially:

```
T001 → T002 → T003 (parallel OK)
T004 → T005 → T006 (sequential - depends on venv)
T007 → T008 → T009 → T010 → T011 → T012 (sequential - same file)
T013 → T014 → T015 → T016 → T017 (sequential - depends on DB)
T018 → T019 → T020 (sequential - depends on server)
T021-T025 (parallel OK) → T026 → T027-T028 (parallel OK) → T029 → T030
T031 → T032 → T033 → T034 (sequential - verification)
T035 → T036 → T037 → T038 → T039 → T040 (sequential - final checks)
```

---

## Notes

- This feature creates infrastructure only - no custom models or API endpoints
- All [P] tasks can run in parallel if desired
- Commit after completing each user story or at final polish phase
- Verification tasks (T012, T015, T030, etc.) confirm story completion
- Git commit (T039) should be in Spanish per constitution

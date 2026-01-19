# Tasks: Final Polish

**Input**: Design documents from `/specs/007-final-polish/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: No additional test tasks - existing 99% coverage to be maintained. Tests are implicitly verified through existing test suite.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization - add new dependencies

- [X] T001 Add django-ratelimit>=4.1.0 and python-magic>=0.4.27 to requirements.txt
- [X] T002 Install new dependencies with pip install -r requirements.txt
- [X] T003 Install libmagic system dependency for python-magic

**Checkpoint**: Dependencies ready - feature implementation can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user stories

**⚠️ CRITICAL**: Settings and infrastructure needed by all user stories

- [X] T004 Configure CACHES with database backend in legaldocs/settings.py
- [X] T005 Add MAX_UPLOAD_SIZE and ALLOWED_FILE_TYPES settings in legaldocs/settings.py
- [X] T006 Add RATELIMIT_ENABLE and RATELIMIT_USE_CACHE settings in legaldocs/settings.py
- [X] T007 Create cache table with python manage.py createcachetable

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Code Quality (Priority: P1) 🎯 MVP

**Goal**: Clean, well-documented code with proper docstrings and type hints

**Independent Test**: Run `ruff check clients/ cases/ documents/ api/` - no critical errors

### Implementation for User Story 1

- [X] T008 [P] [US1] Add docstrings to Client model in legaldocs/clients/models.py
- [X] T009 [P] [US1] Add docstrings to Case model in legaldocs/cases/models.py
- [X] T010 [P] [US1] Add docstrings to Document model in legaldocs/documents/models.py
- [X] T011 [P] [US1] Add docstrings to ClientSerializer in legaldocs/clients/serializers.py
- [X] T012 [P] [US1] Add docstrings to CaseSerializer in legaldocs/cases/serializers.py
- [X] T013 [P] [US1] Add docstrings to DocumentSerializer in legaldocs/documents/serializers.py
- [X] T014 [P] [US1] Add docstrings to ClientViewSet in legaldocs/clients/views.py
- [X] T015 [P] [US1] Add docstrings to CaseViewSet in legaldocs/cases/views.py
- [X] T016 [P] [US1] Add docstrings to DocumentViewSet in legaldocs/documents/views.py
- [X] T017 [P] [US1] Add docstrings to auth views in legaldocs/api/views.py
- [X] T018 [US1] Add type hints to function signatures across all views
- [X] T019 [US1] Run ruff check and fix any linting issues in legaldocs/
- [X] T020 [US1] Remove unused imports and dead code across all files

**Checkpoint**: Code Quality complete - all files have docstrings, type hints, and pass linting

---

## Phase 4: User Story 2 - Security Hardening (Priority: P1)

**Goal**: Secure application with rate limiting and file validation

**Independent Test**: 6 rapid login requests - 6th returns 429; upload .exe file - returns 400

### Implementation for User Story 2

- [X] T021 [US2] Create file upload validators in legaldocs/documents/validators.py
- [X] T022 [US2] Create rate limiting configuration in legaldocs/api/throttling.py
- [X] T023 [US2] Add rate limiting decorator to login view in legaldocs/api/views.py
- [X] T024 [US2] Add rate limiting decorator to register view in legaldocs/api/views.py
- [X] T025 [US2] Integrate file validators into DocumentSerializer in legaldocs/documents/serializers.py
- [X] T026 [US2] Review and update CORS_ALLOWED_ORIGINS for production in legaldocs/settings.py
- [X] T027 [US2] Audit serializers for sensitive data exposure in all serializers.py files

**Checkpoint**: Security Hardening complete - rate limiting active, file validation working

---

## Phase 5: User Story 3 - Performance Optimization (Priority: P1)

**Goal**: Fast API responses with database indexes and query optimization

**Independent Test**: List endpoints respond in < 200ms; dashboard stats cached for 5 minutes

### Implementation for User Story 3

- [X] T028 [US3] Add database indexes to Case model in legaldocs/cases/models.py
- [X] T029 [US3] Add database indexes to Document model in legaldocs/documents/models.py
- [X] T030 [US3] Generate and apply migration for indexes with makemigrations and migrate
- [X] T031 [US3] Add select_related to CaseViewSet queryset in legaldocs/cases/views.py
- [X] T032 [US3] Add select_related to DocumentViewSet queryset in legaldocs/documents/views.py
- [X] T033 [US3] Create cache utilities module in legaldocs/core/cache.py
- [X] T034 [US3] Implement dashboard caching with 5-minute TTL in legaldocs/api/views.py

**Checkpoint**: Performance complete - indexes added, queries optimized, caching implemented

---

## Phase 6: User Story 4 - User Experience Improvements (Priority: P2)

**Goal**: Clear Spanish error messages for all API responses

**Independent Test**: POST to /api/v1/auth/register/ with empty body - returns Spanish error messages

### Implementation for User Story 4

- [X] T035 [US4] Create custom DRF exception handler in legaldocs/api/exceptions.py
- [X] T036 [US4] Add field name translations (English to Spanish) in legaldocs/api/exceptions.py
- [X] T037 [US4] Add common error message translations in legaldocs/api/exceptions.py
- [X] T038 [US4] Configure custom exception handler in legaldocs/settings.py REST_FRAMEWORK
- [X] T039 [US4] Add Spanish error messages to ClientSerializer in legaldocs/clients/serializers.py
- [X] T040 [US4] Add Spanish error messages to CaseSerializer in legaldocs/cases/serializers.py
- [X] T041 [US4] Add Spanish error messages to DocumentSerializer in legaldocs/documents/serializers.py
- [X] T042 [US4] Configure DATE_FORMAT and DATETIME_FORMAT in legaldocs/settings.py

**Checkpoint**: UX complete - all error messages in Spanish, dates formatted correctly

---

## Phase 7: User Story 5 - Final Testing (Priority: P1)

**Goal**: Thorough manual testing to verify all features work correctly

**Independent Test**: All 163+ automated tests pass; coverage >= 70%

### Implementation for User Story 5

- [X] T043 [US5] Run full test suite with python manage.py test --verbosity=2
- [X] T044 [US5] Run coverage report and verify >= 70% coverage
- [X] T045 [US5] Execute manual test scenarios from quickstart.md
- [X] T046 [US5] Test with large dataset (100+ records per model)
- [X] T047 [US5] Document any issues found and create fixes

**Checkpoint**: Testing complete - all tests pass, manual verification done

---

## Phase 8: User Story 6 - Demo Preparation (Priority: P2)

**Goal**: Professional demo materials for project showcase

**Independent Test**: Postman collection imports successfully; demo script is complete

### Implementation for User Story 6

- [X] T048 [P] [US6] Create demo script with 5-minute walkthrough in docs/demo-script.md
- [X] T049 [P] [US6] Create Postman collection in postman/LegalDocs-API.postman_collection.json
- [X] T050 [P] [US6] Create docs/images/ directory for screenshots
- [X] T051 [US6] Capture screenshots for key features (dashboard, client list, case detail)
- [X] T052 [US6] Add environment variables to Postman collection (base_url, token)

**Checkpoint**: Demo materials complete - ready for presentation

---

## Phase 9: User Story 7 - Repository Polish (Priority: P2)

**Goal**: Professional repository for portfolio showcase

**Independent Test**: LICENSE file exists; README has badges; v1.0.0 tag exists

### Implementation for User Story 7

- [X] T053 [US7] Create MIT LICENSE file in repository root
- [X] T054 [US7] Add Python, Django, and License badges to README.md
- [X] T055 [US7] Add project screenshots to README.md
- [X] T056 [US7] Verify .gitignore is comprehensive
- [X] T057 [US7] Create v1.0.0 release tag with git tag

**Checkpoint**: Repository polished - ready for portfolio showcase

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and cleanup

- [X] T058 Run quickstart.md verification checklist
- [X] T059 Final code review for consistency across all changes
- [X] T060 Verify all existing tests still pass after changes
- [X] T061 Update any documentation affected by changes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - US1 (Code Quality) can proceed independently
  - US2 (Security) can proceed independently
  - US3 (Performance) can proceed independently
  - US4 (UX) can proceed after US2 (uses exception handler)
  - US5 (Testing) should be done after US1-US4 are complete
  - US6 (Demo) can proceed after US5
  - US7 (Repository) can proceed after US5
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Phase 2 - May use exception handler from US2
- **User Story 5 (P1)**: Best done after US1-US4 complete - Tests all features
- **User Story 6 (P2)**: After US5 - Demo materials show finished product
- **User Story 7 (P2)**: After US5 - Repository polish for release

### Within Each User Story

- Validators/utilities before views
- Settings changes before features that use them
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks can run sequentially (dependency chain)
- All Foundational tasks can run sequentially (settings file)
- Once Foundational completes, US1, US2, US3 can start in parallel
- All T008-T017 (docstrings) can run in parallel (different files)
- T048-T050 (demo materials) can run in parallel (different files)

---

## Parallel Example: User Story 1 (Code Quality)

```bash
# Launch all docstring tasks together (different files):
Task: "Add docstrings to Client model in legaldocs/clients/models.py"
Task: "Add docstrings to Case model in legaldocs/cases/models.py"
Task: "Add docstrings to Document model in legaldocs/documents/models.py"

# Launch all serializer docstrings together:
Task: "Add docstrings to ClientSerializer in legaldocs/clients/serializers.py"
Task: "Add docstrings to CaseSerializer in legaldocs/cases/serializers.py"
Task: "Add docstrings to DocumentSerializer in legaldocs/documents/serializers.py"
```

---

## Parallel Example: User Story 6 (Demo)

```bash
# Launch all demo creation tasks together (different files):
Task: "Create demo script in docs/demo-script.md"
Task: "Create Postman collection in postman/LegalDocs-API.postman_collection.json"
Task: "Create docs/images/ directory"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Code Quality)
4. Complete Phase 4: User Story 2 (Security)
5. Complete Phase 5: User Story 3 (Performance)
6. **STOP and VALIDATE**: Run tests, verify basic functionality
7. This delivers a production-hardened API

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Code Quality) → Clean codebase
3. Add US2 (Security) → Hardened API
4. Add US3 (Performance) → Optimized queries
5. Add US4 (UX) → Spanish error messages
6. Add US5 (Testing) → Verified quality
7. Add US6 (Demo) → Presentation ready
8. Add US7 (Repository) → Portfolio ready

### Parallel Team Strategy

With multiple developers:

1. Developer A: US1 (Code Quality) - docstrings, linting
2. Developer B: US2 (Security) + US3 (Performance) - validators, indexes
3. Developer C: US6 (Demo) prep - can start Postman collection early

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Existing 99% test coverage must be maintained
- All error messages must be in Spanish
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

# Tasks: Screenshot Documentation for LegalDocs Manager

**Input**: Design documents from `/specs/009-screenshot-documentation/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: No automated tests requested for this feature (it IS a documentation generator).

**Organization**: Tasks grouped by user story to enable independent documentation generation per module.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **E2E Tests**: `tests/e2e/docs/`
- **Output**: `docs/screenshots/`
- **Fixtures**: `tests/e2e/fixtures/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory structure and base screenshot utilities

- [x] T001 Create output directory structure at docs/screenshots/
- [x] T002 Create tests/e2e/docs/ directory for screenshot generator
- [x] T003 [P] Create screenshot helper utilities in tests/e2e/docs/screenshot-utils.ts
- [x] T004 [P] Add screenshot project configuration to tests/e2e/playwright.config.ts

---

## Phase 2: Foundational (Test Data & Base Components)

**Purpose**: Test data generation and shared screenshot infrastructure that ALL modules depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create test data generator function in tests/e2e/docs/test-data.ts (uses existing AuthHelper, generateTestClient, generateTestCase, generateTestDocument)
- [x] T006 [P] Create module configuration constants in tests/e2e/docs/module-config.ts
- [x] T007 [P] Implement captureScreenshot helper function in tests/e2e/docs/screenshot-utils.ts
- [x] T008 [P] Implement ensureDirectory helper function in tests/e2e/docs/screenshot-utils.ts
- [x] T009 Implement README generator function in tests/e2e/docs/readme-generator.ts

**Checkpoint**: Foundation ready - module screenshot generation can now begin in parallel

---

## Phase 3: User Story 1 - Generate Visual Documentation (Priority: P1) 🎯 MVP

**Goal**: Create main orchestration script that coordinates all module screenshots and generates index

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts` and verify all module directories created with README.md

### Implementation for User Story 1

- [x] T010 [US1] Create main test file skeleton in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T011 [US1] Implement test setup to verify server availability in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T012 [US1] Implement test setup to create test data before screenshots in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T013 [US1] Implement final test to generate README.md index in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T014 [US1] Add cleanup option for test data after generation in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Main orchestration ready, placeholder tests for each module exist

---

## Phase 4: User Story 2 - Document Authentication Flow (Priority: P1)

**Goal**: Capture screenshots of Swagger UI authentication endpoints (login, register, auth)

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts -g "01-auth"` and verify 3 screenshots in docs/screenshots/01-auth/

### Implementation for User Story 2

- [x] T015 [P] [US2] Implement 01-auth test: capture login endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T016 [P] [US2] Implement 01-auth test: capture register endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T017 [US2] Implement 01-auth test: capture authenticated user menu in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Authentication module screenshots complete (3 images)

---

## Phase 5: User Story 3 - Document Client Management (Priority: P2)

**Goal**: Capture screenshots of client CRUD operations in Swagger UI

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts -g "02-clients"` and verify 4 screenshots in docs/screenshots/02-clients/

### Implementation for User Story 3

- [x] T018 [P] [US3] Implement 02-clients test: capture client list endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T019 [P] [US3] Implement 02-clients test: capture client create endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T020 [P] [US3] Implement 02-clients test: capture client detail endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T021 [US3] Implement 02-clients test: capture client update endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Client management module screenshots complete (4 images)

---

## Phase 6: User Story 4 - Document Case Management (Priority: P2)

**Goal**: Capture screenshots of case lifecycle operations in Swagger UI

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts -g "03-cases"` and verify 5 screenshots in docs/screenshots/03-cases/

### Implementation for User Story 4

- [x] T022 [P] [US4] Implement 03-cases test: capture case list endpoint with filters in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T023 [P] [US4] Implement 03-cases test: capture case create endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T024 [P] [US4] Implement 03-cases test: capture case detail endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T025 [P] [US4] Implement 03-cases test: capture case statistics endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T026 [US4] Implement 03-cases test: capture case close action endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Case management module screenshots complete (5 images)

---

## Phase 7: User Story 5 - Document Upload and Document Management (Priority: P2)

**Goal**: Capture screenshots of document upload and management in Swagger UI

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts -g "04-documents"` and verify 3 screenshots in docs/screenshots/04-documents/

### Implementation for User Story 5

- [x] T027 [P] [US5] Implement 04-documents test: capture document list endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T028 [P] [US5] Implement 04-documents test: capture document upload endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T029 [US5] Implement 04-documents test: capture document detail endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Document management module screenshots complete (3 images)

---

## Phase 8: User Story 6 - Document Dashboard and Search (Priority: P3)

**Goal**: Capture screenshots of dashboard and search functionality in Swagger UI

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts -g "05-dashboard"` and verify 2 screenshots in docs/screenshots/05-dashboard/

### Implementation for User Story 6

- [x] T030 [P] [US6] Implement 05-dashboard test: capture dashboard statistics endpoint in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T031 [US6] Implement 05-dashboard test: capture search endpoint with results in Swagger UI in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Dashboard and search module screenshots complete (2 images)

---

## Phase 9: User Story 7 - Document Admin Interface (Priority: P3)

**Goal**: Capture screenshots of Django admin interface

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts -g "06-admin"` and verify 4 screenshots in docs/screenshots/06-admin/

### Implementation for User Story 7

- [x] T032 [P] [US7] Implement 06-admin test: capture admin login page in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T033 [P] [US7] Implement 06-admin test: capture admin dashboard after login in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T034 [P] [US7] Implement 06-admin test: capture admin clients list in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T035 [US7] Implement 06-admin test: capture admin cases list with status badges in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Admin interface module screenshots complete (4 images)

---

## Phase 10: User Story 8 - Document Swagger API (Priority: P3)

**Goal**: Capture screenshots of Swagger UI overview and endpoint exploration

**Independent Test**: Run `npx playwright test docs/generate-screenshots.spec.ts -g "07-api"` and verify 3 screenshots in docs/screenshots/07-api/

### Implementation for User Story 8

- [x] T036 [P] [US8] Implement 07-api test: capture Swagger UI full overview in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T037 [P] [US8] Implement 07-api test: capture Swagger authentication section in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T038 [US8] Implement 07-api test: capture Swagger expanded endpoint with parameters in tests/e2e/docs/generate-screenshots.spec.ts

**Checkpoint**: Swagger API module screenshots complete (3 images)

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final README generation, validation, and cleanup

- [x] T039 Validate all screenshots exist and have correct dimensions in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T040 [P] Add progress logging throughout screenshot generation in tests/e2e/docs/generate-screenshots.spec.ts
- [x] T041 [P] Update quickstart.md with actual execution commands in specs/009-screenshot-documentation/quickstart.md
- [x] T042 Run full screenshot generation and verify README.md index at docs/screenshots/README.md
- [x] T043 Commit generated screenshots and documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase completion
  - US1 (orchestration) should complete first to establish file structure
  - US2-US8 can proceed in parallel after US1
- **Polish (Phase 11)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - Creates main file structure
- **User Story 2 (P1)**: Can start after US1 - Auth screenshots
- **User Story 3 (P2)**: Can start after US1 - Independent of US2
- **User Story 4 (P2)**: Can start after US1 - Independent of US2, US3
- **User Story 5 (P2)**: Can start after US1 - Independent of US2, US3, US4
- **User Story 6 (P3)**: Can start after US1 - Independent of earlier stories
- **User Story 7 (P3)**: Can start after US1 - Independent (uses Django admin)
- **User Story 8 (P3)**: Can start after US1 - Independent (uses Swagger UI)

### Within Each User Story

- All screenshot captures marked [P] within a module can run in parallel
- Final screenshot in each module may depend on earlier ones (e.g., need auth first)

### Parallel Opportunities

- T003, T004 can run in parallel (Setup)
- T006, T007, T008 can run in parallel (Foundational utilities)
- T015, T016 can run in parallel (US2 auth screens)
- T018, T019, T020 can run in parallel (US3 client screens)
- T022, T023, T024, T025 can run in parallel (US4 case screens)
- T027, T028 can run in parallel (US5 document screens)
- T032, T033, T034 can run in parallel (US7 admin screens)
- T036, T037 can run in parallel (US8 Swagger screens)

---

## Parallel Example: User Story 4 (Case Management)

```bash
# Launch all case screenshot captures together:
Task: "Implement 03-cases test: capture case list endpoint"
Task: "Implement 03-cases test: capture case create endpoint"
Task: "Implement 03-cases test: capture case detail endpoint"
Task: "Implement 03-cases test: capture case statistics endpoint"

# Then run the final one that may require prior state:
Task: "Implement 03-cases test: capture case close action endpoint"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup (directories and config)
2. Complete Phase 2: Foundational (utilities and test data)
3. Complete Phase 3: User Story 1 (main orchestration)
4. Complete Phase 4: User Story 2 (auth screenshots)
5. **STOP and VALIDATE**: Run generator, verify auth screenshots exist
6. This provides a working screenshot generator with basic output

### Incremental Delivery

1. Setup + Foundational → Infrastructure ready
2. Add US1 (orchestration) → Test runner ready
3. Add US2 (auth) → First module screenshots (MVP!)
4. Add US3, US4, US5 (clients, cases, docs) → Core modules
5. Add US6, US7, US8 (dashboard, admin, swagger) → Complete coverage
6. Polish phase → Final validation and README

### Full Generation Command

```bash
cd tests/e2e
DISABLE_THROTTLING=1 npx playwright test docs/generate-screenshots.spec.ts
```

---

## Notes

- [P] tasks = different screenshots, no dependencies
- [Story] label maps task to specific module documentation
- Each module can be generated independently via `-g` filter
- All screenshots use 1280x720 resolution per FR-005
- README.md auto-generated with all image links per FR-004
- Headless mode supported per FR-009
- Progress logging added per FR-010

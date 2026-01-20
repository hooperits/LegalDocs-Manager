# Tasks: Bilingual README Documentation

**Input**: Design documents from `/specs/010-bilingual-readme/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/readme-sections.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different sections, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Primary deliverable**: `README.md` at repository root
- **Supporting assets**: `docs/screenshots/` (existing)
- **Reference docs**: `API_DOCS.md`, `DEPLOYMENT.md` (existing)

---

## Phase 1: Setup

**Purpose**: Backup existing README and create document skeleton

- [x] T001 Backup existing README.md to README.md.backup
- [x] T002 Create new README.md with header block (title, language toggle, badges) per contracts/readme-sections.md

---

## Phase 2: Foundational (English Section Structure)

**Purpose**: Create the complete English section structure that Spanish will mirror

**⚠️ CRITICAL**: Spanish section mirrors English - complete English structure first

- [x] T003 Add English section anchor and description in README.md
- [x] T004 Add English Table of Contents with all section links in README.md
- [x] T005 Add language section divider with Spanish indicator in README.md

**Checkpoint**: English skeleton with TOC ready - content sections can now be added in parallel

---

## Phase 3: User Story 1 - Language Toggle Navigation (Priority: P1) 🎯 MVP

**Goal**: Enable users to switch between English and Spanish sections with clear visual indicators

**Independent Test**: Click language toggle links and verify navigation to correct language section

### Implementation for User Story 1

- [x] T006 [US1] Verify header block has working language toggle links (🇺🇸/🇪🇸) in README.md
- [x] T007 [US1] Add Spanish section anchor (`#español`) after divider in README.md
- [x] T008 [US1] Add "Switch to English" link in Spanish section header in README.md
- [x] T009 [US1] Add "Cambiar a Español" link in English section for quick access in README.md

**Checkpoint**: Language toggle navigation fully functional

---

## Phase 4: User Story 2 - Quick Navigation Table of Contents (Priority: P1)

**Goal**: Provide clickable navigation to all major sections in both languages

**Independent Test**: Click each TOC link and verify it navigates to correct section

### Implementation for User Story 2

- [x] T010 [P] [US2] Add Spanish Table of Contents with all section links in README.md
- [x] T011 [US2] Verify all English TOC anchor links are valid (13 sections) in README.md
- [x] T012 [US2] Verify all Spanish TOC anchor links are valid (13 sections) in README.md

**Checkpoint**: Both TOCs complete with working navigation

---

## Phase 5: User Story 3 - Visual Feature Overview (Priority: P2)

**Goal**: Showcase system capabilities with icons and screenshots

**Independent Test**: View Features section and verify all icons display, screenshots load with captions

### Implementation for User Story 3

- [x] T013 [P] [US3] Write English Features section with 7 features and icons in README.md
- [x] T014 [P] [US3] Write Spanish Características section with 7 features and icons in README.md
- [x] T015 [P] [US3] Create English Screenshots gallery (collapsible) with 9 key images in README.md
- [x] T016 [P] [US3] Create Spanish Capturas de Pantalla gallery (collapsible) with 9 key images in README.md
- [x] T017 [US3] Add bilingual captions to all screenshots in README.md
- [x] T018 [US3] Add link to full screenshots gallery (docs/screenshots/README.md) in README.md

**Checkpoint**: Visual overview complete in both languages

---

## Phase 6: User Story 4 - Developer Quick Start (Priority: P2)

**Goal**: Enable developers to run the project in 5 copy-paste steps

**Independent Test**: Follow quick start commands on fresh environment and verify server starts

### Implementation for User Story 4

- [x] T019 [P] [US4] Write English Quick Start section with 5-step commands in README.md
- [x] T020 [P] [US4] Write Spanish Inicio Rápido section with 5-step commands in README.md
- [x] T021 [P] [US4] Write English Tech Stack section in README.md
- [x] T022 [P] [US4] Write Spanish Stack Tecnológico section in README.md
- [x] T023 [P] [US4] Write English Installation (detailed) section with prerequisites in README.md
- [x] T024 [P] [US4] Write Spanish Instalación (detailed) section with prerequisites in README.md
- [x] T025 [P] [US4] Write English Environment Variables table in README.md
- [x] T026 [P] [US4] Write Spanish Variables de Entorno table in README.md
- [x] T027 [P] [US4] Write English Database Setup section (PostgreSQL + SQLite) in README.md
- [x] T028 [P] [US4] Write Spanish Configuración de Base de Datos section in README.md
- [x] T029 [P] [US4] Write English Running Tests section in README.md
- [x] T030 [P] [US4] Write Spanish Ejecutar Tests section in README.md
- [x] T031 [P] [US4] Write English Demo Data section in README.md
- [x] T032 [P] [US4] Write Spanish Datos de Demostración section in README.md

**Checkpoint**: Complete developer setup documentation in both languages

---

## Phase 7: User Story 5 - Complete API Reference (Priority: P2)

**Goal**: Document all API endpoints organized by resource

**Independent Test**: Review API section and verify all endpoints are documented with method, path, description

### Implementation for User Story 5

- [x] T033 [P] [US5] Write English API Reference section header with Swagger link in README.md
- [x] T034 [P] [US5] Write Spanish Referencia API section header with Swagger link in README.md
- [x] T035 [P] [US5] Add Authentication endpoints table (4 endpoints) in README.md
- [x] T036 [P] [US5] Add Clients endpoints table (6 endpoints) in README.md
- [x] T037 [P] [US5] Add Cases endpoints table (7 endpoints) in README.md
- [x] T038 [P] [US5] Add Documents endpoints table (5 endpoints) in README.md
- [x] T039 [P] [US5] Add Other endpoints table (Dashboard, Search, Profile) in README.md
- [x] T040 [US5] Add bilingual descriptions to all endpoint tables in README.md

**Checkpoint**: Complete API documentation in both languages

---

## Phase 8: User Story 6 - Professional Visual Presentation (Priority: P3)

**Goal**: Create polished, professional appearance with consistent formatting

**Independent Test**: View README on GitHub and verify badges display, formatting is consistent, mobile view works

### Implementation for User Story 6

- [x] T041 [P] [US6] Verify all 6 badges render correctly in header in README.md
- [x] T042 [P] [US6] Verify consistent header hierarchy (h1→h2→h3) throughout in README.md
- [x] T043 [P] [US6] Verify code blocks have correct syntax highlighting in README.md
- [x] T044 [P] [US6] Verify tables have proper formatting in README.md
- [x] T045 [US6] Add Project Structure tree diagram in English section in README.md
- [x] T046 [US6] Add Estructura del Proyecto tree diagram in Spanish section in README.md

**Checkpoint**: Professional visual presentation verified

---

## Phase 9: User Story 7 - Contribution Guidelines (Priority: P3)

**Goal**: Provide clear contribution process for potential contributors

**Independent Test**: Read Contributing section and verify it answers: how to contribute, testing requirements, PR process

### Implementation for User Story 7

- [x] T047 [P] [US7] Write English Contributing section in README.md
- [x] T048 [P] [US7] Write Spanish Contribuir section in README.md
- [x] T049 [P] [US7] Write English License section with MIT link in README.md
- [x] T050 [P] [US7] Write Spanish Licencia section with MIT link in README.md
- [x] T051 [US7] Add links to API_DOCS.md and DEPLOYMENT.md in README.md

**Checkpoint**: Contribution guidelines complete in both languages

---

## Phase 10: Polish & Validation

**Purpose**: Final validation and cross-cutting improvements

- [x] T052 Validate all 26 internal anchor links work correctly in README.md
- [x] T053 Validate all 9 screenshot image paths are correct in README.md
- [x] T054 Verify content parity between English and Spanish sections in README.md
- [ ] T055 Verify README renders correctly on GitHub web interface
- [ ] T056 Verify README renders correctly on GitHub mobile view
- [x] T057 Remove README.md.backup after successful validation
- [x] T058 Run final line count verification (~600-800 lines expected) in README.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - creates English skeleton
- **US1 (Phase 3)**: Depends on Foundational - adds language toggle
- **US2 (Phase 4)**: Depends on Foundational - adds TOCs
- **US3-US7 (Phases 5-9)**: Can run in parallel after US1+US2 complete
- **Polish (Phase 10)**: Depends on all content phases complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phase 2 - Core navigation
- **User Story 2 (P1)**: Depends on Phase 2 - Works with US1 for complete navigation
- **User Story 3 (P2)**: Depends on US1+US2 - Adds visual content
- **User Story 4 (P2)**: Depends on US1+US2 - Adds developer docs
- **User Story 5 (P2)**: Depends on US1+US2 - Adds API docs
- **User Story 6 (P3)**: Depends on US3-US5 - Verifies formatting
- **User Story 7 (P3)**: Depends on US1+US2 - Adds contribution docs

### Parallel Opportunities

Within each user story phase, all tasks marked [P] can run in parallel:
- US3: Features EN/ES + Screenshots EN/ES (4 parallel tasks)
- US4: All 14 documentation sections can be written in parallel
- US5: All 7 API endpoint tables can be written in parallel
- US6: All 4 verification tasks can run in parallel
- US7: Contributing EN/ES + License EN/ES (4 parallel tasks)

---

## Parallel Example: User Story 4

```bash
# Launch all documentation sections for User Story 4 together:
Task: "Write English Quick Start section in README.md"
Task: "Write Spanish Inicio Rápido section in README.md"
Task: "Write English Tech Stack section in README.md"
Task: "Write Spanish Stack Tecnológico section in README.md"
# ... and so on for all 14 tasks
```

---

## Implementation Strategy

### MVP First (User Stories 1+2 Only)

1. Complete Phase 1: Setup (backup, create skeleton)
2. Complete Phase 2: Foundational (English structure)
3. Complete Phase 3: US1 - Language Toggle
4. Complete Phase 4: US2 - TOC Navigation
5. **STOP and VALIDATE**: Test language switching and TOC navigation
6. Minimal README works - can deploy/demo

### Full Implementation

1. Complete MVP (US1+US2)
2. Add US3: Visual Feature Overview (features + screenshots)
3. Add US4: Developer Quick Start (all setup docs)
4. Add US5: API Reference (all endpoints)
5. Add US6: Professional Presentation (formatting verification)
6. Add US7: Contribution Guidelines
7. Complete Phase 10: Final validation

---

## Notes

- [P] tasks = different sections, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story adds complete bilingual content
- Verify screenshots exist before adding image links
- Commit after each phase or logical group
- Stop at any checkpoint to validate independently
- Total estimated content: ~700 lines of Markdown

---

## Completion Summary

**Status**: ✅ COMPLETE (56/58 tasks done, 2 pending GitHub verification)

**Final Line Count**: 914 lines (exceeds target of 600-800)

**All Screenshots Verified**: 9/9 paths valid

**Content Parity**: Both English and Spanish sections contain equivalent content

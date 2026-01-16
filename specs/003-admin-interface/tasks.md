# Tasks: Django Admin Customization

**Input**: Design documents from `/specs/003-admin-interface/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Task Overview

| Phase | Tasks | Focus |
|-------|-------|-------|
| 1. Setup | 1 | Admin site branding (foundational) |
| 2. User Story 1 | 4 | ClientAdmin enhancement |
| 3. User Story 2 | 5 | CaseAdmin + DocumentInline |
| 4. User Story 3 | 4 | DocumentAdmin enhancement |
| 5. Validation | 3 | Testing and verification |

**Total Tasks**: 17

---

## Phase 1: Setup (Admin Site Branding)

**Purpose**: Configure admin site branding - this applies site-wide and should be done first

- [x] T001 [US4] Create admin site configuration in legaldocs/legaldocs/admin.py with site_header, site_title, index_title
- [x] T002 [US4] Import admin module in legaldocs/legaldocs/urls.py to ensure branding loads

**Checkpoint**: Admin site shows "LegalDocs Manager" header when accessed

---

## Phase 2: User Story 1 - Client Administration (Priority: P1)

**Goal**: Enhanced client management with organized fieldsets, filters, and bulk actions

**Independent Test**: Access /admin/clients/client/ and verify list display, filters, search, fieldsets, and bulk actions

### Implementation for User Story 1

- [x] T003 [US1] Add list_display, list_filter, search_fields, readonly_fields, ordering to ClientAdmin in legaldocs/clients/admin.py
- [x] T004 [US1] Add fieldsets configuration (Información Personal, Contacto, Estado) to ClientAdmin in legaldocs/clients/admin.py
- [x] T005 [US1] Implement activate_clients action with @admin.action decorator in legaldocs/clients/admin.py
- [x] T006 [US1] Implement deactivate_clients action with @admin.action decorator in legaldocs/clients/admin.py

**Checkpoint**: ClientAdmin fully functional with 5-column list, 3 fieldsets, and bulk activate/deactivate actions

---

## Phase 3: User Story 2 - Case Administration (Priority: P1)

**Goal**: Comprehensive case management with colored status badges, inline documents, and bulk close action

**Independent Test**: Access /admin/cases/case/ and verify colored status, inline documents, filters, and mark_as_closed action

### Implementation for User Story 2

- [x] T007 [US2] Add list_display, list_filter, search_fields, readonly_fields, ordering, date_hierarchy to CaseAdmin in legaldocs/cases/admin.py
- [x] T008 [US2] Add fieldsets configuration (Información Básica, Detalles, Fechas, Asignación) to CaseAdmin in legaldocs/cases/admin.py
- [x] T009 [US2] Implement colored_status method with @admin.display decorator and format_html in legaldocs/cases/admin.py
- [x] T010 [US2] Create DocumentInline class (TabularInline) in legaldocs/cases/admin.py with Document model import
- [x] T011 [US2] Implement mark_as_closed action with @admin.action decorator in legaldocs/cases/admin.py

**Checkpoint**: CaseAdmin fully functional with colored badges, inline documents, 4 fieldsets, and bulk close action

---

## Phase 4: User Story 3 - Document Administration (Priority: P1)

**Goal**: Document management with auto-tracking of uploads and human-readable file sizes

**Independent Test**: Upload document via /admin/documents/document/add/ and verify uploaded_by is auto-set and file_size is human-readable

### Implementation for User Story 3

- [x] T012 [US3] Add list_display, list_filter, search_fields, readonly_fields, ordering to DocumentAdmin in legaldocs/documents/admin.py
- [x] T013 [US3] Add fieldsets configuration (Documento, Archivo, Metadatos) to DocumentAdmin in legaldocs/documents/admin.py
- [x] T014 [US3] Implement formatted_file_size method with @admin.display decorator in legaldocs/documents/admin.py
- [x] T015 [US3] Override save_model to auto-set uploaded_by on create in legaldocs/documents/admin.py

**Checkpoint**: DocumentAdmin fully functional with human-readable sizes, auto-set uploaded_by, and organized fieldsets

---

## Phase 5: Validation & Polish

**Purpose**: Verify all admin features work correctly per quickstart.md

- [x] T016 Run Django development server and verify admin site branding (header, title, index)
- [x] T017 Test all admin features per quickstart.md verification checklist
- [x] T018 Verify all edge cases (large files, bulk actions on multiple records)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - sets up admin branding
- **Phase 2 (US1)**: No dependencies on other user stories - can start immediately
- **Phase 3 (US2)**: Requires Document model import but no dependency on DocumentAdmin
- **Phase 4 (US3)**: No dependencies on other user stories
- **Phase 5 (Validation)**: Depends on all user story phases complete

### User Story Independence

All user stories (US1, US2, US3, US4) can be implemented in parallel:

- **US1 (ClientAdmin)**: Independent - modifies only clients/admin.py
- **US2 (CaseAdmin)**: Independent - modifies only cases/admin.py (imports Document model but doesn't depend on DocumentAdmin)
- **US3 (DocumentAdmin)**: Independent - modifies only documents/admin.py
- **US4 (Branding)**: Independent - creates new legaldocs/admin.py

### Parallel Opportunities

```text
# All user story implementations can run in parallel:
Phase 1 (T001-T002): Admin branding
  ↓
Parallel execution possible:
├── Phase 2 (T003-T006): ClientAdmin [US1]
├── Phase 3 (T007-T011): CaseAdmin [US2]
└── Phase 4 (T012-T015): DocumentAdmin [US3]
  ↓
Phase 5 (T016-T018): Validation
```

---

## Implementation Strategy

### MVP First (Recommended Order)

1. Complete Phase 1: Setup (branding)
2. Complete Phase 2: ClientAdmin (US1)
3. Complete Phase 3: CaseAdmin (US2)
4. Complete Phase 4: DocumentAdmin (US3)
5. Complete Phase 5: Validation

### Parallel Execution

If working with multiple developers:
- Developer A: T001-T002 (Setup) then T003-T006 (ClientAdmin)
- Developer B: T007-T011 (CaseAdmin)
- Developer C: T012-T015 (DocumentAdmin)
- All: T016-T018 (Validation)

---

## Git Commit

After completing all tasks:

```bash
git add .
git commit -m "feat(admin): personalizar Django Admin para flujo legal

- Mejorar ClientAdmin con fieldsets y acciones masivas
- Agregar badges de estado con colores en CaseAdmin
- Implementar DocumentInline para edición en línea
- Agregar acción para marcar casos como cerrados
- Auto-asignar uploaded_by en DocumentAdmin
- Mostrar tamaños de archivo legibles
- Configurar branding del sitio admin"
```

---

## Notes

- All admin.py files already exist with basic registration
- This feature enhances existing admin classes, not creating new ones
- DocumentInline requires importing Document model in cases/admin.py (cross-app import at admin level is allowed)
- Use format_html for HTML output in display methods
- Use @admin.action and @admin.display decorators (Django 4.0+ syntax)

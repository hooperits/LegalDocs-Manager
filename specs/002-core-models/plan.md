# Implementation Plan: Core Data Models

**Branch**: `002-core-models` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-core-models/spec.md`

## Summary

Define and implement the core Django models for LegalDocs Manager: Client, Case, and Document. This feature establishes the data layer with proper relationships, custom managers, auto-generated fields, and sample fixtures for testing. Models follow Django best practices with proper Meta classes, __str__ methods, and related_name attributes.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Django 5.0.11, PostgreSQL (psycopg2-binary)
**Storage**: PostgreSQL 15+ (legaldocs_db)
**Testing**: Django TestCase, fixtures for sample data
**Target Platform**: Linux server (development on WSL2/Linux)
**Project Type**: Web application (Django backend)
**Performance Goals**: N/A for models (data layer only)
**Constraints**: Must follow Django ORM conventions, no raw SQL
**Scale/Scope**: POC - 5 clients, 10 cases, 15 documents for demo

## Constitution Check

*GATE: Must pass before implementation.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Django Best Practices First | ✅ PASS | Using Django ORM, Model conventions |
| II. Clean Architecture | ✅ PASS | Each model in its domain app (clients, cases, documents) |
| III. API-First Design | N/A | Models only - API in future feature |
| IV. Documentation Mandatory | ✅ PASS | Docstrings required on all models/methods |
| V. Security by Default | ✅ PASS | File uploads to dedicated directory, proper on_delete |
| Model Conventions | ✅ PASS | __str__, Meta, related_name, verbose_name |
| Commit Standards | ✅ PASS | Spanish commits |

**Gate Result**: PASS - Proceeding with implementation.

## Project Structure

### Documentation (this feature)

```text
specs/002-core-models/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technical decisions
├── data-model.md        # Entity relationships diagram
├── quickstart.md        # Testing guide
└── tasks.md             # Implementation tasks
```

### Source Code (affected files)

```text
legaldocs/
├── clients/
│   ├── models.py        # Client model
│   ├── admin.py         # Client admin registration
│   └── migrations/
├── cases/
│   ├── models.py        # Case model + CaseManager
│   ├── admin.py         # Case admin registration
│   └── migrations/
├── documents/
│   ├── models.py        # Document model
│   ├── admin.py         # Document admin registration
│   └── migrations/
└── fixtures/
    ├── clients.json     # 5 sample clients
    ├── cases.json       # 10 sample cases
    └── documents.json   # 15 sample documents
```

**Structure Decision**: Models placed in their respective domain apps following app-per-domain pattern. Fixtures in centralized fixtures/ directory.

## Complexity Tracking

> No violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

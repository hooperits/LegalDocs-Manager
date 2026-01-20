# Data Model: Bilingual README Structure

**Feature**: 010-bilingual-readme
**Date**: 2026-01-20

## Document Structure

The README.md follows a hierarchical structure with two parallel language sections.

```
README.md
├── Header Block
│   ├── Project Title (centered)
│   ├── Language Toggle Links
│   └── Badges Row
│
├── [English Section] ────────────────────────────
│   ├── Description
│   ├── Table of Contents
│   ├── Features
│   │   └── Feature items with icons
│   ├── Screenshots Gallery (collapsible)
│   │   ├── Swagger UI
│   │   ├── Authentication
│   │   ├── Client Management
│   │   ├── Case Management
│   │   ├── Document Management
│   │   ├── Dashboard & Search
│   │   └── Django Admin
│   ├── Tech Stack
│   ├── Quick Start (5-step minimal setup)
│   ├── Installation (detailed)
│   │   ├── Prerequisites
│   │   └── Step-by-step guide
│   ├── Environment Variables
│   │   ├── Table of variables
│   │   └── Example .env file
│   ├── Database Setup
│   │   ├── PostgreSQL instructions
│   │   └── SQLite instructions
│   ├── Running Tests
│   │   ├── Basic commands
│   │   └── Coverage report
│   ├── Demo Data
│   ├── API Reference
│   │   ├── Authentication endpoints
│   │   ├── Clients endpoints
│   │   ├── Cases endpoints
│   │   ├── Documents endpoints
│   │   └── Other endpoints
│   ├── Project Structure
│   ├── Contributing
│   └── License
│
├── Divider ──────────────────────────────────────
│
└── [Spanish Section] ────────────────────────────
    └── (Mirror of English structure)
```

## Content Entities

### Header Block
- **Title**: "LegalDocs Manager" (centered, h1)
- **Language Toggle**: Emoji flags with anchor links
- **Badges**: 6 shields (Python, Django, DRF, License, Coverage, Tests)

### Feature Item
- **Icon**: Emoji representing the feature
- **Name**: Short feature name
- **Description**: One-line explanation

### Screenshot Entry
- **Image**: Relative path to PNG file
- **Caption**: Bilingual description (English / Spanish)
- **Alt Text**: Accessibility description

### API Endpoint Entry
- **Path**: URL path with variables
- **Method**: HTTP method (GET, POST, PUT, PATCH, DELETE)
- **Description**: What the endpoint does
- **Auth**: Whether authentication is required

### Environment Variable Entry
- **Name**: Variable name (e.g., SECRET_KEY)
- **Description**: What it configures
- **Default**: Default value or "Required"

## Section Mapping (English ↔ Spanish)

| English | Spanish | Anchor EN | Anchor ES |
|---------|---------|-----------|-----------|
| Features | Características | #features | #características |
| Screenshots | Capturas de Pantalla | #screenshots | #capturas-de-pantalla |
| Tech Stack | Stack Tecnológico | #tech-stack | #stack-tecnológico |
| Quick Start | Inicio Rápido | #quick-start | #inicio-rápido |
| Installation | Instalación | #installation | #instalación |
| Environment Variables | Variables de Entorno | #environment-variables | #variables-de-entorno |
| Database Setup | Configuración de BD | #database-setup | #configuración-de-base-de-datos |
| Running Tests | Ejecutar Tests | #running-tests | #ejecutar-tests |
| Demo Data | Datos de Demo | #demo-data | #datos-de-demostración |
| API Reference | Referencia API | #api-reference | #referencia-api |
| Project Structure | Estructura del Proyecto | #project-structure | #estructura-del-proyecto |
| Contributing | Contribuir | #contributing | #contribuir |
| License | Licencia | #license | #licencia |

## Validation Rules

1. **Anchor uniqueness**: No duplicate anchor IDs in the document
2. **Image paths**: All screenshot paths must exist in `docs/screenshots/`
3. **Link validity**: All internal links must resolve to existing anchors
4. **Content parity**: Every section in English must have a Spanish equivalent
5. **Badge accuracy**: Coverage and test count badges must reflect current state (98%, 163 tests)

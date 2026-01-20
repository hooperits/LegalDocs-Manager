# Research: Bilingual README Documentation

**Feature**: 010-bilingual-readme
**Date**: 2026-01-20

## Bilingual README Patterns

### Decision: Single-file with Language Sections

**Rationale**: GitHub automatically renders README.md on repository landing page. Using a single file with clearly separated language sections ensures:
- Maximum discoverability (GitHub prioritizes README.md)
- Easy navigation with anchor links
- No file switching required
- Works on all GitHub interfaces (web, mobile, API)

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Separate README.md + README.es.md | GitHub only renders README.md on main page; Spanish version would be hidden |
| Directory structure (docs/en/, docs/es/) | Requires navigation away from landing page |
| Language toggle via GitHub Actions | Over-engineering for a static documentation task |

### Decision: Language Toggle at Top + Dual TOC

**Rationale**: Place language selector links prominently at the very top, before any content. Each language section has its own complete Table of Contents. This pattern is used by popular multilingual projects.

**Implementation Pattern**:
```markdown
<div align="center">

# LegalDocs Manager

🇺🇸 [English](#english) | 🇪🇸 [Español](#español)

</div>
```

## GitHub Markdown Best Practices

### Decision: Use HTML for Enhanced Formatting

**Rationale**: GitHub-Flavored Markdown supports embedded HTML for:
- Centered headers with `<div align="center">`
- Collapsible sections with `<details>` and `<summary>`
- Better table formatting
- Badge alignment

### Decision: Shield.io Badges

**Rationale**: Industry standard for project status badges. Already in use in current README.

**Badges to Include**:
- Python version
- Django version
- DRF version
- License (MIT)
- Coverage percentage
- Tests passing count

### Decision: Screenshot Gallery with Captions

**Rationale**: Visual documentation increases engagement and understanding. Existing 24 screenshots should be organized with bilingual captions.

**Format**:
```markdown
<details>
<summary>📸 View Screenshots / Ver Capturas</summary>

### Swagger API Documentation / Documentación API Swagger
![Swagger Overview](docs/screenshots/07-api/01-swagger-overview.png)
*Interactive API documentation / Documentación interactiva de la API*

</details>
```

## Existing Assets Inventory

### Screenshots Available (24 total)

| Module | Count | Files |
|--------|-------|-------|
| 01-auth | 3 | auth-endpoints-overview, login-endpoint, register-endpoint |
| 02-clients | 4 | clients-endpoints-overview, client-list, client-create, client-detail |
| 03-cases | 5 | cases-endpoints-overview, case-list-filters, case-create, case-statistics, case-close |
| 04-documents | 3 | documents-endpoints-overview, document-list, document-upload |
| 05-dashboard | 2 | dashboard-endpoint, search-endpoint |
| 06-admin | 4 | admin-login, admin-dashboard, admin-clients-list, admin-cases-list |
| 07-api | 3 | swagger-overview, swagger-header, swagger-try-it-out |

### Existing Documentation Files

| File | Purpose | To Be Linked |
|------|---------|--------------|
| API_DOCS.md | Detailed API documentation | Yes |
| DEPLOYMENT.md | Production deployment guide | Yes |
| docs/screenshots/README.md | Screenshots gallery | Yes |

## Section Structure

Based on spec requirements (FR-001 to FR-014), the README will have these sections in each language:

### English Sections
1. Header (title, badges, description)
2. Table of Contents
3. Features (with icons/screenshots)
4. Screenshots Gallery (collapsible)
5. Tech Stack
6. Quick Start
7. Installation (detailed)
8. Environment Variables
9. Database Setup
10. Running Tests
11. Demo Data
12. API Reference
13. Project Structure
14. Contributing
15. License

### Spanish Sections (Equivalent)
1. Encabezado (título, badges, descripción)
2. Tabla de Contenidos
3. Características (con iconos/capturas)
4. Galería de Capturas (colapsable)
5. Stack Tecnológico
6. Inicio Rápido
7. Instalación (detallada)
8. Variables de Entorno
9. Configuración de Base de Datos
10. Ejecutar Tests
11. Datos de Demostración
12. Referencia de API
13. Estructura del Proyecto
14. Contribuir
15. Licencia

## Navigation Strategy

### Anchor Link Convention
- English anchors: lowercase with hyphens (e.g., `#installation`, `#api-reference`)
- Spanish anchors: lowercase with hyphens, prefixed with `-es` suffix (e.g., `#instalación-es`, `#referencia-api-es`)

This avoids conflicts while maintaining readable URLs.

## References

- [GitHub Markdown Guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Shields.io Badges](https://shields.io/)
- [Best README Templates](https://github.com/othneildrew/Best-README-Template)

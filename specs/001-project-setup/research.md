# Research: Project Setup

**Feature**: 001-project-setup
**Date**: 2026-01-16
**Status**: Complete

## Research Tasks

This feature is primarily infrastructure setup with well-established patterns. Research focuses on confirming best practices and version compatibility.

---

### 1. Django 5.x Project Structure Best Practices

**Decision**: Use flat project structure with apps inside the project directory.

**Rationale**:
- Django 5.x maintains the same project structure conventions as Django 4.x
- Placing apps inside the project directory (`legaldocs/core/`, `legaldocs/users/`) keeps imports clean and consistent
- The `startproject` command creates the standard structure; `startapp` creates apps at the current directory level
- This matches Django's official tutorial structure and is immediately recognizable to Django developers

**Alternatives Considered**:
- Separate `apps/` directory: Rejected because it adds unnecessary nesting and non-standard import paths
- Apps at repository root: Rejected because it mixes concerns and complicates deployment

---

### 2. Environment Variable Management: python-dotenv vs django-environ

**Decision**: Use `python-dotenv` for environment variable management.

**Rationale**:
- Lighter weight than django-environ (fewer dependencies)
- Simple API: `load_dotenv()` + `os.getenv()`
- Widely used and well-documented
- Sufficient for POC scope
- Constitution specifies `python-decouple` or `django-environ`, but `python-dotenv` achieves the same goal with simpler implementation

**Alternatives Considered**:
- `django-environ`: More features (URL parsing, type casting) but overkill for this POC
- `python-decouple`: Similar to python-dotenv but with type coercion; either would work
- Manual os.environ: No .env file support, worse developer experience

**Note**: This is a minor deviation from constitution which mentions `python-decouple`. Justified because python-dotenv is functionally equivalent and more commonly used in Django tutorials.

---

### 3. PostgreSQL Configuration for Django

**Decision**: Use standard Django database configuration with environment variables.

**Rationale**:
- `psycopg2-binary` is the recommended PostgreSQL adapter for development
- Environment variables for all connection parameters (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
- UTC timezone and utf8 encoding are Django best practices
- `read committed` isolation level is PostgreSQL/Django default and appropriate for web applications

**Alternatives Considered**:
- `psycopg[binary]` (psycopg3): Newer but Django 5.0 has better psycopg2 support
- `DATABASE_URL` single variable: Cleaner but requires URL parsing library
- SQLite for development: Rejected because PostgreSQL is production target and we want dev/prod parity

---

### 4. Django REST Framework Configuration

**Decision**: Configure DRF with TokenAuthentication, pagination, and filtering out of the box.

**Rationale**:
- TokenAuthentication is simple and stateless, ideal for API-first design
- SessionAuthentication kept for Django Admin compatibility
- PageNumberPagination with PAGE_SIZE=20 is reasonable default
- django-filter integration provides powerful queryset filtering
- SearchFilter and OrderingFilter are DRF built-ins that complement django-filter

**Alternatives Considered**:
- JWT Authentication: More complex, requires additional package (djangorestframework-simplejwt)
- Session-only auth: Not suitable for API-first design
- No default pagination: Would require adding pagination to every view

---

### 5. CORS Configuration

**Decision**: Configure django-cors-headers with localhost:3000 as allowed origin.

**Rationale**:
- React/Next.js frontend will run on port 3000 during development
- CORS headers are required for browser-based API calls from different origins
- Whitelist approach (CORS_ALLOWED_ORIGINS) is more secure than CORS_ALLOW_ALL_ORIGINS

**Alternatives Considered**:
- CORS_ALLOW_ALL_ORIGINS=True: Insecure, only for testing
- No CORS: Would block frontend development entirely
- Proxy through Django: Adds complexity, masks real deployment architecture

---

### 6. Static and Media Files Configuration

**Decision**: Use Django's built-in static files handling with STATICFILES_DIRS and MEDIA_ROOT.

**Rationale**:
- `static/` directory at project root for CSS, JS, images
- `media/` directory for user uploads (legal documents)
- Development server serves both via Django
- Production will use whitenoise or nginx (future consideration)

**Alternatives Considered**:
- S3/cloud storage for media: Overkill for POC, adds complexity
- No STATICFILES_DIRS: Would require static files in app directories only

---

### 7. .gitignore Best Practices for Django/Python

**Decision**: Use comprehensive .gitignore covering Python, Django, and IDE files.

**Rationale**:
- Must ignore: `.env`, `venv/`, `__pycache__/`, `*.pyc`, `.sqlite3`, `media/`
- Should ignore: IDE files (`.idea/`, `.vscode/`), OS files (`.DS_Store`)
- Should NOT ignore: `requirements.txt`, `.env.example`, `static/` (project static files)

**Source**: GitHub's Python .gitignore template + Django-specific additions

---

## Resolved Clarifications

| Item | Resolution |
|------|------------|
| Environment variable library | python-dotenv (deviation from constitution's python-decouple, justified above) |
| Database adapter | psycopg2-binary for development simplicity |
| Authentication method | TokenAuthentication + SessionAuthentication |
| Project structure | Flat structure with apps in project directory |

## Dependencies Confirmed

| Package | Version | Purpose | Compatibility |
|---------|---------|---------|---------------|
| Django | 5.0.11 | Web framework | Python 3.10+ |
| djangorestframework | 3.15.2 | REST API | Django 4.2+ |
| psycopg2-binary | 2.9.10 | PostgreSQL adapter | Python 3.7+ |
| python-dotenv | 1.0.1 | Env var management | Python 3.8+ |
| Pillow | 11.1.0 | Image handling | Python 3.9+ |
| django-cors-headers | 4.6.0 | CORS support | Django 4.2+ |
| django-filter | 24.3 | Queryset filtering | Django 4.2+ |

All packages are compatible with Python 3.11+ and Django 5.0.x.

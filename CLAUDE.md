# LegalDocs-Manager Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-16

## Active Technologies
- Python 3.11+ + Django 5.0.11 (built-in admin module) (003-admin-interface)
- PostgreSQL 15+ (legaldocs_db) (003-admin-interface)
- Python 3.11+ + Django 5.x, Django REST Framework 3.15+, django-filter, drf-spectacular, django-cors-headers (004-rest-api)
- PostgreSQL 15+ (existing database with Client, Case, Document models) (004-rest-api)

- Python 3.11+ + Django 5.0.11, djangorestframework 3.15.2, psycopg2-binary 2.9.10, python-dotenv 1.0.1, Pillow 11.1.0, django-cors-headers 4.6.0, django-filter 24.3 (001-project-setup)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11+: Follow standard conventions

## Recent Changes
- 004-rest-api: Added Python 3.11+ + Django 5.x, Django REST Framework 3.15+, django-filter, drf-spectacular, django-cors-headers
- 003-admin-interface: Added Python 3.11+ + Django 5.0.11 (built-in admin module)

- 001-project-setup: Added Python 3.11+ + Django 5.0.11, djangorestframework 3.15.2, psycopg2-binary 2.9.10, python-dotenv 1.0.1, Pillow 11.1.0, django-cors-headers 4.6.0, django-filter 24.3

<!-- MANUAL ADDITIONS START -->

## Commit & PR Guidelines

- Do NOT add "Co-Authored-By" lines to commits
- Do NOT add "Generated with Claude Code" or similar attribution lines to PRs
- Keep commits and PRs clean without tool attribution

<!-- MANUAL ADDITIONS END -->

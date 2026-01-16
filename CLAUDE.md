# LegalDocs-Manager Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-16

## Active Technologies
- Python 3.11+ + Django 5.0.11 (built-in admin module) (003-admin-interface)
- PostgreSQL 15+ (legaldocs_db) (003-admin-interface)
- Python 3.11+ + Django 5.x, Django REST Framework 3.15+, django-filter, drf-spectacular, django-cors-headers (004-rest-api)
- PostgreSQL 15+ (existing database with Client, Case, Document models) (004-rest-api)
- Python 3.11+ + Django 5.x + Django REST Framework 3.15+, rest_framework.authtoken (already installed) (005-auth-dashboard)
- Python 3.11+ + Django 5.x, Django REST Framework 3.15+, coverage.py (006-testing-docs)
- PostgreSQL 15+ (SQLite for tests) (006-testing-docs)

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
- 006-testing-docs: Added Python 3.11+ + Django 5.x, Django REST Framework 3.15+, coverage.py
- 005-auth-dashboard: Added Python 3.11+ + Django 5.x + Django REST Framework 3.15+, rest_framework.authtoken (already installed)
- 004-rest-api: Added Python 3.11+ + Django 5.x, Django REST Framework 3.15+, django-filter, drf-spectacular, django-cors-headers


<!-- MANUAL ADDITIONS START -->

## Commit & PR Guidelines

- Do NOT add "Co-Authored-By" lines to commits
- Do NOT add "Generated with Claude Code" or similar attribution lines to PRs
- Keep commits and PRs clean without tool attribution

## Post-Spec Completion Workflow

After completing all tasks in a spec, automatically run:

1. `git push -u origin <branch-name>` - Push branch to remote
2. `gh pr create --title "..." --body "..."` - Create pull request
3. `gh pr merge <pr-number> --merge --delete-branch` - Merge PR and delete remote branch
4. `git checkout master && git pull origin master` - Switch to master and pull changes
5. `git fetch --prune` - Clean up stale remote tracking branches

<!-- MANUAL ADDITIONS END -->
